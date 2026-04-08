# 🚀 Render.com Deployment Guide

**Deployment Status**: ✅ Ready to Deploy

## Quick Start (5 minutes)

### 1. Create Render Account
- Go to https://render.com
- Click **"Sign up"**
- Use your GitHub account to sign up (fastest way)

### 2. Create Web Service
- Click **"New"** → **"Web Service"**
- Select **"Deploy an existing repo"**
- Click **"Connect a repository"**

### 3. Select Your Repository
- Search for: **`SchoolManagementSystem`**
- Click **"Connect"**

### 4. Configure Service
Fill in these details:

| Field | Value |
|-------|-------|
| **Name** | `school-management-system` |
| **Environment** | `Python 3` |
| **Region** | Choose closest to you (e.g., US East) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn school_management.wsgi --bind 0.0.0.0:$PORT --timeout 120` |

### 5. Add Environment Variables
Click **"Add Environment Variable"** and add these one by one:

```
DEBUG=false
SECRET_KEY=<GENERATE_NEW_ONE_BELOW>
ALLOWED_HOSTS=school-management-system.onrender.com
```

#### Generate a New SECRET_KEY
Run this in your terminal:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Or use this pre-generated one:**
```
=5^qdrpll$2np+4les0$g*l!9=_sk5adh-u^!)vd50u)^uqsrm
```

### 6. Create Database (Optional but Recommended)
At the bottom of the page:
- Check **"Add a database"**
- Select **"PostgreSQL"**
- This will automatically add `DATABASE_URL` to your environment

### 7. Deploy!
- Click **"Create Web Service"**
- Render will start building your app
- **First deployment: 5-10 minutes**
- Subsequent deployments: 1-2 minutes

---

## ✅ Pre-Deployment Checklist

Your project has been verified for:
- ✅ `Procfile` - Configured correctly
- ✅ `render.yaml` - Deployment config ready
- ✅ `requirements.txt` - All dependencies listed
- ✅ `runtime.txt` - Python version specified (3.14.0)
- ✅ `settings.py` - Production-ready configuration
- ✅ WhiteNoise middleware - Static files configured
- ✅ ALLOWED_HOSTS - Set to accept all hosts (`*`)
- ✅ DEBUG mode - Can be toggled via environment variable

---

## 📊 What Happens During Deployment

1. **Build Phase** (2-3 minutes)
   - Install Python 3.14.0
   - Download and install all packages from requirements.txt
   - Collect static files
   - Compress and optimize assets

2. **Configuration Phase**
   - Apply environment variables
   - Run database migrations (if using PostgreSQL)
   - Create superuser (optional)

3. **Launch Phase**
   - Start Gunicorn server
   - Your app goes live!

---

## 🔑 Important Environment Variables

### Required:
- **`DEBUG`**: Set to `false` for production
- **`SECRET_KEY`**: Keep it secret! Generate a new one
- **`ALLOWED_HOSTS`**: Your Render domain

### Optional:
- **`DATABASE_URL`**: Auto-set if you add PostgreSQL database
- **`EMAIL_*`**: If you want to send emails from your app
- **`AWS_*`**: If you want to use S3 for media files

---

## 🌐 Your Live URL

After deployment, your app will be available at:
```
https://school-management-system.onrender.com
```

(or whatever name you choose in step 4)

---

## 🔄 Auto-Deployment

Once deployed:
- **Every push to GitHub** → Automatic redeploy
- **Build logs** visible in Render dashboard
- **Logs** available for debugging

---

## 🆘 Troubleshooting

### If deployment fails:
1. Check build logs in Render dashboard
2. Look for error messages
3. Common issues:
   - Missing environment variables
   - Database connection errors
   - Static files not collected

### Check Logs:
```
In Render dashboard:
- Click "Logs" tab
- Check Build Logs and Runtime Logs
- Look for error messages
```

---

## 📱 Access Your App

**Admin Panel**: 
```
https://school-management-system.onrender.com/admin
```

**Default superuser** (if created):
```
Username: admin
Password: admin123 (CHANGE THIS!)
```

---

## 💰 Costs

- **Free tier**: 
  - 0.50 CPU hours/month
  - 0.5 GB RAM
  - PostgreSQL database (free)
  - Suitable for learning/testing

- **Paid tiers**: Starting from $7/month for more resources

---

## 🎯 Next Steps After Deployment

1. ✅ Visit your deployed app
2. ✅ Change admin password
3. ✅ Test all features
4. ✅ Configure email (optional)
5. ✅ Add custom domain (optional)
6. ✅ Monitor logs and performance

---

**Your app is ready to go! 🎉**

Sumit, your School Management System will be live on Render in just a few clicks!
