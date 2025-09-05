# RareVault - Vintage Treasures & Antiques Platform

A full-stack web application for collectors and enthusiasts to buy, sell, and discover vintage treasures, antiques, and rare collectibles.

## 🎨 Features

- **Landing Page**: Beautifully designed home page matching the provided design
- **Authentication**: Login and registration with role-based access (User/Admin)
- **User Dashboard**: Personal dashboard for collectors to manage their listings
- **Admin Dashboard**: Administrative panel for user and platform management
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Clean Architecture**: Well-organized project structure with separation of concerns

## 🛠 Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **MySQL** - Database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Flask-CORS** - Cross-origin requests

### Frontend
- **Vue.js 3** - Progressive framework
- **Vue Router** - Client-side routing
- **Axios** - HTTP client
- **Vite** - Build tool
- **CSS3** - Custom styling with CSS variables

## 📁 Project Structure

```
rarevault-app/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── models.py          # Database models
│   │   ├── routes/
│   │   │   ├── auth.py            # Authentication routes
│   │   │   └── main.py            # Main API routes
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   │   └── routes.py          # Admin-specific routes
│   │   ├── user/
│   │   │   ├── __init__.py
│   │   │   └── routes.py          # User-specific routes
│   │   └── __init__.py            # Flask app factory
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables
│   └── run.py                     # Application entry point
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── Landing.vue        # Landing page
│   │   │   ├── Login.vue          # Login page
│   │   │   ├── Register.vue       # Registration page
│   │   │   ├── admin/
│   │   │   │   └── Dashboard.vue  # Admin dashboard
│   │   │   └── user/
│   │   │       └── Dashboard.vue  # User dashboard
│   │   ├── router/
│   │   │   └── index.js           # Vue Router configuration
│   │   ├── assets/
│   │   │   └── styles.css         # Global styles
│   │   ├── App.vue                # Root component
│   │   └── main.js                # Vue app entry point
│   ├── package.json               # Node.js dependencies
│   ├── vite.config.js             # Vite configuration
│   └── index.html                 # HTML template
└── README.md                      # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- MySQL 8.0 or higher
- Git

### Database Setup

1. **Create MySQL Database**
   ```sql
   CREATE DATABASE rarevault_db;
   CREATE USER 'rarevault_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON rarevault_db.* TO 'rarevault_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\\Scripts\\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   Update `.env` file with your database credentials:
   ```env
   SECRET_KEY=your-super-secret-key-here
   DATABASE_URL=mysql+pymysql://rarevault_user:your_password@localhost/rarevault_db
   JWT_SECRET_KEY=your-jwt-secret-key-here
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

   The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   The frontend will start on `http://localhost:3000`

## 🎯 Usage

### Account Types

1. **User/Collector Account**
   - Register as a seller/buyer
   - Add and manage item listings
   - Browse other collectors' items
   - Update profile information

2. **Admin Account**
   - Register as an admin
   - View platform statistics
   - Manage all users
   - Activate/deactivate user accounts
   - Monitor platform activity

### Key Features

1. **Landing Page**
   - Eye-catching hero section with call-to-action buttons
   - Feature highlights for the platform
   - Navigation to login/register

2. **Authentication**
   - Secure login/register forms
   - Social login buttons (UI only - ready for integration)
   - Role-based redirects after authentication

3. **User Dashboard**
   - Quick action cards for common tasks
   - Item management interface
   - Add new items with detailed forms
   - View and edit existing listings

4. **Admin Dashboard**
   - Platform statistics overview
   - User management table
   - User activation/deactivation controls
   - Real-time data updates

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `POST /api/auth/logout` - User logout

### User Routes
- `GET /api/user/dashboard` - User dashboard data
- `POST /api/user/items` - Create new item
- `PUT /api/user/items/:id` - Update item
- `DELETE /api/user/items/:id` - Delete item

### Admin Routes
- `GET /api/admin/dashboard` - Admin dashboard stats
- `GET /api/admin/users` - Get all users
- `PATCH /api/admin/users/:id/toggle-status` - Toggle user status

### Public Routes
- `GET /api/items` - Get all available items
- `GET /api/items/:id` - Get specific item

## 🎨 Design Features

### Landing Page
- Modern, clean design with vintage-inspired elements
- Responsive layout that works on all devices
- Beautiful typography using Playfair Display and Inter fonts
- Smooth animations and hover effects
- Professional gradient backgrounds

### Authentication Pages
- Clean, minimal forms with excellent UX
- Social login integration (UI ready)
- Form validation and error handling
- Consistent branding throughout

### Dashboard Interfaces
- Card-based layouts for easy scanning
- Intuitive navigation and actions
- Real-time data updates
- Mobile-responsive design
- Professional color scheme

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- SQL injection prevention through SQLAlchemy ORM
- Input validation and sanitization
- Role-based access control

## 🚀 Deployment

### Backend Deployment
1. Set up production database
2. Update environment variables for production
3. Use a production WSGI server like Gunicorn
4. Set up reverse proxy with Nginx

### Frontend Deployment
1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Deploy the `dist` folder to your web server
3. Configure routing for SPA

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 📞 Support

For support, please contact the development team or create an issue in the repository.

---

**RareVault** - Connecting collectors and preserving history, one treasure at a time. 🏺✨
