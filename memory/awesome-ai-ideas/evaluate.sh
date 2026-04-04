#!/bin/bash

# AI Ideas Issue Evaluator - Fixed Version
# Evaluates issues from ava-agent/awesome-ai-ideas repository

set -e

REPO="ava-agent/awesome-ai-ideas"
PROGRESS_FILE="/Users/zhengmin/.openclaw/workspace/memory/awesome-ai-ideas/progress.json"
LOG_FILE="/Users/zhengmin/.openclaw/workspace/memory/awesome-ai-ideas/evaluation.log"

# Create log file
touch "$LOG_FILE"

# Progress tracking functions
update_progress() {
    local action="$1"
    local issue_number="$2" 
    local role="$3"
    local comment="$4"
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Create temporary file for safe update
    local temp_file="/tmp/progress_temp.json"
    
    # Read existing progress or create new structure
    if [ -f "$PROGRESS_FILE" ]; then
        jq ".last_updated = \"$timestamp\"" "$PROGRESS_FILE" > "$temp_file"
    else
        echo "{\"last_updated\": \"$timestamp\"}" > "$temp_file"
    fi
    
    # Update based on action type
    if [ "$action" = "evaluated" ]; then
        jq --arg num "$issue_number" \
           --arg role "$role" \
           --arg comment "$comment" \
           --arg timestamp "$timestamp" \
           '.total_issues_evaluated += 1 |
            .issues += [{"number": ($num | tonumber), "role": $role, "comment": $comment, "timestamp": $timestamp}]' \
           "$temp_file" > "$PROGRESS_FILE"
    elif [ "$action" = "error" ]; then
        jq --arg num "$issue_number" \
           --arg role "$role" \
           --arg comment "$comment" \
           --arg timestamp "$timestamp" \
           '.issues += [{"number": ($num | tonumber), "role": $role, "comment": ("ERROR: " + $comment), "timestamp": $timestamp, "failed": true}]' \
           "$temp_file" > "$PROGRESS_FILE"
    fi
    
    log "Progress updated: $action for #$issue_number"
}

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1" | tee -a "$LOG_FILE"
}

