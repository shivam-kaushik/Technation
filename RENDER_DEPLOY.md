# 🚀 Deploy to Render.com - Step by Step

## ✅ Prerequisites (Already Done!)
- [x] Code pushed to GitHub
- [x] requirements.txt ready
- [x] render.yaml configuration created

## 📋 Deployment Steps

### Step 1: Sign Up / Sign In to Render
1. Go to **https://render.com/**
2. Click **"Get Started"** or **"Sign In"**
3. Choose **"Sign in with GitHub"**
4. Authorize Render to access your repositories

### Step 2: Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Find and select your repository: **`Technation`**
   - If you don't see it, click "Configure account" to grant access

### Step 3: Configure Your Service

Fill in these settings:

**Basic Settings:**
- **Name**: `technation-skill-passport` (or your choice)
- **Region**: Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
  
- **Start Command**:
  ```bash
  streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
  ```

**Instance Type:**
- Select **"Free"** ($0/month)
- 512 MB RAM, 0.1 CPU
- Sleeps after 15 minutes of inactivity
- Free SSL certificate included

### Step 4: Environment Variables (Important!)

Click **"Advanced"** and add these environment variables:

| Key | Value |
|-----|-------|
| `USE_TF` | `NO` |
| `TRANSFORMERS_NO_TF` | `1` |
| `PYTHON_VERSION` | `3.10.0` |

### Step 5: Deploy! 🎉
1. Click **"Create Web Service"**
2. Watch the build logs (will take 5-10 minutes)
3. Your app will be live at: `https://technation-skill-passport.onrender.com`

---

## 📊 What Happens During Deployment?

### Build Phase (5-8 minutes):
```
1. ✅ Cloning repository from GitHub
2. ✅ Setting up Python 3.10 environment
3. ✅ Installing dependencies from requirements.txt
4. ✅ Downloading ML models (sentence-transformers)
5. ✅ Building application
```

### Deploy Phase (1-2 minutes):
```
6. ✅ Starting Streamlit server
7. ✅ Configuring SSL certificate
8. ✅ Health checks passing
9. ✅ App is LIVE! 🎊
```

---

## 🎯 Your App URL

After deployment, your app will be available at:
```
https://technation-skill-passport.onrender.com
```

(Replace `technation-skill-passport` with whatever name you chose)

---

## ⚙️ Post-Deployment Configuration

### Custom Domain (Optional)
1. Go to your service dashboard
2. Click "Settings" → "Custom Domain"
3. Add your domain (e.g., `skills.yourdomain.com`)
4. Follow DNS configuration instructions
5. Free SSL certificate auto-generated!

### Auto-Deploy Settings
- **Enabled by default**: Pushes to `main` branch auto-deploy
- To disable: Settings → "Auto-Deploy" → Toggle off

### Health Checks
Render automatically monitors your app:
- HTTP health checks every 30 seconds
- Auto-restarts if app crashes
- Email notifications on failures

---

## 🔍 Monitoring Your App

### View Logs
1. Go to your service dashboard
2. Click "Logs" tab
3. See real-time application logs
4. Filter by time, search for errors

### View Metrics
1. Click "Metrics" tab
2. See:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

### Events
1. Click "Events" tab
2. See deployment history
3. Track when app goes to sleep/wakes

---

## ⚡ Important Notes

### Free Tier Limitations:
- ✅ 750 hours/month (always on if used daily)
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ Cold start takes ~30 seconds to wake up
- ✅ Automatic SSL certificates
- ✅ 100 GB bandwidth/month

### How Sleep Works:
- App sleeps after 15 min without requests
- First request wakes it up (~30 sec delay)
- Subsequent requests are instant
- Good for demos and MVPs!

### Keep App Awake (Optional):
Use a service like **UptimeRobot** or **cron-job.org**:
1. Sign up for free
2. Add your Render URL
3. Set to ping every 14 minutes
4. Your app stays awake 24/7!

---

## 🐛 Troubleshooting

### Build Fails
**Problem**: Dependencies won't install
**Solution**: 
- Check requirements.txt format
- Ensure all versions are compatible
- Check build logs for specific error

### App Won't Start
**Problem**: Application error after build
**Solution**:
- Check start command is correct
- Verify environment variables are set
- Check app logs for Python errors

### Slow to Load
**Problem**: App takes 30+ seconds to load
**Solution**:
- This is normal on free tier (cold start)
- Use UptimeRobot to keep app awake
- Consider upgrading to paid tier ($7/month)

### Out of Memory
**Problem**: App crashes with memory error
**Solution**:
- Free tier has 512MB RAM
- Consider upgrading to Starter plan (1GB RAM)
- Optimize model loading in code

---

## 📈 Upgrade Options (When You're Ready)

### Starter Plan - $7/month
- ✅ No sleeping!
- ✅ 1 GB RAM
- ✅ 0.5 CPU
- ✅ Always fast

### Standard Plan - $25/month
- ✅ 4 GB RAM
- ✅ 2 CPU
- ✅ Priority support
- ✅ More bandwidth

---

## 🔄 Update Your App

### Automatic Updates
1. Make changes locally
2. Commit: `git commit -am "Update feature"`
3. Push: `git push origin main`
4. Render auto-deploys! ✅

### Manual Deploy
1. Go to service dashboard
2. Click "Manual Deploy"
3. Select branch
4. Click "Deploy"

---

## 🎉 Next Steps After Deployment

1. **Test All Features**:
   - Upload CV
   - Analyze skills
   - Generate passport
   - Check equity features

2. **Share Your App**:
   - Post on LinkedIn
   - Share with potential users
   - Get feedback

3. **Monitor Usage**:
   - Check logs regularly
   - Monitor for errors
   - Track response times

4. **Iterate**:
   - Implement feedback
   - Add new features
   - Optimize performance

---

## 🆘 Need Help?

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com/
- **Status**: https://status.render.com/
- **Support**: help@render.com

---

## 💡 Pro Tips

### 1. Environment Variables
Store sensitive data (API keys, secrets) as environment variables, not in code

### 2. Monitoring
Set up health check notifications in Render settings

### 3. Logging
Use `st.logger` for better debugging in production

### 4. Performance
First load is slow (model download) - set expectations with users

### 5. Backups
Keep GitHub repo updated - it's your backup!

---

## ✅ Deployment Checklist

Before deploying, ensure:
- [x] Code pushed to GitHub
- [x] requirements.txt updated
- [x] render.yaml created
- [x] Environment variables ready
- [x] Start command tested locally

After deploying:
- [ ] Test all features on live URL
- [ ] Check logs for any errors
- [ ] Set up health monitoring
- [ ] Share URL with test users
- [ ] Monitor resource usage

---

## 🚀 You're Ready to Deploy!

Just follow the steps above and your app will be live in ~10 minutes!

**Your app will be at**: `https://[your-service-name].onrender.com`

Good luck! 🎊
