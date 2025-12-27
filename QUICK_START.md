# Quick Start Guide

Follow these steps to get the IT Support Ticket System up and running quickly.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note for Windows users:** If you encounter issues installing `mysqlclient`, you may need to:
1. Install MySQL Connector/C from MySQL website
2. Or use `pip install mysqlclient` with pre-built wheels
3. Alternative: Use `pymysql` (modify settings.py to use pymysql instead)

## Step 2: Create MySQL Database

Run the SQL script or manually create the database:

```sql
CREATE DATABASE ticket_system_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or use the provided script:
```bash
mysql -u root -p < setup_database.sql
```

## Step 3: Configure Database

Edit `ticket_system/settings.py` and update database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ticket_system_db',
        'USER': 'root',           # Change this
        'PASSWORD': '',            # Change this
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 5: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

## Step 6: Create Test Users (Optional)

You can create users via Django admin panel or use the registration page:

1. Go to http://127.0.0.1:8000/register/
2. Register as an employee
3. Login to admin panel (http://127.0.0.1:8000/admin/)
4. Change user role to 'IT Staff' or 'Administrator' as needed

## Step 7: Run the Server

```bash
python manage.py runserver
```

## Step 8: Access the Application

- **Web Interface**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Base URL**: http://127.0.0.1:8000/api/

## Testing the System

### As Employee:
1. Register/Login as employee
2. Create a new ticket
3. View your tickets
4. Add comments to your tickets

### As IT Staff:
1. Login as IT staff (change role in admin panel)
2. View all unassigned tickets
3. Assign tickets to yourself
4. Update ticket status
5. Add comments

### As Admin:
1. Login as admin
2. View all tickets
3. Manage users
4. Delete tickets
5. Full system access

## Common Issues

### Issue: `mysqlclient` installation fails
**Solution**: Use `pymysql` as alternative:
```bash
pip install pymysql
```

Then add to `ticket_system/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Issue: Database connection error
**Solution**: 
- Check MySQL is running
- Verify database credentials in settings.py
- Ensure database exists

### Issue: Migration errors
**Solution**:
```bash
python manage.py makemigrations tickets
python manage.py migrate
```

### Issue: Static files not loading
**Solution**:
```bash
python manage.py collectstatic
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [POSTMAN_API_GUIDE.md](POSTMAN_API_GUIDE.md) for API testing
- Explore the admin panel to manage users and tickets
- Test different user roles and permissions

## Default Credentials

After creating a superuser, you can:
- Login to admin panel
- Create additional users
- Change user roles
- Manage all tickets

Enjoy using the IT Support Ticket Management System! 🎉

