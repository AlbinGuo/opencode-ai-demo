#!/bin/bash
# 代码推送脚本

echo "=== 百度热搜榜代码推送 ==="
echo ""

# 推送到Gitee
echo "1. 推送到Gitee..."
echo "   仓库: https://gitee.com/guonan01/vibe-coding.git"
read -p "   请输入Gitee访问令牌(密码): " -s GITEE_TOKEN
echo ""

if [ ! -z "$GITEE_TOKEN" ]; then
    git push https://guonan01:$GITEE_TOKEN@gitee.com/guonan01/vibe-coding.git master
    echo "   Gitee推送完成!"
else
    echo "   已跳过Gitee推送"
fi

echo ""

# 推送到GitHub
echo "2. 推送到GitHub..."
echo "   仓库: https://github.com/your-username/vibe-coding.git"
echo "   (请将 your-username 替换为你的实际GitHub用户名)"

# 检查GitHub远程仓库URL
GITHUB_URL=$(git remote get-url github 2>/dev/null)
if [ "$GITHUB_URL" = "https://github.com/your-username/vibe-coding.git" ]; then
    echo "   警告: GitHub仓库URL未配置，请先更新:"
    echo "   git remote set-url github https://github.com/YOUR_USERNAME/vibe-coding.git"
else
    read -p "   请输入GitHub访问令牌: " -s GITHUB_TOKEN
    echo ""

    if [ ! -z "$GITHUB_TOKEN" ]; then
        # 提取用户名
        GITHUB_USER=$(echo "$GITHUB_URL" | sed 's|https://||' | sed 's|/.*||')
        git push https://$GITHUB_USER:$GITHUB_TOKEN@$GITHUB_URL master
        echo "   GitHub推送完成!"
    else
        echo "   已跳过GitHub推送"
    fi
fi

echo ""
echo "=== 推送完成 ==="
