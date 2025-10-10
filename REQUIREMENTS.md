# 📋 System Requirements & Dependencies

## System Requirements

### Operating System
- **Windows**: 10 or 11 (64-bit)
- **macOS**: 10.15 (Catalina) or later
- **Linux**: Ubuntu 20.04+ or equivalent

### Hardware Minimum
- **CPU**: Dual-core processor (2 GHz or faster)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 2 GB free space (1 GB for dependencies + 1 GB for data)
- **Display**: 1280x720 or higher resolution

---

## Required Software

### 1. Python 3.10 or Higher
- **Download**: https://www.python.org/downloads/
- **Version Check**: `python --version` or `python3 --version`
- **Installation Notes**: 
  - Windows: Check "Add Python to PATH" during installation
  - Mac: May need to use `python3` command
  - Linux: Usually pre-installed, or use `sudo apt install python3 python3-pip`

### 2. Node.js 16.x or Higher (LTS Recommended)
- **Download**: https://nodejs.org/
- **Version Check**: `node --version`
- **Installation Notes**: 
  - Includes npm (Node Package Manager)
  - LTS (Long Term Support) version recommended
  - Current version tested: Node.js 18.x

### 3. MySQL 8.0 or Higher

#### Option A: MySQL Server
- **Download**: https://dev.mysql.com/downloads/installer/
- **Version Check**: `mysql --version`
- **Installation Notes**:
  - Remember your root password
  - Default port: 3306
  - Enable MySQL service to start on boot

#### Option B: XAMPP (Recommended for Beginners)
- **Download**: https://www.apachefriends.org/
- **Includes**: MySQL + phpMyAdmin GUI
- **Installation Notes**:
  - Easier to manage with control panel
  - No password by default (or set during setup)
  - Use XAMPP Control Panel to start/stop MySQL

### 4. Web Browser
- **Chrome** (Recommended) - Version 90+
- **Firefox** - Version 88+
- **Edge** - Version 90+
- **Safari** - Version 14+ (macOS only)

---

## Python Dependencies (Backend)

These are automatically installed via `pip install -r requirements.txt`:

### Core Framework
- **Flask 2.3.3** - Web framework
- **Werkzeug 2.3.7** - WSGI utilities

### Database
- **Flask-SQLAlchemy 3.0.5** - ORM (Object-Relational Mapping)
- **PyMySQL 1.1.0** - MySQL database driver
- **cryptography 41.0.4** - Database encryption support

### Authentication & Security
- **Flask-JWT-Extended 4.5.3** - JWT token authentication
- **bcrypt 4.0.1** - Password hashing

### Utilities
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing
- **python-dotenv 1.0.0** - Environment variable management
- **pytz 2023.3** - Timezone handling

### Installation Command:
```bash
pip install -r backend/requirements.txt
```

### File Size: ~50-70 MB installed

---

## Node.js Dependencies (Frontend)

These are automatically installed via `npm install`:

### Core Framework
- **vue 3.4.0** - Progressive JavaScript framework
- **vue-router 4.2.5** - Official router for Vue.js
- **pinia 2.1.7** - State management

### HTTP & Data
- **axios 1.6.0** - HTTP client for API calls

### UI Libraries
- **leaflet 1.9.4** - Interactive maps (if used)

### Build Tools
- **vite 5.0.0** - Fast build tool and dev server
- **@vitejs/plugin-vue 4.5.0** - Vue plugin for Vite

### Development Dependencies
- **sass-embedded 1.93.2** - CSS preprocessor

### Installation Command:
```bash
npm install
```

### File Size: ~200-300 MB installed (in node_modules)

---

## Database Schema

### Database: `rarevault_db`
- **Engine**: MySQL 8.0+
- **Character Set**: utf8mb4
- **Collation**: utf8mb4_unicode_ci

### Tables:
1. **users** - User accounts (buyers, sellers, admins)
2. **items** - Product listings
3. **item_images** - Product images
4. **orders** - Purchase orders
5. **messages** - User messaging
6. **notifications** - System notifications
7. **seller_notifications** - Seller-specific notifications
8. **reviews** / **ratings** - Product reviews

### Import File:
```bash
rarevault_db.sql (~100-500 KB depending on data)
```

---

## Network Ports

The application uses the following ports:

### Backend (Flask)
- **Port**: 5000
- **URL**: http://localhost:5000
- **Protocol**: HTTP
- **Usage**: REST API endpoints

### Frontend (Vite Dev Server)
- **Port**: 3001
- **URL**: http://localhost:3001
- **Protocol**: HTTP
- **Usage**: Vue.js application

