"use strict";
/**
 * OpenClaw GitHub Skill
 * Query and manage GitHub repositories from conversation
 *
 * TypeScript version - Compiled to JavaScript for OpenClaw
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.skillDescription = exports.skillVersion = exports.skillName = void 0;
const api_1 = require("./api");
// Skill metadata
exports.skillName = 'github';
exports.skillVersion = '2.0.1';
exports.skillDescription = 'Query and manage GitHub repositories';
// Handler functions with proper signatures
async function listReposHandler(args, context) {
    return (0, api_1.listRepos)(args, context);
}
async function getRepoHandler(args, context) {
    return (0, api_1.getRepo)(args, context);
}
async function checkCIStatusHandler(args, context) {
    return (0, api_1.checkCIStatus)(args, context);
}
async function getRecentActivityHandler(args, context) {
    return (0, api_1.getRecentActivity)(args, context);
}
async function createIssueHandler(args, context) {
    return (0, api_1.createIssue)(args, context);
}
async function createRepoHandler(args, context) {
    return (0, api_1.createRepo)(args, context);
}
async function searchReposHandler(args, context) {
    return (0, api_1.searchRepos)(args, context);
}
async function createPullRequestHandler(args, context) {
    return (0, api_1.createPullRequest)(args, context);
}
// Skill definition for OpenClaw
const skill = {
    name: exports.skillName,
    version: exports.skillVersion,
    description: exports.skillDescription,
    actions: {
        list_repos: {
            description: 'List your repositories',
            parameters: {
                type: 'object',
                properties: {
                    type: { type: 'string', enum: ['owner', 'all', 'member'], default: 'owner' },
                    sort: { type: 'string', enum: ['created', 'updated', 'pushed', 'full_name'], default: 'updated' },
                    language: { type: 'string' },
                    limit: { type: 'number', default: 30 }
                }
            },
            handler: listReposHandler
        },
        get_repo: {
            description: 'Get repository details',
            parameters: {
                type: 'object',
                properties: {
                    owner: { type: 'string' },
                    repo: { type: 'string' }
                },
                required: ['owner', 'repo']
            },
            handler: getRepoHandler
        },
        check_ci_status: {
            description: 'Check CI/CD pipeline status',
            parameters: {
                type: 'object',
                properties: {
                    owner: { type: 'string' },
                    repo: { type: 'string' }
                },
                required: ['owner', 'repo']
            },
            handler: checkCIStatusHandler
        },
        get_recent_activity: {
            description: 'Get recent commits',
            parameters: {
                type: 'object',
                properties: {
                    repo: { type: 'string' },
                    limit: { type: 'number', default: 10 }
                },
                required: ['repo']
            },
            handler: getRecentActivityHandler
        },
        create_issue: {
            description: 'Create a new issue',
            parameters: {
                type: 'object',
                properties: {
                    repo: { type: 'string' },
                    title: { type: 'string' },
                    body: { type: 'string' },
                    extra: { type: 'object' }
                },
                required: ['repo', 'title']
            },
            handler: createIssueHandler
        },
        create_repo: {
            description: 'Create a new repository',
            parameters: {
                type: 'object',
                properties: {
                    name: { type: 'string', description: 'Repository name' },
                    description: { type: 'string', description: 'Repository description' },
                    private: { type: 'boolean', description: 'Private repository', default: false },
                    auto_init: { type: 'boolean', description: 'Initialize with README', default: true }
                },
                required: ['name']
            },
            handler: createRepoHandler
        },
        create_pull_request: {
            description: 'Create a pull request',
            parameters: {
                type: 'object',
                properties: {
                    owner: { type: 'string', description: 'Repository owner' },
                    repo: { type: 'string', description: 'Repository name' },
                    title: { type: 'string', description: 'PR title' },
                    body: { type: 'string', description: 'PR description' },
                    head: { type: 'string', description: 'Source branch' },
                    base: { type: 'string', description: 'Target branch', default: 'main' }
                },
                required: ['owner', 'repo', 'title', 'head']
            },
            handler: createPullRequestHandler
        },
        search_repos: {
            description: 'Search your repositories',
            parameters: {
                type: 'object',
                properties: {
                    query: { type: 'string' },
                    sort: { type: 'string', enum: ['stars', 'updated', 'created'], default: 'updated' },
                    limit: { type: 'number', default: 30 }
                },
                required: ['query']
            },
            handler: searchReposHandler
        }
    }
};
// Export for both CommonJS and ES modules
exports.default = skill;
module.exports = skill;
//# sourceMappingURL=index.js.map