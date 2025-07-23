# 🚀 Render Deployment Guide

## Step 1: Install Git (if not already installed)

1. **Download Git for Windows:**
   - Go to: https://git-scm.com/download/win
   - Download and install with default settings
   - Restart your terminal/PowerShell

## Step 2: Create GitHub Repository

1. **Go to GitHub:**
   - Visit: https://github.com
   - Sign in or create account
   - Click "New repository"

2. **Create Repository:**
   - Name: `ai-study-assistant`
   - Make it **Public**
   - Don't initialize with README (we have files)
   - Click "Create repository"

## Step 3: Push Code to GitHub

After installing Git, run these commands in your project folder:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-study-assistant.git
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

## Step 4: Deploy on Render

1. **Go to Render:**
   - Visit: https://render.com
   - Click "Sign Up" or "Get Started"
   - Sign up with your GitHub account

2. **Create New Web Service:**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub account if not already connected

3. **Configure Your Service:**
   - **Repository**: Select your `ai-study-assistant` repository
   - **Name**: `ai-study-assistant` (or any name you want)
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Plan**: `Free`
   - **Region**: Choose closest to you (US East, US West, etc.)

4. **Advanced Settings (Optional):**
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: ✅ Enabled (deploys on every Git push)

5. **Click "Create Web Service"**

## Step 5: Wait for Deployment

- **Build time**: 5-10 minutes
- **Status**: You'll see "Building" → "Deploying" → "Live"
- **URL**: You'll get a URL like `https://ai-study-assistant.onrender.com`

## Step 6: Test Your App

1. **Visit your URL**
2. **Create an account** to test full functionality
3. **Try the chat** - send a message to test AI responses
4. **Test on mobile** - should work perfectly

## 🎉 You're Done!

Your AI Study Assistant is now:
- ✅ **Publicly accessible** at your Render URL
- ✅ **Free forever** - no payment required
- ✅ **Mobile-friendly** - works on all devices
- ✅ **Auto-updating** - deploys when you push code changes

## 📱 Sharing Your App

Share your Render URL with:
- **Friends & classmates**
- **Study groups**
- **Social media**
- **Anyone with internet access**

## ⚠️ Important Notes

### **Sleep/Wake Behavior:**
- **First visit**: 30-60 seconds to wake up
- **Subsequent visits**: Instant loading
- **After 15 minutes**: Goes to sleep
- **Next visitor**: Wakes up automatically

### **Free Tier Limits:**
- **750 hours/month** (almost unlimited)
- **100GB bandwidth/month** (plenty for sharing)
- **Sleep after 15 minutes** of inactivity

## 🛠️ Troubleshooting

### **Build Fails:**
- Check that all files are committed to GitHub
- Ensure `Dockerfile` is in the root directory
- Verify `render.yaml` exists

### **App Won't Load:**
- Check the deployment logs in Render dashboard
- Ensure the backend is starting correctly
- Wait 30-60 seconds for first load

### **AI Not Responding:**
- Check the backend logs in Render
- Test with a simple message first
- Verify the AI service is working

## 🔄 Updating Your App

To update your app:
1. Make changes to your code
2. Push to GitHub: `git add . && git commit -m "Update" && git push`
3. Render automatically deploys the changes

## 🎯 Next Steps

1. **Customize your app** - add your own branding
2. **Share with friends** - send them the URL
3. **Monitor usage** - check Render dashboard for stats
4. **Add features** - enhance the AI responses

**Your AI Study Assistant is now live and helping students worldwide! 🌍** 