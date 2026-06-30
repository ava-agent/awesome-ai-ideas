#!/usr/bin/env python3
import requests
import json
import subprocess
import os

def main():
    # Fetch top HN stories
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(top_stories_url)
    response.raise_for_status()
    story_ids = response.json()[:10]  # Take top 10
    
    # Get details for each story
    stories = []
    for story_id in story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_resp = requests.get(story_url)
        story = story_resp.json()
        if story and story.get("title") and story.get("url"):
            stories.append(story)
            if len(stories) >= 3:  # Take up to 3 to choose from
                break
    
    if not stories:
        print("No valid stories found.")
        return
    
    # Pick the first one
    story = stories[0]
    title = f"💡 {story['title']}"
    body = f"Hacker News: {story['url']}\n\nScore: {story.get('score')} | Comments: {story.get('descendants')}"
    
    # Create a GitHub issue using gh CLI
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_dir)
    
    # Write issue body to a temp file to avoid shell escaping issues
    with open("issue-body.md", "w") as f:
        f.write(body)
    
    # Run gh issue create
    result = subprocess.run(
        ["gh", "issue", "create", "--repo", "ava-agent/awesome-ai-ideas", "--title", title, "--body-file", "issue-body.md"],
        capture_output=True,
        text=True,
        check=True
    )
    print("Issue created successfully:", result.stdout.strip())

if __name__ == "__main__":
    main()
