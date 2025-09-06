"""
Database Schema Inspector
This script will connect to your database and show you the exact structure,
then generate the correct SQLAlchemy model based on your actual database.
"""

import pymysql
import sys
from datetime import datetime

# Database connection settings
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL user
    'password': 'password',  # Change this to your MySQL password
    'database': 'rarevault_db',
    'charset': 'utf8mb4'
}

def check_database_structure():
    try:
        # Connect to database
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("="*60)
        print("DATABASE STRUCTURE INSPECTION")
        print("="*60)
        
        # 1. Show all tables
        print("\n1. TABLES IN DATABASE:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            print(f"   - {table[0]}")
        
        # 2. Check items table structure
        print("\n2. ITEMS TABLE STRUCTURE:")
        cursor.execute("DESCRIBE items")
        items_columns = cursor.fetchall()
        
        print("   Column Name        | Type           | Null | Key | Default | Extra")
        print("   " + "-"*70)
        for col in items_columns:
            print(f"   {col[0]:<18} | {col[1]:<14} | {col[2]:<4} | {col[3]:<3} | {str(col[4]):<7} | {col[5]}")
        
        # 3. Check users table structure
        print("\n3. USERS TABLE STRUCTURE:")
        cursor.execute("DESCRIBE users")
        users_columns = cursor.fetchall()
        
        print("   Column Name        | Type           | Null | Key | Default | Extra")
        print("   " + "-"*70)
        for col in users_columns:
            print(f"   {col[0]:<18} | {col[1]:<14} | {col[2]:<4} | {col[3]:<3} | {str(col[4]):<7} | {col[5]}")
        
        # 4. Generate correct Item model
        print("\n4. SUGGESTED ITEM MODEL BASED ON YOUR DATABASE:")
        print("="*60)
        
        model_code = generate_item_model(items_columns)
        print(model_code)
        
        # 5. Check for data
        print("\n5. DATA IN TABLES:")
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM items")
        item_count = cursor.fetchone()[0]
        
        print(f"   Users: {user_count} records")
        print(f"   Items: {item_count} records")
        
        # 6. Show sample users
        if user_count > 0:
            print("\n6. SAMPLE USERS:")
            cursor.execute("SELECT id, username, email, role FROM users LIMIT 3")
            users = cursor.fetchall()
            for user in users:
                print(f"   ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("\nPlease check your database connection settings in the script.")
        return False
    
    return True

def generate_item_model(columns):
    """Generate SQLAlchemy model based on actual database columns"""
    
    model = """class Item(db.Model):
    __tablename__ = 'items'
    
"""
    
    for col in columns:
        col_name = col[0]
        col_type = col[1].lower()
        is_nullable = col[2] == 'YES'
        is_primary = col[3] == 'PRI'
        default_val = col[4]
        
        # Map MySQL types to SQLAlchemy types
        if 'int' in col_type:
            if is_primary:
                model += f"    {col_name} = db.Column(db.Integer, primary_key=True)\n"
            else:
                nullable_str = f", nullable={not is_nullable}" if not is_nullable else ""
                model += f"    {col_name} = db.Column(db.Integer{nullable_str})\n"
        elif 'varchar' in col_type or 'char' in col_type:
            length = col_type.split('(')[1].split(')')[0] if '(' in col_type else '255'
            nullable_str = f", nullable={not is_nullable}" if not is_nullable else ""
            model += f"    {col_name} = db.Column(db.String({length}){nullable_str})\n"
        elif 'text' in col_type:
            model += f"    {col_name} = db.Column(db.Text)\n"
        elif 'decimal' in col_type:
            model += f"    {col_name} = db.Column(db.Numeric(10, 2))\n"
        elif 'timestamp' in col_type or 'datetime' in col_type:
            if 'created_at' in col_name:
                model += f"    {col_name} = db.Column(db.DateTime, default=datetime.utcnow)\n"
            elif 'updated_at' in col_name:
                model += f"    {col_name} = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)\n"
            else:
                model += f"    {col_name} = db.Column(db.DateTime)\n"
        elif 'enum' in col_type:
            model += f"    {col_name} = db.Column(db.String(50))  # ENUM in database\n"
        elif 'json' in col_type:
            model += f"    {col_name} = db.Column(db.JSON)\n"
        else:
            model += f"    {col_name} = db.Column(db.String(255))  # {col_type}\n"
    
    model += """
    seller = db.relationship('User', backref=db.backref('items', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': float(self.price) if self.price else None,
            'condition': getattr(self, 'condition', None),  # Handle different column names
            'year': self.year,
            'image_url': getattr(self, 'image_url', ''),
            'seller_id': self.seller_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
"""
    
    return model

if __name__ == "__main__":
    print("Checking database structure...")
    print("Make sure your database is running and the connection settings are correct.")
    print()
    
    success = check_database_structure()
    
    if success:
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("1. Copy the suggested model code above")
        print("2. Replace your current Item model with this code")
        print("3. Update your seller routes to match the actual column names")
        print("="*60)
    else:
        print("\nFailed to connect to database. Please check:")
        print("1. MySQL server is running")
        print("2. Database 'rarevault_db' exists")
        print("3. Connection credentials are correct")
        print("4. Required Python packages are installed: pip install pymysql")
