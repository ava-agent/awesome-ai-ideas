/**
 * GitHub Skill - Type Definitions
 */
export interface GitHubConfig {
    token?: string;
    username?: string;
}
export interface Context {
    config?: {
        github?: GitHubConfig;
    };
}
export interface Repository {
    name: string;
    full_name: string;
    description: string | null;
    stars: number;
    forks: number;
    watchers?: number;
    language: string | null;
    open_issues?: number;
    updated: string;
    created?: string;
    pushed?: string;
    url: string;
    private: boolean;
    default_branch?: string;
}
export interface RepositoryListParams {
    type?: 'owner' | 'all' | 'member';
    sort?: 'created' | 'updated' | 'pushed' | 'full_name';
    direction?: 'asc' | 'desc';
    language?: string;
    limit?: number;
}
export interface RepoDetailsParams {
    owner: string;
    repo: string;
}
export interface CIStatusParams {
    owner: string;
    repo: string;
}
export interface WorkflowRun {
    name: string;
    status: string;
    conclusion: string | null;
    branch: string;
    commit: string;
    created: string;
    url: string;
}
export interface RecentActivityParams {
    repo: string;
    limit?: number;
}
export interface Commit {
    sha: string;
    message: string;
    author: string;
    date: string;
    url: string;
}
export interface CreateIssueParams {
    repo: string;
    title: string;
    body?: string;
    extra?: Record<string, unknown>;
}
export interface Issue {
    number: number;
    title: string;
    url: string;
    state: string;
}
export interface CreateRepoParams {
    name: string;
    description?: string;
    private?: boolean;
    auto_init?: boolean;
}
export interface SearchReposParams {
    query: string;
    sort?: 'stars' | 'updated' | 'created';
    limit?: number;
}
export interface CreatePRParams {
    owner: string;
    repo: string;
    title: string;
    body?: string;
    head: string;
    base?: string;
}
export interface PullRequest {
    number: number;
    title: string;
    url: string;
    state: string;
    head: string;
    base: string;
}
export interface ListReposResult {
    total: number;
    repos: Repository[];
}
export interface SearchReposResult {
    total: number;
    repos: Repository[];
}
export interface CheckCIResult {
    repo: string;
    runs: WorkflowRun[];
}
export interface RecentActivityResult {
    repo: string;
    commits: Commit[];
}
//# sourceMappingURL=types.d.ts.map