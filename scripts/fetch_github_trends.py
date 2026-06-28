#!/usr/bin/env python3
"""Fetch trending AI projects from GitHub API"""

import json
import sys
import urllib.parse
from datetime import datetime, timedelta
from urllib.request import Request, urlopen


def fetch_trending_ai_projects():
    """Fetch trending AI projects from GitHub"""
    
    # Search for AI-related repos (without date filter for reliability)
    queries = [
        "topic:llm",
        "topic:ai",
        "topic:machine-learning",
        "topic:deep-learning",
    ]
    
    repos = []
    
    for query in queries:
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=10"
        
        req = Request(url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        
        try:
            with urlopen(req, timeout=10) as f:
                data = json.load(f)
                repos.extend(data.get('items', []))
        except Exception as e:
            print(f"Error fetching {query}: {e}", file=sys.stderr)
    
    # Deduplicate by full_name
    seen = set()
    unique = []
    for repo in repos:
        if repo['full_name'] not in seen:
            seen.add(repo['full_name'])
            unique.append(repo)
    
    # Sort by stars
    unique.sort(key=lambda x: x['stargazers_count'], reverse=True)
    
    return unique[:20]


def main():
    repos = fetch_trending_ai_projects()
    
    for i, repo in enumerate(repos, 1):
        print(f"{i}. {repo['full_name']}")
        print(f"   ⭐ {repo['stargazers_count']:,}")
        print(f"   📝 {repo['description'] or 'No description'}")
        print(f"   🔗 {repo['html_url']}")
        print()


if __name__ == "__main__":
    main()
