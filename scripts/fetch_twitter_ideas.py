#!/usr/bin/env python3
"""Fetch Twitter/X trending AI topics and create AI idea issues"""

import json
import requests
import subprocess
import os
import re
from datetime import datetime


def fetch_twitter_trends():
    """Fetch trending topics from X/Twitter using xurl CLI"""
    # First, check xurl is available
    try:
        subprocess.run(["xurl", "--help"], capture_output=True, check=True)
    except Exception as e:
        print("xurl not available. Falling back to web search for AI trends.")
        return fetch_ai_trends_from_web()

    # Use xurl to get trending topics - let's try using search for AI-related tweets
    search_queries = [
        "AI",
        "LLM",
        "machine learning",
        "AI agent",
        "generative AI"
    ]
    all_tweets = []
    for query in search_queries:
        try:
            result = subprocess.run(
                ["xurl", "search", query, "-n", "30"],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            tweets = data.get("data", [])
            for tweet in tweets:
                # Add public metrics if available
                metrics = tweet.get("public_metrics", {})
                all_tweets.append({
                    "text": tweet.get("text", ""),
                    "id": tweet.get("id"),
                    "likes": metrics.get("like_count", 0),
                    "retweets": metrics.get("retweet_count", 0),
                    "replies": metrics.get("reply_count", 0),
                    "created_at": tweet.get("created_at")
                })
        except Exception as e:
            print(f"Error searching for {query}: {e}")

    # Sort by likes descending
    all_tweets.sort(key=lambda x: x["likes"], reverse=True)
    return all_tweets[:20]


def fetch_ai_trends_from_web():
    """Fallback: fetch AI trends from other sources (Hacker News, GitHub) if xurl fails"""
    print("Using fallback sources for AI trends...")
    # Fetch top HN stories with AI keywords
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        response = requests.get(top_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:30]
        stories = []
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_resp = requests.get(story_url, timeout=10)
            story = story_resp.json()
            if story and story.get("title"):
                title = story["title"].lower()
                keywords = ["ai", "llm", "machine learning", "artificial intelligence", "gpt", "agent", "generative"]
                if any(kw in title for kw in keywords):
                    stories.append({
                        "text": story["title"],
                        "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        "likes": story.get("score", 0),
                        "comments": story.get("descendants", 0),
                        "type": "hn"
                    })
                    if len(stories) >= 5:
                        break
        # Convert to tweet-like structure
        return [{
            "text": s["text"],
            "url": s["url"],
            "likes": s["likes"],
            "type": "hn"
        } for s in stories]
    except Exception as e:
        print(f"Error fetching HN stories: {e}")
        # Last resort: return a default AI trend
        return [{
            "text": "AI Agents for Personal Productivity - The Next Big Thing",
            "url": "https://example.com",
            "likes": 1000,
            "type": "default"
        }]


def sanitize_filename(title):
    """Sanitize title for use as filename"""
    # Remove special chars, replace spaces with hyphens, limit length
    sanitized = re.sub(r'[^\w\s-]', '', title)
    sanitized = re.sub(r'[-\s]+', '-', sanitized).strip('-')
    return sanitized[:80]


def create_idea_file(trend, issue_num):
    """Create a markdown file in ideas/ directory"""
    # Generate idea content based on trend
    idea_title = f"💡 [Twitter Hot] {trend['text'][:60]}..." if len(trend['text']) > 60 else f"💡 [Twitter Hot] {trend['text']}"
    content = f"""# {idea_title}

## Issue #{issue_num}

---

## 🎯 问题

**痛点背景：**
- Twitter/X 热门话题揭示了当前 AI 领域最受关注的方向
- 来自真实用户讨论的高热度内容，获得 {trend.get('likes', 0):,} 赞
- 灵感来源：{trend.get('url', f'https://x.com/i/status/{trend.get("id", "")}')}

**具体问题：**
- 从热门讨论中识别可以用 AI 产品化的方向
- 挖掘社区关注但尚未满足的需求
- 将技术趋势转化为用户场景

---

## 🤖 功能

**核心功能：**
- 基于热门讨论场景的 AI 解决方案
- 针对 Twitter/X 社区用户的特定需求设计
- 快速响应热点趋势，提供实时价值

**特色功能：**
- 贴合社区文化和语言习惯
- 利用实时讨论数据进行持续迭代
- 社区参与的产品验证机制

---

## 🏗️ 方案

**技术架构：**
- 前端：简洁高效的用户界面
- 后端：AI 驱动的智能处理
- 数据层：实时讨论分析和用户反馈收集

**实现路线：**
- MVP：核心功能验证，在 Twitter/X 社区测试
- V1：功能完善，用户体验优化
- V2：生态扩展，商业化探索

**技术栈：**
- 现代 Web 技术栈
- AI/LLM 集成
- 社交媒体 API 集成

---

*生成时间：{datetime.now().strftime('%Y-%m-%d')}*
*基于 Twitter/X 热门：{trend.get('url', f'https://x.com/i/status/{trend.get("id", "")}')}*
"""
    # Create file
    filename = f"ideas/issue-{issue_num}-twitter-{sanitize_filename(trend['text'])}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename


def create_github_issue(trend):
    """Create GitHub issue using gh CLI"""
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_dir)
    # Create issue title and body
    title = f"💡 [Twitter Hot] {trend['text'][:80]}..." if len(trend['text']) > 80 else f"💡 [Twitter Hot] {trend['text']}"
    body = f"""Twitter/X 热门 AI 话题：{trend.get('url', f'https://x.com/i/status/{trend.get("id", "")}')}

**赞：** {trend.get('likes', 0):,}

---

{trend['text'][:1000]}

---

*自动生成的 AI 创意 Issue*
"""
    # Write to temp file
    with open("issue-body.md", "w", encoding="utf-8") as f:
        f.write(body)
    # Run gh CLI
    result = subprocess.run(
        ["gh", "issue", "create", "--repo", "ava-agent/awesome-ai-ideas", "--title", title, "--body-file", "issue-body.md"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        # Extract issue number from output
        output = result.stdout.strip()
        import re
        match = re.search(r"/(\d+)$", output)
        issue_num = match.group(1) if match else "unknown"
        # Create idea file
        idea_file = create_idea_file(trend, issue_num)
        print(f"Issue created: {output}")
        print(f"Idea file: {idea_file}")
        # Commit the idea file
        try:
            subprocess.run(["git", "config", "user.name", "kevinten"], check=True)
            subprocess.run(["git", "config", "user.email", "596823919@qq.com"], check=True)
            subprocess.run(["git", "add", idea_file], check=True)
            subprocess.run(["git", "commit", "-m", f"Add idea from Twitter hot (issue #{issue_num})"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Committed and pushed.")
        except Exception as e:
            print(f"Git error: {e}")
        return issue_num
    else:
        print(f"Error creating issue: {result.stderr}")
        return None


def main():
    print("Fetching Twitter/X trending AI topics...")
    trends = fetch_twitter_trends()
    if not trends:
        print("No trends found.")
        return
    # Print top 10
    print("\nTop 10 trends:")
    for i, trend in enumerate(trends[:10], 1):
        print(f"{i}. [{trend.get('likes', 0):,} ⭐] {trend['text'][:80]}...")
    # Pick the first one
    selected_trend = trends[0]
    print(f"\nSelected trend: {selected_trend['text']}")
    # Create issue
    issue_num = create_github_issue(selected_trend)
    if issue_num:
        print(f"Success! Issue #{issue_num} created.")
    else:
        print("Failed to create issue.")


if __name__ == "__main__":
    main()
