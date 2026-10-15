#!/usr/bin/env python3
"""
fetch_repos_graphql.py - Ultra-Optimized GraphQL Repository Fetcher

Integrates `github-api-rate-limit-optimization` with `github-architect`.
Fetches up to 100 repositories along with topics, licenses, and CI workflow status
in a SINGLE GraphQL query (1 API quota point).
"""

import sys
import json
import os
import subprocess
from typing import List, Dict, Any

GRAPHQL_QUERY = """
query ($login: String!) {
  user(login: $login) {
    repositories(first: 100, orderBy: {field: PUSHED_AT, direction: DESC}) {
      nodes {
        name
        description
        isFork
        isArchived
        pushedAt
        updatedAt
        stargazerCount
        forkCount
        openIssues: issues(states: OPEN) {
          totalCount
        }
        licenseInfo {
          name
          spdxId
        }
        repositoryTopics(first: 10) {
          nodes {
            topic {
              name
            }
          }
        }
        object(expression: "HEAD:.github/workflows") {
          ... on Tree {
            entries {
              name
            }
          }
        }
      }
    }
  }
}
"""

def fetch_repos(username: str) -> List[Dict[str, Any]]:
    """Execute authenticated GraphQL query unsetting stale GITHUB_TOKEN if needed."""
    cmd = ["gh", "api", "graphql", "-f", f"query={GRAPHQL_QUERY}", "-F", f"login={username}"]
    env = os.environ.copy()
    if "GITHUB_TOKEN" in env:
        del env["GITHUB_TOKEN"]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
        data = json.loads(res.stdout)
    except Exception as e:
        sys.stderr.write(f"GraphQL Query Failed: {e}\n")
        return []

    user_data = data.get("data", {}).get("user", {})
    if not user_data:
        return []

    raw_nodes = user_data.get("repositories", {}).get("nodes", [])
    enriched_repos = []

    for node in raw_nodes:
        # Check workflow presence
        wf_tree = node.get("object")
        has_ci = bool(wf_tree and isinstance(wf_tree, dict) and wf_tree.get("entries"))

        # Extract topics
        topics_nodes = node.get("repositoryTopics", {}).get("nodes", [])
        topics = [t["topic"]["name"] for t in topics_nodes if "topic" in t]

        # Extract license
        license_info = node.get("licenseInfo")
        license_name = license_info.get("name") if license_info else None

        enriched = {
            "name": node.get("name"),
            "description": node.get("description"),
            "is_fork": node.get("isFork", False),
            "is_archived": node.get("isArchived", False),
            "pushed_at": node.get("pushedAt") or node.get("updatedAt"),
            "updated_at": node.get("updatedAt"),
            "stargazers_count": node.get("stargazerCount", 0),
            "forks_count": node.get("forkCount", 0),
            "open_issues_count": node.get("openIssues", {}).get("totalCount", 0),
            "has_readme": True,
            "has_license": bool(license_name),
            "license": license_name,
            "has_ci": has_ci,
            "topics": topics
        }
        enriched_repos.append(enriched)

    return enriched_repos

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "borjamoskv"
    repos = fetch_repos(username)
    print(json.dumps(repos, indent=2))

if __name__ == "__main__":
    main()
