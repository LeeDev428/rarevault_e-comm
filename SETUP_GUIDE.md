# RareVault E-Commerce Platform - Setup Guide

## Project Overview
RareVault is a full-stack e-commerce platform for vintage/rare items with the following features:
- User authentication and authorization
- Item marketplace with advanced search and filtering
- Order management system
- Seller dashboard for inventory management
- Real-time messaging between buyers and sellers
- Rating and review system
- Wishlist functionality
- Image upload and management

## Technology Stack
- **Frontend**: Vue.js 3 with Vite
- **Backend**: Python Flask with JWT authentication
- **Database**: MySQL 8.0+
- **File Storage**: Local file system for uploads
- **Package Managers**: npm (frontend), pip (backend)

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

### 1. Node.js and npm
- **Download**: https://nodejs.org/ (LTS version recommended)
- **Verify installation**:
  ```bash
  node --version
  npm --version
  ```

### 2. Python 3.8+
- **Download**: https://www.python.org/downloads/
- **Verify installation**:
  ```bash
  python --version
  # or
  python3 --version
  ```

### 3. MySQL 8.0+
- **Download**: https://dev.mysql.com/downloads/mysql/
- **Alternative**: Use XAMPP/WAMP which includes MySQL
- **Verify installation**: Access MySQL through command line or phpMyAdmin

### 4. Git (optional but recommended)
- **Download**: https://git-scm.com/downloads

---

## Project Setup Instructions

### Step 1: Download/Clone the Project
```bash
# If using Git
git clone [repository-url]
cd rarevault

# Or extract the zip file to your desired location
```

### Step 2: Database Setup

#### A. Create Database
1. Open MySQL command line or phpMyAdmin
2. Create a new database:
   ```sql
   CREATE DATABASE rarevault_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

#### B. Import Database Schema
1. Navigate to the project root directory
2. Import the complete schema:
   ```bash
   mysql -u root -p rarevault_db < complete_database_schema.sql
   ```
   Or use phpMyAdmin to import the `complete_database_schema.sql` file

#### C. Create Database User (Optional but recommended)
```sql
CREATE USER 'rarevault_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON rarevault_db.* TO 'rarevault_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 3: Backend Setup

#### A. Navigate to Backend Directory
```bash
cd backend
```

#### B. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### C. Install Dependencies
```bash
pip install -r requirements.txt
```

#### D. Configure Environment Variables
Create a `.env` file in the backend directory:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=rarevault_db
DB_USER=root
DB_PASSWORD=your_mysql_password

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

#### E. Create Upload Directories
```bash
mkdir -p uploads/items
mkdir -p uploads/ratings
mkdir -p uploads/users
```

### Step 4: Frontend Setup

#### A. Navigate to Frontend Directory
```bash
cd ../frontend
```

#### B. Install Dependencies
```bash
npm install
```

#### C. Configure Environment (Optional)
Create a `.env` file in the frontend directory if you need custom API URLs:
```env
VITE_API_BASE_URL=http://localhost:5000
```

---

## Running the Application

### Step 1: Start the Backend Server
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already active)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start the Flask server
python run.py
```
The backend will run on: `http://localhost:5000`

### Step 2: Start the Frontend Development Server
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Start the Vite development server
npm run dev
```
The frontend will run on: `http://localhost:5173` (or another port if 5173 is busy)

### Step 3: Access the Application
- Open your browser and navigate to the frontend URL (usually `http://localhost:5173`)
- The application should now be fully functional

---

## Default Users and Testing

The database should include some default users for testing:
- **Admin User**: Check the database for admin credentials
- **Seller User**: Check the database for seller credentials
- **Regular User**: Check the database for regular user credentials

You can also register new users through the application interface.

---

## Project Structure

```
rarevault/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── admin/
│   │   ├── seller/
│   │   └── user/
│   ├── uploads/
│   ├── requirements.txt
│   ├── run.py
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── assets/
│   │   └── main.js
│   ├── package.json
│   ├── vite.config.js
│   └── .env
├── complete_database_schema.sql
└── README.md
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Issues
- **Error**: "Access denied for user"
  - **Solution**: Check MySQL credentials in `.env` file
  - Ensure MySQL server is running

#### 2. Port Already in Use
- **Error**: "Port 5000 already in use"
  - **Solution**: Kill the process using the port or change the port in the Flask app

#### 3. Node Module Issues
- **Error**: Module not found errors
  - **Solution**: Delete `node_modules` and run `npm install` again

#### 4. Python Package Issues
- **Error**: Module not found in Python
  - **Solution**: Ensure virtual environment is activated and run `pip install -r requirements.txt`

#### 5. Image Upload Issues
- **Error**: Images not displaying
  - **Solution**: Ensure upload directories exist and have proper permissions

#### 6. CORS Issues
- **Error**: CORS policy blocks requests
  - **Solution**: Check Flask-CORS configuration in the backend

### Getting Help
- Check browser console for frontend errors
- Check terminal/command prompt for backend errors
- Ensure both frontend and backend servers are running
- Verify database connection and schema

---

## Production Deployment Notes

For production deployment, consider:
1. Set `FLASK_ENV=production` in backend
2. Build frontend: `npm run build`
3. Configure proper web server (Apache, Nginx)
4. Set up SSL certificates
5. Configure production database
6. Set secure JWT secrets
7. Configure file upload limits and security

---

## System Requirements

**Minimum Requirements:**
- RAM: 4GB
- Storage: 2GB free space
- OS: Windows 10, macOS 10.14, or Linux Ubuntu 18.04+

**Recommended Requirements:**
- RAM: 8GB+
- Storage: 5GB+ free space
- Modern multi-core processor

---

## Support

If you encounter any issues during setup:
1. Check this guide first
2. Review error messages carefully
3. Ensure all prerequisites are properly installed
4. Check that all required services are running (MySQL, etc.)

---

**Last Updated**: September 2025
**Version**: 1.0.0