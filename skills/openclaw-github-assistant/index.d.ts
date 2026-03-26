/**
 * OpenClaw GitHub Skill
 * Query and manage GitHub repositories from conversation
 *
 * TypeScript version - Compiled to JavaScript for OpenClaw
 */
import { Context, RepositoryListParams, RepoDetailsParams, CIStatusParams, RecentActivityParams, CreateIssueParams, CreateRepoParams, SearchReposParams, CreatePRParams, ListReposResult, Repository, CheckCIResult, RecentActivityResult, Issue, SearchReposResult, PullRequest } from './types';
export declare const skillName = "github";
export declare const skillVersion = "2.0.1";
export declare const skillDescription = "Query and manage GitHub repositories";
declare function listReposHandler(args: RepositoryListParams, context: Context): Promise<ListReposResult>;
declare function getRepoHandler(args: RepoDetailsParams, context: Context): Promise<Repository>;
declare function checkCIStatusHandler(args: CIStatusParams, context: Context): Promise<CheckCIResult>;
declare function getRecentActivityHandler(args: RecentActivityParams, context: Context): Promise<RecentActivityResult>;
declare function createIssueHandler(args: CreateIssueParams, context: Context): Promise<Issue>;
declare function createRepoHandler(args: CreateRepoParams, context: Context): Promise<Repository>;
declare function searchReposHandler(args: SearchReposParams, context: Context): Promise<SearchReposResult>;
declare function createPullRequestHandler(args: CreatePRParams, context: Context): Promise<PullRequest>;
declare const skill: {
    name: string;
    version: string;
    description: string;
    actions: {
        list_repos: {
            description: string;
            parameters: {
                type: string;
                properties: {
                    type: {
                        type: string;
                        enum: string[];
                        default: string;
                    };
                    sort: {
                        type: string;
                        enum: string[];
                        default: string;
                    };
                    language: {
                        type: string;
                    };
                    limit: {
                        type: string;
                        default: number;
                    };
                };
            };
            handler: typeof listReposHandler;
        };
        get_repo: {
            description: string;
            parameters: {
                type: string;
                properties: {
                    owner: {
                        type: string;
                    };
                    repo: {
                        type: string;
                    };
                };
                required: string[];
            };
            handler: typeof getRepoHandler;
        };
        check_ci_status: {
            description: string;
            parameters: {
                type: string;
                properties: {
                    owner: {
                        type: string;
                    };
                    repo: {
                        type: string;
                    };
                };
                required: string[];
            };
            handler: typeof checkCIStatusHandler;
        };
        get_recent_activity: {
            description: string;
            parameters: {
                type: string;
                properties: {
                    repo: {
                        type: string;
                    };
                    limit: {
                        type: string;
                        default: number;
                    };
                };
                required: string[];
            };
            handler: typeof getRecentActivityHandler;
        };
        create_issue: {
            description: string;
            parameters: {
                type: string;
                properties: {
                    repo: {
                        type: string;
                    };
                    title: {
                        type: string;
                    };
                    body: {
                        type: string;
                    };
                    extra: {
                        type: string;
                    };
                };
                required: string[];
            };
            handler: typeof createIssueHandler;
        };
        create_repo: {
            description: string;
            parameters: {
                type: string;
                properties: {
                    name: {
                        type: string;
                        description: string;
                    };
                    description: {
                        type: string;
                        description: string;
                    };
                    private: {
                        type: string;
                        description: string;
                        default: boolean;
                    };
                    auto_init: {
                        type: string;
                        description: string;
                        default: boolean;
                    };
                };
                required: string[];
            };
            handler: typeof createRepoHandler;
        };
        create_pull_request: {
            description: string;
            parameters: {
                type: string;
                properties: {
                    owner: {
                        type: string;
                        description: string;
                    };
                    repo: {
                        type: string;
                        description: string;
                    };
                    title: {
                        type: string;
                        description: string;
                    };
                    body: {
                        type: string;
                        description: string;
                    };
                    head: {
                        type: string;
                        description: string;
                    };
                    base: {
                        type: string;
                        description: string;
                        default: string;
                    };
                };
                required: string[];
            };
            handler: typeof createPullRequestHandler;
        };
        search_repos: {
            description: string;
            parameters: {
                type: string;
                properties: {
                    query: {
                        type: string;
                    };
                    sort: {
                        type: string;
                        enum: string[];
                        default: string;
                    };
                    limit: {
                        type: string;
                        default: number;
                    };
                };
                required: string[];
            };
            handler: typeof searchReposHandler;
        };
    };
};
export default skill;
//# sourceMappingURL=index.d.ts.map