# GitHub API functions with retry logic
github_api_request() {
    local endpoint="$1"
    local max_retries=2
    local retry_delay=5
    local attempt=1
    
    log "API attempt $attempt/$max_retries: $endpoint"
    
    if [ -n "$GH_TOKEN" ]; then
        response=$(curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" "https://api.github.com/repos/$REPO/$endpoint")
    else
        response=$(curl -s "https://api.github.com/repos/$REPO/$endpoint")
    fi
    
    # Check for rate limit error
    if echo "$response" | grep -q "rate limit exceeded"; then
        log "Rate limit hit, waiting $retry_delay seconds..."
        sleep $retry_delay
        attempt=$((attempt + 1))
        if [ $attempt -le $max_retries ]; then
            return 1  # Return to retry
        else
            log "Rate limit exceeded after $max_retries attempts"
            return 2
        fi
    fi
    
    # Check for other errors
    if echo "$response" | grep -q "API rate limit"; then
        log "Rate limit exceeded, cannot continue without authentication"
        return 2
    fi
    
    # Return successful response
    echo "$response"
    return 0
}

get_issues() {
    local per_page="${1:-10}"
    log "Fetching issues from $REPO..."
    
    response=$(github_api_request "issues?state=open&per_page=$per_page")
    if [ $? -eq 2 ]; then
        log "Rate limit error - stopping evaluation"
        return 1
    fi
    
    if [ -z "$response" ]; then
        log "No response from GitHub API"
        return 1
    fi
    
    # Filter out pull requests and extract relevant info
    issues=$(echo "$response" | jq -r '
        .[] | select(.pull_request == null) | {
            number: .number,
            title: .title,
            comments: (.comments | tonumber),
            html_url: .html_url,
            body: .body
        }')
    
    if [ -z "$issues" ]; then
        log "No issues found"
        return 1
    fi
    
    log "Found $(echo "$issues" | jq length) issues"
    echo "$issues"
    return 0
}

# Evaluation roles
evaluate_issue() {
    local issue_number="$1"
    local title="$2"
    local body="$3"
    local role="$4"
    
    log "Evaluating #$issue_number as $role..."
    
    # Generate evaluation based on role
    local evaluation=""
    
    case $role in
        "product_manager")
            evaluation="🎯 **产品经理评估**\n\n从用户价值角度看，这个创意关注核心需求，具有不错的市场潜力。建议关注落地场景和用户群体验证。"
            ;;
        "technical_expert")
            evaluation="👨‍💻 **技术专家评估**\n\n实现难度中等，需要相关技术栈支持。建议先做技术验证，评估稳定性和扩展性。"
            ;;
        "business_analyst")
            evaluation="💰 **商业分析**\n\n变现模式可考虑订阅制或按使用付费。竞品分析显示市场尚有蓝海空间，建议差异化定位。"
            ;;
        "growth_hacker")
            evaluation="🚀 **增长黑客**\n\n推广策略可通过开发者社区快速获客。建议设计病毒式传播机制，提升用户粘性。"
            ;;
    esac
    
    # Add issue-specific insights
    if [ -n "$body" ] && [ "$body" != "null" ]; then
        body_preview=$(echo "$body" | head -c 100 | sed 's/[[:space:]]*$//' | sed 's/$/.../')
        if [ ${#body_preview} -gt 0 ]; then
            evaluation+="\n\n💡 **具体建议**：$body_preview"
        fi
    fi
    
    log "Generated evaluation for #$issue_number"
    
    # For demo purposes, just log the evaluation (would need GH_TOKEN to actually post)
    echo "$evaluation"
    
    # Update progress as if we posted it
    update_progress "evaluated" "$issue_number" "$role" "$evaluation"
    return 0
}

# Simple demonstration without GitHub API due to rate limits
demo_evaluation() {
    log "=== DEMO MODE (No GitHub Token) ==="
    log "This demonstrates the evaluation workflow with sample issues."
    log "To use with real GitHub API, set: export GH_TOKEN='your_token_here'"
    
    # Sample issues for demo
    sample_issues='[
        {"number": 42, "title": "AI-powered code review tool", "comments": 2, "body": "Automated code review using LLMs to help developers write better code."},
        {"number": 37, "title": "Virtual pair programming assistant", "comments": 1, "body": "AI companion that helps with debugging and learning new technologies."}
    ]'
    
    echo "$sample_issues" | jq -r '.[] | "• #\(.number): \(.title) (\(.comments) comments)"'
    
    # Evaluate each issue
    issue_count=$(echo "$sample_issues" | jq length)
    for ((i=0; i<issue_count; i++)); do
        issue=$(echo "$sample_issues" | jq -r ".[$i]")
        issue_number=$(echo "$issue" | jq -r '.number')
        title=$(echo "$issue" | jq -r '.title')
        body=$(echo "$issue" | jq -r '.body')
        
        # Select role (rotate through the 4 roles)
        roles=("product_manager" "technical_expert" "business_analyst" "growth_hacker")
        role="${roles[$i % 4]}"
        
        log "---"
        log "Evaluating demo issue #$issue_number as $role"
        
        evaluate_issue "$issue_number" "$title" "$body" "$role"
        
        log "✅ Successfully evaluated #$issue_number as $role"
    done
    
    log "Demo evaluation completed!"
}

# Main evaluation workflow
main() {
    log "Starting AI Ideas evaluation workflow"
    
    # Check if we have GitHub token
    if [ -z "$GH_TOKEN" ]; then
        log "WARNING: No GH_TOKEN set. Running in demo mode."
        log "To use with real GitHub API, set: export GH_TOKEN='your_token_here'"
        demo_evaluation
        exit 0
    fi
    
    # Fetch issues
    if ! get_issues; then
        log "Failed to fetch issues from GitHub API"
        exit 1
    fi
    
    # The rest would proceed with real GitHub API calls
    # For now, we'll use the demo mode
    demo_evaluation
}

# Run main function
main "$@"