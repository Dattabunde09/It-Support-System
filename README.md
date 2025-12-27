# IT Support Ticket Management System

A full-stack IT Support Ticket Management System built with Django and MySQL that allows employees to create and track support tickets while enabling administrators and IT staff to assign, update, and manage requests.

## Features

- **Role-Based Authentication**: Three user roles (Employee, IT Staff, Administrator)
- **Ticket Lifecycle Management**: Complete workflow from Open → In-Progress → Resolved → Closed
- **Priority Levels**: Urgent, High, Medium, and Low priority classification
- **Comment-Based Communication**: Real-time communication through comments on tickets
- **Clean Dashboard UI**: Modern, responsive interface built with Bootstrap 5
- **Secure CRUD Operations**: Django ORM with proper permissions and validation
- **REST API Endpoints**: Full API support for Postman testing and integration
- **Advanced Filtering**: Search and filter tickets by status, priority, and keywords
- **Assignment System**: IT staff and admins can assign tickets to team members

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL
- **Frontend**: Django Templates, Bootstrap 5, JavaScript
- **API**: Django REST Framework
- **Authentication**: Django's built-in authentication system

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create MySQL Database**:
   ```sql
   CREATE DATABASE ticket_system_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **Configure Database Settings**:
   Edit `ticket_system/settings.py` and update the database credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'ticket_system_db',
           'USER': 'your_mysql_username',
           'PASSWORD': 'your_mysql_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

7. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create a Superuser** (Administrator):
   ```bash
   python manage.py createsuperuser
   ```

9. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

10. **Access the Application**:
    - Web Interface: http://127.0.0.1:8000/
    - Admin Panel: http://127.0.0.1:8000/admin/

## User Roles

### Employee
- Create new support tickets
- View and comment on their own tickets
- Track ticket status and updates

### IT Staff
- All Employee permissions
- View all unassigned tickets
- Assign tickets to themselves or other IT staff
- Update ticket status and priority
- Add comments to any ticket

### Administrator
- All IT Staff permissions
- View all tickets in the system
- Delete tickets
- Manage users through admin panel
- Full system access

## Ticket Workflow

1. **Open**: New ticket created by employee
2. **In Progress**: Ticket assigned and being worked on by IT staff
3. **Resolved**: Issue fixed, awaiting confirmation
4. **Closed**: Ticket confirmed resolved and archived

## API Endpoints

The system includes REST API endpoints for programmatic access. All endpoints require authentication.

### Base URL: `/api/`

### Ticket Endpoints

- `GET /api/tickets/` - List all tickets (filtered by user role)
- `POST /api/tickets/` - Create a new ticket
- `GET /api/tickets/{id}/` - Get ticket details
- `PUT /api/tickets/{id}/` - Update ticket (full update)
- `PATCH /api/tickets/{id}/` - Update ticket (partial update)
- `DELETE /api/tickets/{id}/` - Delete ticket (admin only)
- `POST /api/tickets/{id}/add_comment/` - Add comment to ticket
- `POST /api/tickets/{id}/update_status/` - Update ticket status
- `POST /api/tickets/{id}/assign/` - Assign ticket to IT staff

### Comment Endpoints

- `GET /api/comments/?ticket_id={id}` - Get comments for a ticket
- `POST /api/comments/` - Create a new comment
- `GET /api/comments/{id}/` - Get comment details
- `PUT /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment

### Example API Request (Postman)

**Create Ticket:**
```
POST http://127.0.0.1:8000/api/tickets/
Headers:
  Content-Type: application/json
  Cookie: sessionid=your_session_id

Body (JSON):
{
  "title": "Email server not responding",
  "description": "Unable to send emails through Outlook",
  "priority": "high"
}
```

**Update Ticket Status:**
```
POST http://127.0.0.1:8000/api/tickets/1/update_status/
Headers:
  Content-Type: application/json
  Cookie: sessionid=your_session_id

Body (JSON):
{
  "status": "in_progress"
}
```

## Project Structure

```
IT Support Ticket System/
├── manage.py
├── requirements.txt
├── README.md
├── ticket_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tickets/
│   ├── __init__.py
│   ├── models.py          # User, Ticket, Comment models
│   ├── views.py          # View functions
│   ├── urls.py           # URL routing
│   ├── forms.py          # Django forms
│   ├── admin.py          # Admin configuration
│   ├── serializers.py    # DRF serializers
│   ├── api_views.py      # API viewset
│   └── api_urls.py       # API URL routing
└── templates/
    ├── base.html
    └── tickets/
        ├── login.html
        ├── register.html
        ├── dashboard.html
        ├── ticket_list.html
        ├── ticket_create.html
        ├── ticket_detail.html
        ├── ticket_update.html
        └── ticket_delete.html
```

## Security Features

- Password hashing using Django's PBKDF2 algorithm
- CSRF protection on all forms
- Role-based access control
- SQL injection prevention via Django ORM
- Session-based authentication
- Secure password validation

## Testing with Postman

1. **Login via Web Interface** to get session cookie
2. **Import Postman Collection** (create manually):
   - Set base URL: `http://127.0.0.1:8000/api/`
   - Add session cookie from browser to Postman
3. **Test Endpoints**:
   - Create tickets
   - Update status
   - Add comments
   - Assign tickets

## Screenshots

The system includes:
- Modern dashboard with statistics
- Ticket listing with filters
- Detailed ticket view with comments
- Status update interface
- Priority and status badges

## Future Enhancements

- Email notifications for ticket updates
- File attachments for tickets
- Ticket categories and tags
- SLA tracking and reporting
- Advanced analytics dashboard
- Mobile responsive improvements

## License

This project is developed for educational and demonstration purposes.

## Support

For issues or questions, please create a ticket in the system itself! 😊

---

**Developed with ❤️ using Django and MySQL**

