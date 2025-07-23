#!/bin/bash

echo "🚀 Deploying AI Study Assistant to Railway..."
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please run these commands first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git branch -M main"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/ai-study-assistant.git"
    echo "   git push -u origin main"
    echo ""
    echo "Then visit: https://railway.app/"
    echo "1. Sign in with GitHub"
    echo "2. Click 'New Project'"
    echo "3. Select 'Deploy from GitHub repo'"
    echo "4. Choose your repository"
    echo "5. Click 'Deploy Now'"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Git remote not set. Please run:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/ai-study-assistant.git"
    exit 1
fi

echo "✅ Git repository found!"
echo ""

# Push latest changes
echo "📤 Pushing latest changes to GitHub..."
git add .
git commit -m "Update for deployment" || echo "No changes to commit"
git push origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🌐 Now deploy on Railway:"
echo "1. Go to: https://railway.app/"
echo "2. Sign in with GitHub"
echo "3. Click 'New Project'"
echo "4. Select 'Deploy from GitHub repo'"
echo "5. Choose your repository"
echo "6. Click 'Deploy Now'"
echo ""
echo "⏳ Wait 5-10 minutes for deployment to complete"
echo "🎉 You'll get a public URL like: https://your-app-name.railway.app"
echo ""
echo "📱 Share that URL with anyone - they can use your AI assistant!" 