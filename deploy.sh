#!/bin/bash

# AI Study Balance Assistant - Quick Deploy Script
echo "🚀 Deploying AI Study Balance Assistant to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Initialize and deploy
echo "🚀 Deploying your app..."
railway init
railway up

echo "✅ Deployment complete!"
echo "🌐 Your app is now live at the URL shown above!"
echo "📱 Share this URL with your co-worker and anyone else!"
echo ""
echo "💡 Next steps:"
echo "1. Copy the URL from Railway"
echo "2. Send it to your co-worker"
echo "3. They can use it immediately on any device!" 