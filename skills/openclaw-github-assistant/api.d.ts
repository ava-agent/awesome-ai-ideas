/**
 * GitHub API Module
 * Core functions for interacting with GitHub API
 */
import { Context, Repository, RepositoryListParams, RepoDetailsParams, CIStatusParams, RecentActivityParams, CreateIssueParams, Issue, CreateRepoParams, SearchReposParams, SearchReposResult, CreatePRParams, PullRequest, ListReposResult, CheckCIResult, RecentActivityResult } from './types';
/**
 * Get auth headers for API requests
 */
export declare function getAuthHeaders(context: Context): Record<string, string>;
/**
 * Get GitHub username
 */
export declare function getUsername(context: Context): Promise<string>;
/**
 * List repositories
 */
export declare function listRepos(args: RepositoryListParams, context: Context): Promise<ListReposResult>;
/**
 * Get repository details
 */
export declare function getRepo(args: RepoDetailsParams, context: Context): Promise<Repository>;
/**
 * Check CI/CD status
 */
export declare function checkCIStatus(args: CIStatusParams, context: Context): Promise<CheckCIResult>;
/**
 * Get recent activity (commits)
 */
export declare function getRecentActivity(args: RecentActivityParams, context: Context): Promise<RecentActivityResult>;
/**
 * Create an issue
 */
export declare function createIssue(args: CreateIssueParams, context: Context): Promise<Issue>;
/**
 * Create a new repository
 */
export declare function createRepo(args: CreateRepoParams, context: Context): Promise<Repository>;
/**
 * Search repositories
 */
export declare function searchRepos(args: SearchReposParams, context: Context): Promise<SearchReposResult>;
/**
 * Create a pull request
 */
export declare function createPullRequest(args: CreatePRParams, context: Context): Promise<PullRequest>;
//# sourceMappingURL=api.d.ts.map