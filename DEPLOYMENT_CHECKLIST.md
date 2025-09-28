# 🚀 RareVault Deployment Checklist

## Pre-Deployment Checklist

### ✅ System Requirements
- [ ] Node.js 16+ installed
- [ ] Python 3.8+ installed  
- [ ] MySQL 8.0+ installed and running
- [ ] Git installed (optional)
- [ ] At least 4GB RAM available
- [ ] At least 2GB disk space available

### ✅ Database Setup
- [ ] MySQL server is running
- [ ] Database `rarevault_db` created
- [ ] Database schema imported from `complete_database_schema.sql`
- [ ] Database user created (if not using root)
- [ ] Database connection tested

### ✅ Backend Configuration
- [ ] Virtual environment created
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with correct database credentials
- [ ] JWT secret key configured
- [ ] Upload directories created (`uploads/items`, `uploads/ratings`, `uploads/users`)
- [ ] Backend server starts without errors (`python run.py`)
- [ ] API endpoints accessible at `http://localhost:5000`

### ✅ Frontend Configuration
- [ ] Node.js dependencies installed (`npm install`)
- [ ] Frontend environment configured (if needed)
- [ ] Frontend development server starts (`npm run dev`)
- [ ] Frontend accessible at `http://localhost:5173`
- [ ] API calls connecting to backend successfully

### ✅ Integration Testing
- [ ] User registration works
- [ ] User login works
- [ ] Marketplace displays items
- [ ] Image uploads work
- [ ] Order placement works
- [ ] Seller dashboard accessible
- [ ] Admin panel accessible
- [ ] Real-time messaging works
- [ ] Wishlist functionality works

## Production Deployment Additional Steps

### 🔒 Security
- [ ] Change default JWT secret keys
- [ ] Set `FLASK_ENV=production`
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper database user permissions
- [ ] Configure firewall rules
- [ ] Enable CORS for production domains only

### 🏗️ Build Process
- [ ] Frontend production build (`npm run build`)
- [ ] Static files served correctly
- [ ] API URLs updated for production
- [ ] Environment variables set for production

### 🚀 Server Configuration
- [ ] Web server configured (Apache/Nginx)
- [ ] Python WSGI server configured (Gunicorn/uWSGI)
- [ ] Process management configured (systemd/supervisor)
- [ ] Log rotation configured
- [ ] Backup strategy implemented

### 📊 Monitoring
- [ ] Error logging configured
- [ ] Performance monitoring set up
- [ ] Database backup scheduled
- [ ] Health check endpoints working
- [ ] Monitoring alerts configured

## Quick Test Commands

### Test Database Connection
```bash
mysql -u root -p -e "USE rarevault_db; SHOW TABLES;"
```

### Test Backend API
```bash
curl http://localhost:5000/api/health
```

### Test Frontend Build
```bash
cd frontend && npm run build
```

### Test Complete Flow
1. Register new user
2. Login with credentials
3. Browse marketplace
4. Add item to wishlist
5. Place an order
6. Check seller dashboard
7. Verify admin panel access

## Troubleshooting

### Backend Won't Start
- Check MySQL is running
- Verify `.env` file exists and has correct credentials
- Ensure virtual environment is activated
- Check `python run.py` error messages

### Frontend Won't Start
- Run `npm install` to ensure dependencies are installed
- Check if port 5173 is available
- Verify Node.js version compatibility

### Database Connection Issues
- Test MySQL connection manually
- Check database name, username, and password
- Ensure database exists and schema is imported

### Images Not Loading
- Check upload directories exist and have write permissions
- Verify image paths in database
- Check file upload limits in Flask configuration

## Support

If you encounter issues:
1. Check this checklist first
2. Review error logs in terminal
3. Check browser console for frontend errors
4. Verify all services are running
5. Consult SETUP_GUIDE.md for detailed instructions

---

**Last Updated**: September 2025