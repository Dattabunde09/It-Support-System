# Postman API Testing Guide

This guide explains how to test the IT Support Ticket System API using Postman.

## Prerequisites

1. The Django server must be running (`python manage.py runserver`)
2. You must have a user account (register via web interface or create via admin)
3. You need to obtain a session cookie from the web interface

## Getting Your Session Cookie

1. Open your browser and navigate to `http://127.0.0.1:8000/`
2. Login with your credentials
3. Open browser Developer Tools (F12)
4. Go to Application/Storage → Cookies
5. Copy the `sessionid` value

## Setting Up Postman

### Method 1: Using Session Cookie

1. Create a new Postman request
2. Go to the **Headers** tab
3. Add a header:
   - Key: `Cookie`
   - Value: `sessionid=your_session_id_here`

### Method 2: Using Postman's Cookie Manager

1. In Postman, click on the **Cookies** link (below Send button)
2. Enter domain: `127.0.0.1:8000`
3. Add cookie:
   - Name: `sessionid`
   - Value: `your_session_id_here`
   - Domain: `127.0.0.1`

## API Endpoints

### Base URL
```
http://127.0.0.1:8000/api/
```

### 1. List All Tickets
```
GET /api/tickets/
```
**Response:** List of tickets (filtered by user role)

### 2. Create a New Ticket
```
POST /api/tickets/
Content-Type: application/json

Body:
{
  "title": "Email server not responding",
  "description": "Unable to send emails through Outlook. Error message: 'Connection timeout'",
  "priority": "high"
}
```

**Priority values:** `low`, `medium`, `high`, `urgent`

### 3. Get Ticket Details
```
GET /api/tickets/{id}/
```
**Example:** `GET /api/tickets/1/`

### 4. Update Ticket
```
PUT /api/tickets/{id}/
Content-Type: application/json

Body:
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "urgent",
  "assigned_to": 2
}
```

**Partial Update:**
```
PATCH /api/tickets/{id}/
Content-Type: application/json

Body:
{
  "status": "resolved"
}
```

### 5. Delete Ticket (Admin Only)
```
DELETE /api/tickets/{id}/
```

### 6. Add Comment to Ticket
```
POST /api/tickets/{id}/add_comment/
Content-Type: application/json

Body:
{
  "content": "I've restarted the email service. Please try again."
}
```

### 7. Update Ticket Status
```
POST /api/tickets/{id}/update_status/
Content-Type: application/json

Body:
{
  "status": "in_progress"
}
```

**Status values:** `open`, `in_progress`, `resolved`, `closed`

### 8. Assign Ticket to IT Staff
```
POST /api/tickets/{id}/assign/
Content-Type: application/json

Body:
{
  "user_id": 2
}
```

### 9. List Comments
```
GET /api/comments/?ticket_id=1
```

### 10. Create Comment
```
POST /api/comments/
Content-Type: application/json

Body:
{
  "ticket_id": 1,
  "content": "This is a new comment"
}
```

## Example Postman Collection

You can create a Postman Collection with these requests. Here's a sample structure:

### Collection: IT Support Ticket System API

#### Folder: Tickets
- List Tickets (GET)
- Create Ticket (POST)
- Get Ticket (GET)
- Update Ticket (PUT)
- Partial Update Ticket (PATCH)
- Delete Ticket (DELETE)
- Add Comment (POST)
- Update Status (POST)
- Assign Ticket (POST)

#### Folder: Comments
- List Comments (GET)
- Create Comment (POST)
- Get Comment (GET)
- Update Comment (PUT)
- Delete Comment (DELETE)

## Testing Workflow

1. **Create a Ticket** (as Employee)
   ```
   POST /api/tickets/
   {
     "title": "Printer not working",
     "description": "The printer in room 205 is not printing",
     "priority": "medium"
   }
   ```

2. **View the Ticket** (as IT Staff)
   ```
   GET /api/tickets/1/
   ```

3. **Assign Ticket to Yourself** (as IT Staff)
   ```
   POST /api/tickets/1/assign/
   {
     "user_id": 2
   }
   ```

4. **Update Status to In Progress** (as IT Staff)
   ```
   POST /api/tickets/1/update_status/
   {
     "status": "in_progress"
   }
   ```

5. **Add a Comment** (as IT Staff)
   ```
   POST /api/tickets/1/add_comment/
   {
     "content": "I've checked the printer. It needs a new toner cartridge."
   }
   ```

6. **Update Status to Resolved** (as IT Staff)
   ```
   POST /api/tickets/1/update_status/
   {
     "status": "resolved"
   }
   ```

7. **Close the Ticket** (as IT Staff/Admin)
   ```
   POST /api/tickets/1/update_status/
   {
     "status": "closed"
   }
   ```

## Response Examples

### Successful Ticket Creation
```json
{
  "id": 1,
  "title": "Email server not responding",
  "description": "Unable to send emails",
  "status": "open",
  "priority": "high",
  "created_by": {
    "id": 1,
    "username": "employee1",
    "email": "employee1@example.com",
    "role": "employee"
  },
  "assigned_to": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "resolved_at": null,
  "closed_at": null,
  "comments": []
}
```

### Error Response
```json
{
  "error": "Permission denied"
}
```
or
```json
{
  "status": ["Invalid status"]
}
```

## Authentication Notes

- All endpoints require authentication
- Use session-based authentication (cookie)
- Different user roles see different tickets:
  - **Employee**: Only their own tickets
  - **IT Staff**: Assigned tickets + unassigned tickets
  - **Admin**: All tickets

## Troubleshooting

### 401 Unauthorized
- Check that your session cookie is valid
- Make sure you're logged in via web interface
- Session may have expired - login again

### 403 Forbidden
- Check user permissions/role
- Some actions require IT Staff or Admin role

### 404 Not Found
- Check that the ticket ID exists
- Verify the endpoint URL is correct

### 400 Bad Request
- Check request body format (must be valid JSON)
- Verify required fields are provided
- Check field values are valid (e.g., status, priority)

## Tips

1. **Save Environment Variables** in Postman:
   - `base_url`: `http://127.0.0.1:8000`
   - `session_id`: Your session cookie value

2. **Use Variables** in requests:
   - `{{base_url}}/api/tickets/`
   - `{{base_url}}/api/tickets/{{ticket_id}}/`

3. **Test Different Roles**: Create multiple user accounts with different roles to test permission levels

4. **Use Pre-request Scripts** to automatically set cookies or headers

