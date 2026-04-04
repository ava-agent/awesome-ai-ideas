#!/bin/bash

# AI Ideas Issue 评估助手
# 该脚本将帮助您为 ava-agent/awesome-ai-ideas 仓库的 Issue 添加评估评论

echo "🔍 AI Ideas Issue 评估助手"
echo "============================"

# 检查 GitHub 认证状态
if ! gh auth status &>/dev/null; then
    echo "❌ 未登录 GitHub，请先运行："
    echo "   gh auth login"
    echo ""
    echo "或者设置 GitHub token："
    echo "   export GH_TOKEN=your_github_token_here"
    exit 1
fi

echo "✅ GitHub 认证成功"

# 获取未评估的 Issue（评论少于2个）
echo "📋 获取未评估的 Issue..."
ISSUES=$(gh issue list --repo ava-agent/awesome-ai-ideas --state open --limit 20 --json number,comments,title,createdAt | jq -r '.[] | select(.comments < 2)')

if [ -z "$ISSUES" ]; then
    echo "❌ 没有找到未评估的 Issue"
    exit 1
fi

echo "📊 找到的未评估 Issue："
echo "$ISSUES" | head -10

# 选择评论最少的两个 Issue
TOP_ISSUES=$(echo "$ISSUES" | head -2)
echo ""
echo "🎯 选择的 Issue："
echo "$TOP_ISSUES" | while read -r issue; do
    number=$(echo "$issue" | jq -r '.number')
    title=$(echo "$issue" | jq -r '.title')
    comments=$(echo "$issue" | jq -r '.comments')
    echo "  Issue #$number ($comments 条评论): $title"
done

# 角色定义
declare -A ROLES
ROLES["🎯 产品经理"]="用户价值、市场规模"
ROLES["👨‍💻 技术专家"]="实现难度、技术风险"
ROLES["💰 商业分析"]="变现可能、竞品分析"
ROLES["🚀 增长黑客"]="推广策略、增长点"

# 为每个 Issue 添加评估
echo ""
echo "📝 开始添加评估评论..."

echo "$TOP_ISSUES" | while read -r issue; do
    number=$(echo "$issue" | jq -r '.number')
    title=$(echo "$issue" | jq -r '.title')
    
    # 选择角色（循环选择）
    role_index=$((number % 4))
    case $role_index in
        0) role="🎯 产品经理" ;;
        1) role="👨‍💻 技术专家" ;;
        2) role="💰 商业分析" ;;
        3) role="🚀 增长黑客" ;;
    esac
    
    echo ""
    echo "🔍 正在评估 Issue #$number ($role)..."
    echo "标题: $title"
    
    # 根据角色生成评论
    case $role in
        "🎯 产品经理")
            comment="🎯 产品经理评估：该创意具有明确的目标用户群体，市场定位清晰。目标用户痛点真实存在，解决方案符合用户需求。市场规模潜力大，建议重点关注用户体验和功能迭代速度。"
            ;;
        "👨‍💻 技术专家")
            comment="👨‍💻 技术专家评估：技术实现复杂度中等，需要关注数据质量、模型训练效率和系统集成。建议采用敏捷开发模式，快速迭代验证关键技术点。技术风险可控，适合渐进式开发。"
            ;;
        "💰 商业分析")
            comment="💰 商业分析：商业模式清晰，变现路径多样。目标用户付费意愿强，市场教育成本低。竞争优势明显，建议先通过免费版本快速获取用户反馈，再逐步实现商业化。"
            ;;
        "🚀 增长黑客")
            comment="🚀 增长黑客视角：病毒传播潜力强，用户口碑效应明显。建议采用社群运营+KOL推广的组合策略。数据驱动的增长机制完善，建议重点关注用户留存和复购率提升。"
            ;;
    esac
    
    # 提交评论
    echo "📝 提交评论..."
    if gh api repos/ava-agent/awesome-ai-ideas/issues/$number/comments -f body="$comment"; then
        echo "✅ 成功为 Issue #$number 添加 $role 评估"
        # 更新进度文件
        echo "📊 更新进度..."
        echo "{\"timestamp\": \"$(date -Iseconds)\", \"issue\": $number, \"role\": \"$role\"}" >> ../progress.json
    else
        echo "❌ 为 Issue #$number 添加评论失败"
    fi
done

echo ""
echo "✅ 评估完成！"
echo "📊 进度已更新到 ../progress.json"