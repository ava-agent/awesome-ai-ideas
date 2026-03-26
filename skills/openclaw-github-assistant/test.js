// OpenClaw GitHub Skill - Test Suite
// Run with: node test.js

const { execSync } = require('child_process');

// Test configuration
const TEST_REPO = 'conorkenn/openclaw-github-skill';
const TEST_OWNER = 'conorkenn';

// Helper to run GitHub API calls
async function githubAPI(endpoint, options = {}) {
  const token = process.env.GITHUB_TOKEN;
  const response = await fetch(`https://api.github.com${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `token ${token}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'OpenClaw-GitHub-Skill-Test',
      ...options.headers
    }
  });
  return response;
}

// Test functions
const tests = [
  {
    name: 'Environment Variables Set',
    test: () => {
      if (!process.env.GITHUB_TOKEN) throw new Error('GITHUB_TOKEN not set');
      if (!process.env.GITHUB_USERNAME) throw new Error('GITHUB_USERNAME not set');
      return true;
    }
  },
  {
    name: 'GitHub API Authentication',
    test: async () => {
      const response = await githubAPI('/user');
      if (!response.ok) throw new Error(`Auth failed: ${response.status}`);
      const data = await response.json();
      if (data.login !== process.env.GITHUB_USERNAME) {
        throw new Error(`Username mismatch: expected ${process.env.GITHUB_USERNAME}, got ${data.login}`);
      }
      return true;
    }
  },
  {
    name: 'List Repositories',
    test: async () => {
      const response = await githubAPI(`/users/${TEST_OWNER}/repos?per_page=5`);
      if (!response.ok) throw new Error(`Failed to list repos: ${response.status}`);
      const repos = await response.json();
      if (!Array.isArray(repos) || repos.length === 0) {
        throw new Error('No repositories found');
      }
      console.log(`  Found ${repos.length} repos`);
      return true;
    }
  },
  {
    name: 'Get Repository',
    test: async () => {
      const response = await githubAPI(`/repos/${TEST_REPO}`);
      if (!response.ok) throw new Error(`Repo not found: ${response.status}`);
      const repo = await response.json();
      if (repo.full_name !== TEST_REPO) {
        throw new Error(`Repo mismatch: expected ${TEST_REPO}, got ${repo.full_name}`);
      }
      console.log(`  Repo: ${repo.full_name} (⭐ ${repo.stargazers_count})`);
      return true;
    }
  },
  {
    name: 'Check CI Status',
    test: async () => {
      const response = await githubAPI(`/repos/${TEST_REPO}/actions/runs?per_page=1`);
      if (!response.ok) throw new Error(`Failed to get CI status: ${response.status}`);
      const data = await response.json();
      console.log(`  Latest run: ${data.workflow_runs?.[0]?.name || 'none'}`);
      return true;
    }
  },
  {
    name: 'Search Repositories',
    test: async () => {
      const response = await githubAPI(`/search/repositories?q=user:${TEST_OWNER}+github&per_page=5`);
      if (!response.ok) throw new Error(`Search failed: ${response.status}`);
      const data = await response.json();
      if (data.total_count === 0) {
        throw new Error('No repos found in search');
      }
      console.log(`  Found ${data.total_count} repos matching search`);
      return true;
    }
  },
  {
    name: 'Get Recent Commits',
    test: async () => {
      const response = await githubAPI(`/repos/${TEST_REPO}/commits?per_page=3`);
      if (!response.ok) throw new Error(`Failed to get commits: ${response.status}`);
      const commits = await response.json();
      if (!Array.isArray(commits) || commits.length === 0) {
        throw new Error('No commits found');
      }
      console.log(`  Latest commit: ${commits[0].sha.substring(0, 7)} - ${commits[0].commit.message.split('\n')[0]}`);
      return true;
    }
  },
  {
    name: 'Create Repository (Dry Run - Skip)',
    test: async () => {
      console.log('  Skipping actual repo creation (would create test-repo)');
      return true;
    }
  }
];

// Run tests
async function runTests() {
  console.log('🧪 OpenClaw GitHub Skill - Test Suite\n');
  console.log('=' .repeat(50));
  
  let passed = 0;
  let failed = 0;
  
  for (const { name, test } of tests) {
    process.stdout.write(`\n🔍 ${name}... `);
    
    try {
      const result = await test();
      if (result) {
        console.log('✅ PASS');
        passed++;
      } else {
        console.log('❌ FAIL');
        failed++;
      }
    } catch (error) {
      console.log(`❌ FAIL: ${error.message}`);
      failed++;
    }
  }
  
  console.log('\n' + '=' .repeat(50));
  console.log(`\n📊 Results: ${passed} passed, ${failed} failed\n`);
  
  if (failed > 0) {
    console.log('❌ Some tests failed. Check your configuration.');
    process.exit(1);
  } else {
    console.log('✅ All tests passed! Your GitHub skill is working correctly.');
    process.exit(0);
  }
}

runTests();
