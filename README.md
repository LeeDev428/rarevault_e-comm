# RareVault E-Commerce Platform

A full-stack e-commerce platform for vintage and rare items, built with Vue.js 3 and Flask.

## 📋 Table of Contents
- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Detailed Setup Instructions](#detailed-setup-instructions)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Required Software
1. **Python 3.10 or higher**
   - Download: https://www.python.org/downloads/
   - During installation, CHECK "Add Python to PATH"

2. **Node.js 16.x or higher**
   - Download: https://nodejs.org/ (LTS version recommended)
   - Includes npm (Node Package Manager)

3. **MySQL 8.0 or higher**
   - Download: https://dev.mysql.com/downloads/installer/
   - OR use XAMPP: https://www.apachefriends.org/
   - OR use WAMP: https://www.wampserver.com/

4. **Git** (optional, for version control)
   - Download: https://git-scm.com/downloads

### Operating System
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

---

## 🚀 Quick Start

### For First-Time Setup (Choose One Method)

#### Method 1: Automated Setup (Recommended)
```bash
# Navigate to project folder
cd rarevault

# Run the setup script
# On Windows PowerShell:
.\SETUP.ps1

# On Windows CMD or Git Bash:
bash SETUP.sh

# On macOS/Linux:
bash SETUP.sh
```

#### Method 2: Manual Setup
Follow the [Detailed Setup Instructions](#detailed-setup-instructions) below.

---

## 📚 Detailed Setup Instructions

### Step 1: Extract the Project
1. Extract the `rarevault` folder from Google Drive to your desired location
2. Example: `C:\Projects\rarevault` or `D:\Development\rarevault`

### Step 2: Install MySQL and Create Database

#### Option A: Using MySQL Server
1. Install MySQL Server from https://dev.mysql.com/downloads/installer/
2. During installation:
   - Remember your **root password**
   - Note the **port** (default: 3306)
3. Open MySQL Workbench or MySQL Command Line
4. Run the following command:
   ```sql
   CREATE DATABASE rarevault_db;
   ```
5. Import the database schema:
   ```sql
   mysql -u root -p rarevault_db < rarevault_db.sql
   ```
   OR in MySQL Workbench:
   - File → Run SQL Script
   - Select `rarevault_db.sql`
   - Execute

#### Option B: Using XAMPP
1. Install XAMPP from https://www.apachefriends.org/
2. Start the XAMPP Control Panel
3. Start **Apache** and **MySQL** services
4. Click **Admin** button next to MySQL (opens phpMyAdmin)
5. Create a new database named `rarevault_db`
6. Import `rarevault_db.sql`:
   - Click on `rarevault_db` database
   - Go to "Import" tab
   - Choose file: `rarevault_db.sql`
   - Click "Go"

### Step 3: Backend Setup (Flask/Python)

1. **Open Terminal/Command Prompt** and navigate to backend folder:
   ```bash
   cd rarevault/backend
   ```

2. **Create Python Virtual Environment**:
   ```bash
   # On Windows:
   python -m venv venv
   
   # On macOS/Linux:
   python3 -m venv venv
   ```

3. **Activate Virtual Environment**:
   ```bash
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   
   # On Windows CMD:
   venv\Scripts\activate.bat
   
   # On macOS/Linux:
   source venv/bin/activate
   ```
   
   You should see `(venv)` at the start of your command prompt.

4. **Install Python Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**:
   - Open the file `backend\.env` in a text editor
   - Update the following values:
   ```properties
   SECRET_KEY=your-secret-key-here-change-in-production
   DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost/rarevault_db
   JWT_SECRET_KEY=jwt-secret-string-change-in-production
   ```
   
   **Important**: Replace `YOUR_MYSQL_PASSWORD` with your actual MySQL root password
   
   Example:
   ```properties
   DATABASE_URL=mysql+pymysql://root:mypassword123@localhost/rarevault_db
   ```

6. **Test Database Connection**:
   ```bash
   python check_database.py
   ```
   This should show all database tables and confirm the connection works.

### Step 4: Frontend Setup (Vue.js)

1. **Open a NEW Terminal/Command Prompt** and navigate to frontend folder:
   ```bash
   cd rarevault/frontend
   ```

2. **Install Node.js Dependencies**:
   ```bash
   npm install
   ```
   
   This may take 2-5 minutes. You should see a `node_modules` folder created.

3. **Verify Installation**:
   ```bash
   npm list vue
   ```
   Should show Vue 3.4.0 or similar.

---

## ▶️ Running the Application

You need to run **BOTH** backend and frontend servers.

### Terminal 1: Start Backend Server

```bash
# Navigate to backend folder
cd rarevault/backend

# Activate virtual environment (if not already activated)
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Run the Flask server
python run.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
 * Running on http://YOUR_LOCAL_IP:5000
```

Keep this terminal **OPEN**. The backend is now running on http://localhost:5000

### Terminal 2: Start Frontend Server

```bash
# Navigate to frontend folder
cd rarevault/frontend

# Run the development server
npm run dev
```

**Expected Output:**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3001/
  ➜  Network: http://192.168.x.x:3001/
```

Keep this terminal **OPEN**. The frontend is now running on http://localhost:3001

### Access the Application

Open your web browser and go to:
```
http://localhost:3001
```

---

## 📁 Project Structure

```
rarevault/
├── backend/              # Flask Backend API
│   ├── app/
│   │   ├── models/      # Database models
│   │   ├── routes/      # API endpoints
│   │   ├── admin/       # Admin routes
│   │   ├── seller/      # Seller routes
│   │   └── user/        # User routes
│   ├── uploads/         # Uploaded images
│   ├── venv/           # Python virtual environment (created during setup)
│   ├── .env            # Environment variables (CONFIGURE THIS)
│   ├── requirements.txt # Python dependencies
│   └── run.py          # Backend entry point
│
├── frontend/           # Vue.js Frontend
│   ├── src/
│   │   ├── views/     # Page components
│   │   ├── components/# Reusable components
│   │   ├── router/    # Vue Router config
│   │   └── assets/    # Static assets
│   ├── node_modules/  # Node dependencies (created during setup)
│   ├── package.json   # Frontend dependencies
│   └── vite.config.js # Vite configuration
│
├── rarevault_db.sql   # Database schema and seed data
├── README.md          # This file
└── SETUP_GUIDE.md     # Detailed setup instructions
```

---

## 🔧 Troubleshooting

### Backend Issues

#### "ModuleNotFoundError: No module named 'flask'"
**Solution**: Make sure the virtual environment is activated and dependencies are installed:
```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

#### "Access denied for user 'root'@'localhost'"
**Solution**: Update your `backend\.env` file with the correct MySQL password:
```properties
DATABASE_URL=mysql+pymysql://root:YOUR_CORRECT_PASSWORD@localhost/rarevault_db
```

#### "Can't connect to MySQL server"
**Solution**: 
- Make sure MySQL service is running
- On Windows: Open Services (services.msc) and start "MySQL80" service
- With XAMPP: Open XAMPP Control Panel and start MySQL

#### "Port 5000 is already in use"
**Solution**: 
- Close any application using port 5000
- OR change the port in `backend/run.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
  ```

### Frontend Issues

#### "npm: command not found" or "'npm' is not recognized"
**Solution**: 
- Install Node.js from https://nodejs.org/
- Restart your terminal after installation
- Verify: `node --version` and `npm --version`

#### "ENOENT: no such file or directory"
**Solution**: Make sure you're in the correct directory:
```bash
cd rarevault/frontend
npm install
```

#### "Module not found" errors when running
**Solution**: Delete `node_modules` and reinstall:
```bash
rm -rf node_modules
npm install
```

#### Port 3001 is already in use
**Solution**: Kill the process or change the port in `frontend/vite.config.js`:
```javascript
server: {
  port: 3002,  // Changed to 3002
  // ... rest of config
}
```

### Database Issues

#### Cannot import SQL file
**Solution**:
1. Make sure the database exists: `CREATE DATABASE rarevault_db;`
2. Use the correct command:
   ```bash
   # From project root
   mysql -u root -p rarevault_db < rarevault_db.sql
   ```
3. Or use MySQL Workbench GUI: File → Run SQL Script

#### "Table doesn't exist" errors
**Solution**: Re-import the database:
```bash
mysql -u root -p
DROP DATABASE rarevault_db;
CREATE DATABASE rarevault_db;
exit

mysql -u root -p rarevault_db < rarevault_db.sql
```

---

## 🔐 Default Accounts

After importing the database, you may have default test accounts. Check the SQL file or create new accounts through the registration page.

---

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review error messages carefully
3. Check that all prerequisites are installed correctly
4. Verify MySQL is running and credentials are correct

---

## 🌟 Features

- **User Management**: Registration, login, profile management
- **Seller Dashboard**: List items, manage inventory, view analytics
- **Admin Panel**: User management, item moderation, system monitoring
- **Marketplace**: Browse items, search, filter, favorites
- **Messaging System**: Buyer-seller communication
- **Order Management**: Purchase flow, order tracking
- **Image Uploads**: Multiple images per item
- **Notifications**: Real-time updates for users and sellers

---

## 📝 License

Proprietary - All rights reserved