### Database (MySQL)
- **Port**: 3306 (default)
- **Protocol**: TCP
- **Usage**: Database connections

### Firewall Notes:
- No inbound firewall rules needed for local development
- All connections are localhost only

---

## Development Tools (Optional but Recommended)

### Code Editors
- **VS Code** (Recommended) - https://code.visualstudio.com/
  - Extensions: Python, Vue - Official, Vetur
- **PyCharm** - https://www.jetbrains.com/pycharm/
- **Sublime Text** - https://www.sublimetext.com/

### Database Management
- **MySQL Workbench** - https://www.mysql.com/products/workbench/
- **phpMyAdmin** - Included with XAMPP
- **DBeaver** - https://dbeaver.io/
- **HeidiSQL** - https://www.heidisql.com/ (Windows)

### API Testing
- **Postman** - https://www.postman.com/
- **Insomnia** - https://insomnia.rest/
- **Thunder Client** - VS Code extension

### Version Control
- **Git** - https://git-scm.com/
- **GitHub Desktop** - https://desktop.github.com/

---

## Disk Space Requirements

### Installation:
- Python + venv: ~200 MB
- Node.js + npm: ~100 MB
- MySQL Server: ~500 MB
- Project dependencies:
  - Python packages: ~70 MB
  - Node modules: ~300 MB
- **Total**: ~1.2 GB

### Runtime:
- Database: 100-500 MB (grows with data)
- Uploaded images: 50-500 MB (grows with usage)
- Logs: 10-100 MB
- **Total**: ~2-3 GB recommended

---

## Internet Connection

### During Setup:
- Required for downloading dependencies
- Bandwidth needed: ~500 MB total downloads
- Time: 10-20 minutes depending on connection speed

### During Runtime:
- **Not required** - application runs entirely locally
- Frontend connects to backend via localhost
- Backend connects to database via localhost
- No external API calls (unless explicitly added)

---

## Performance Considerations

### Backend Performance:
- **Response Time**: < 100ms for most API calls
- **Concurrent Users**: 10-20 (development mode)
- **Database Queries**: Optimized with indexes

### Frontend Performance:
- **Initial Load**: 1-3 seconds
- **Page Transitions**: < 500ms
- **Hot Module Reload**: 200-500ms (development)

### Optimization Tips:
- Use SSD for better database performance
- Close unnecessary applications during development
- Increase RAM allocation if running multiple services

---

## Browser Compatibility

### Tested Browsers:
- ✅ Chrome 90+ (Recommended)
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+ (macOS)

### Required Browser Features:
- ES6+ JavaScript support
- CSS Grid and Flexbox
- Fetch API
- Local Storage
- Async/Await

### Not Supported:
- Internet Explorer (any version)
- Very old browser versions (pre-2020)

---

## Environment Variables

### Backend (.env file):
```properties
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://root:password@localhost/rarevault_db
JWT_SECRET_KEY=jwt-secret-string
JWT_ACCESS_TOKEN_EXPIRES=3600
FLASK_ENV=development
FLASK_DEBUG=True
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Configuration Notes:
- All sensitive values in `.env` file
- Never commit `.env` to version control
- Use `.env.example` as template

---

## Security Considerations

### Development Mode:
- Debug mode enabled
- CORS allows all origins
- Detailed error messages
- No HTTPS required

### Production Notes:
When deploying to production:
- Disable debug mode
- Set specific CORS origins
- Use HTTPS
- Use strong secret keys
- Enable rate limiting
- Use production database server

---

## Troubleshooting Commands

### Check Versions:
```bash
python --version          # Python version
node --version           # Node.js version
npm --version            # npm version
mysql --version          # MySQL version
```

### Check Ports:
```bash
# Windows
netstat -an | findstr :5000
netstat -an | findstr :3001
netstat -an | findstr :3306

# Mac/Linux
lsof -i :5000
lsof -i :3001
lsof -i :3306
```

### Check Services:
```bash
# Windows - Check if MySQL is running
sc query MySQL80

# Mac - Check if MySQL is running
brew services list

# Linux - Check if MySQL is running
systemctl status mysql
```

---

## Summary Checklist

Before starting development, ensure:
- [ ] Python 3.10+ installed and in PATH
- [ ] Node.js 16+ installed
- [ ] MySQL 8.0+ installed and running
- [ ] 2+ GB free disk space
- [ ] Internet connection for initial setup
- [ ] Text editor or IDE installed
- [ ] Terminal/Command Prompt access

---

**All requirements met? You're ready to set up the project!**
**See SETUP_GUIDE.md for installation instructions.**
