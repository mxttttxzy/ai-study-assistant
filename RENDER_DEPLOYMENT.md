# 🚀 Render Deployment Guide - Free AI Study Assistant

## 🎯 **Deploy to Render in 5 Minutes**

This guide will help you deploy your free AI study assistant to Render.com with zero cost!

---

## 📋 Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Render Account**: Free account at [render.com](https://render.com)
3. **Repository**: This project should be in your GitHub repository

---

## 🚀 Quick Deployment Steps

### 1. **Prepare Your Repository**

Ensure your repository has these files:
- ✅ `render.yaml` - Render configuration
- ✅ `Dockerfile` - Multi-stage Docker build
- ✅ `start.sh` - Startup script
- ✅ `nginx.conf` - Nginx configuration
- ✅ `docker-compose.yml` - Local development
- ✅ `README.md` - Project documentation

### 2. **Connect to Render**

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign in or create a free account

2. **Create New Web Service**
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure the Service**
   - **Name**: `ai-study-assistant` (or your preferred name)
   - **Environment**: `Docker`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (root of repository)

### 3. **Environment Variables**

The `render.yaml` file already includes the necessary environment variables:

```yaml
envVars:
  - key: JWT_SECRET_KEY
    value: your-secret-key-here-change-in-production
  - key: DATABASE_URL
    value: sqlite:///./ai_assistant.db
  - key: DEFAULT_AI_MODEL
    value: fallback-enhanced
  - key: MAX_TOKENS
    value: "2048"
  - key: TEMPERATURE
    value: "0.7"
  - key: REACT_APP_BACKEND_URL
    value: https://ai-study-assistant.onrender.com
```

**Important**: Update the `REACT_APP_BACKEND_URL` to match your actual Render URL!

### 4. **Deploy**

1. **Click "Create Web Service"**
2. **Wait for Build**: This takes 5-10 minutes
3. **Check Logs**: Monitor the build process
4. **Access Your App**: Use the provided URL

---

## 🔧 Configuration Details

### **Free Tier Limitations**
- **Build Time**: 500 minutes/month
- **Runtime**: 750 hours/month
- **Sleep**: Services sleep after 15 minutes of inactivity
- **Storage**: 1GB persistent disk

### **Performance Optimization**

#### **For Better Performance**
1. **Enable Auto-Deploy**: Automatically deploys on git push
2. **Health Checks**: Configured at `/health` endpoint
3. **Database**: SQLite for simplicity (persistent across deployments)

#### **Scaling Considerations**
- **Free Tier**: Perfect for personal use and small groups
- **Paid Plans**: Available if you need more resources
- **Custom Domain**: Can be added to any plan

---

## 🆓 Free AI Configuration

### **Default Setup (Always Works)**
The deployment uses the **Enhanced Local AI** model by default:
- ✅ **No API keys required**
- ✅ **Works immediately**
- ✅ **Student-focused responses**
- ✅ **No internet dependency**

### **Optional Enhancements**

#### **HuggingFace Free (Better Quality)**
1. **Get Free Token**:
   - Go to [HuggingFace](https://huggingface.co/)
   - Create free account
   - Get your API token

2. **Add to Render**:
   - Go to your service dashboard
   - Environment → Environment Variables
   - Add: `HUGGINGFACE_TOKEN` = `your-token`

3. **Update Model**:
   - Change `DEFAULT_AI_MODEL` to `huggingface-free`

#### **Custom Domain (Optional)**
1. **Add Custom Domain** in Render dashboard
2. **Update Environment Variables**:
   - `REACT_APP_BACKEND_URL` = `https://your-domain.com`

---

## 🔍 Troubleshooting

### **Build Issues**

#### **"Build Failed"**
```bash
# Check build logs in Render dashboard
# Common issues:
# 1. Missing files in repository
# 2. Docker build errors
# 3. Environment variable issues
```

#### **"Service Won't Start"**
```bash
# Check runtime logs
# Common issues:
# 1. Port configuration
# 2. Database migration errors
# 3. Missing dependencies
```

### **Runtime Issues**

#### **"Health Check Failed"**
- Check if `/health` endpoint is working
- Verify backend is starting correctly
- Check database migrations

#### **"AI Not Responding"**
- Default model should always work
- Check if HuggingFace token is valid (if using)
- Verify environment variables

### **Performance Issues**

#### **"Slow Responses"**
- Free tier has limitations
- Consider upgrading to paid plan
- Optimize for local AI model

#### **"Service Sleeping"**
- Free tier services sleep after 15 minutes
- First request after sleep takes 30-60 seconds
- Consider paid plan for always-on service

---

## 📊 Monitoring

### **Render Dashboard**
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, request count
- **Deployments**: Build and deployment history
- **Environment**: Variable management

### **Health Checks**
- **Endpoint**: `/health`
- **Frequency**: Every 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3 attempts

---

## 🔄 Updates and Maintenance

### **Automatic Deployments**
- **Enabled by default**
- **Deploys on git push to main branch**
- **Can be disabled in dashboard**

### **Manual Deployments**
1. **Go to Render dashboard**
2. **Select your service**
3. **Click "Manual Deploy"**
4. **Choose branch/commit**

### **Rollback**
1. **Go to Deployments tab**
2. **Find previous deployment**
3. **Click "Promote"**

---

## 🎯 Production Checklist

### **Before Going Live**
- ✅ **Update JWT_SECRET_KEY** to a secure value
- ✅ **Test all AI models** work correctly
- ✅ **Verify database migrations** run successfully
- ✅ **Check health endpoint** responds correctly
- ✅ **Test user registration/login**
- ✅ **Verify document upload** functionality

### **Security Considerations**
- ✅ **HTTPS enabled** (automatic on Render)
- ✅ **Environment variables** properly set
- ✅ **Database** using secure configuration
- ✅ **CORS** configured correctly

---

## 🆓 Cost Breakdown

### **Free Tier (Perfect for Students)**
- **Deployment**: $0/month
- **Hosting**: $0/month
- **Domain**: $0/month (render.com subdomain)
- **SSL Certificate**: $0/month (automatic)
- **AI Models**: $0/month (all free options)

### **Optional Paid Features**
- **Custom Domain**: $5/month
- **Always-On Service**: $7/month
- **More Resources**: $25+/month

---

## 🚀 Your App is Live!

### **Access Your App**
- **URL**: `https://your-app-name.onrender.com`
- **Health Check**: `https://your-app-name.onrender.com/health`
- **API**: `https://your-app-name.onrender.com/api/`

### **Share with Students**
- **No registration required** for basic use
- **Free for everyone**
- **Works on any device**
- **No installation needed**

---

## 🎓 Perfect for Educational Use

### **For Students**
- **Completely free**
- **No registration required**
- **Works immediately**
- **Student-focused AI**

### **For Teachers**
- **Share with your class**
- **No setup required**
- **Always available**
- **Privacy-focused**

### **For Schools**
- **Deploy for your institution**
- **Custom branding possible**
- **Scalable solution**
- **Cost-effective**

---

**🎯 Your free AI study assistant is now live and helping students everywhere!**

**Next Steps:**
1. **Test the deployment**
2. **Share with students**
3. **Monitor usage**
4. **Gather feedback**

**Remember**: This is completely free and designed specifically for students! 🎓✨ 