# MySQL Database Setup Script

# Create the database and user
CREATE DATABASE rarevault_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create user (replace 'your_password' with a strong password)
CREATE USER 'rarevault_user'@'localhost' IDENTIFIED BY 'your_password';

# Grant privileges
GRANT ALL PRIVILEGES ON rarevault_db.* TO 'rarevault_user'@'localhost';

# Refresh privileges
FLUSH PRIVILEGES;

# Use the database
USE rarevault_db;

# Show that it's ready
SHOW TABLES;
