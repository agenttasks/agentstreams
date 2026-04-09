/**
 * GitHub GraphQL client — typed queries via @octokit/graphql.
 *
 * Wraps @octokit/graphql with auth from CLAUDE_CODE_OAUTH_TOKEN or
 * GITHUB_TOKEN. Provides pre-built queries for PR review, repo metadata,
 * and commit history — the operations most needed by agentstreams pipelines.
 *
 * Auth: GITHUB_TOKEN env var (never ANTHROPIC_API_KEY).
 */

import { graphql } from "@octokit/graphql";

// ── Types ──────────────────────────────────────────────────────

export interface RepoInfo {
  nameWithOwner: string;
  description: string | null;
  stargazerCount: number;
  defaultBranchRef: { name: string } | null;
  url: string;
  isArchived: boolean;
  primaryLanguage: { name: string } | null;
}

export interface PullRequestInfo {
  number: number;
  title: string;
  body: string;
  state: string;
  mergeable: string;
  additions: number;
  deletions: number;
  changedFiles: number;
  headRefName: string;
  baseRefName: string;
  author: { login: string } | null;
  reviews: { totalCount: number };
  commits: { totalCount: number };
}

export interface CommitInfo {
  oid: string;
  messageHeadline: string;
  committedDate: string;
  author: { name: string | null; email: string | null } | null;
  additions: number;
  deletions: number;
  changedFilesIfAvailable: number | null;
}

// ── Client ─────────────────────────────────────────────────────

export class GitHubGraphQL {
  private gql: typeof graphql;

  constructor(token?: string) {
    const t = token ?? process.env.GITHUB_TOKEN;
    if (!t) {
      throw new Error(
        "GitHub token required: set GITHUB_TOKEN env var or pass token to constructor",
      );
    }
    this.gql = graphql.defaults({
      headers: { authorization: `token ${t}` },
    });
  }

  /** Fetch repository metadata */
  async getRepo(owner: string, name: string): Promise<RepoInfo> {
    const { repository } = await this.gql<{ repository: RepoInfo }>(
      `query ($owner: String!, $name: String!) {
        repository(owner: $owner, name: $name) {
          nameWithOwner
          description
          stargazerCount
          defaultBranchRef { name }
          url
          isArchived
          primaryLanguage { name }
        }
      }`,
      { owner, name },
    );
    return repository;
  }

  /** Fetch pull request details */
  async getPullRequest(
    owner: string,
    repo: string,
    number: number,
  ): Promise<PullRequestInfo> {
    const { repository } = await this.gql<{
      repository: { pullRequest: PullRequestInfo };
    }>(
      `query ($owner: String!, $repo: String!, $number: Int!) {
        repository(owner: $owner, name: $repo) {
          pullRequest(number: $number) {
            number title body state mergeable
            additions deletions changedFiles
            headRefName baseRefName
            author { login }
            reviews { totalCount }
            commits { totalCount }
          }
        }
      }`,
      { owner, repo, number },
    );
    return repository.pullRequest;
  }

  /** Fetch recent commits on a branch */
  async getCommits(
    owner: string,
    repo: string,
    branch: string,
    count = 20,
  ): Promise<CommitInfo[]> {
    const { repository } = await this.gql<{
      repository: {
        ref: {
          target: {
            history: { nodes: CommitInfo[] };
          };
        } | null;
      };
    }>(
      `query ($owner: String!, $repo: String!, $branch: String!, $count: Int!) {
        repository(owner: $owner, name: $repo) {
          ref(qualifiedName: $branch) {
            target {
              ... on Commit {
                history(first: $count) {
                  nodes {
                    oid messageHeadline committedDate
                    author { name email }
                    additions deletions changedFilesIfAvailable
                  }
                }
              }
            }
          }
        }
      }`,
      { owner, repo, branch: `refs/heads/${branch}`, count },
    );
    return repository.ref?.target?.history?.nodes ?? [];
  }

  /** Run an arbitrary GraphQL query */
  async query<T>(q: string, variables?: Record<string, unknown>): Promise<T> {
    return this.gql<T>(q, variables);
  }
}
