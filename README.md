# Social_Media

This project is a social networking application API built using Django Rest Framework (DRF). The API includes user authentication, search functionality, and friend request management.

## Features

1. **User Authentication:**

   - Signup with email (case insensitive).
   - Login with email and password (case insensitive).

2. **User Search:**

   - Search users by email or name (paginated, 10 records per page).
   - Exact email match returns the associated user.
   - Partial name match returns all matching users.

3. **Friend Management:**
   - Send, accept, and reject friend requests.
   - List of friends (accepted friend requests).
   - List of pending friend requests (received but not yet accepted/rejected).
   - Limit of 3 friend requests per minute per user.

## Installation Steps

### Prerequisites

- Docker
- Docker Compose
- Git

### Steps

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/kiranrokkam09/social_media.git
   cd social_media
   ```

2. **Build and Run Docker Containers:**

   ```sh
   docker-compose up --build
   ```

3. **Create a Superuser (optional):**
   To create an admin user for accessing the Django admin interface:
   ```sh
   docker-compose exec web python manage.py createsuperuser
   ```

## API Endpoints

### Authentication

- **Signup:**

  ```
  POST /signup
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```

- **Login:**
  ```
  POST /login
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```

### User Search

- **Search Users:**
  ```
  GET /search/?q=search_string
  ```

### Friend Management

- **Friend Suggestions:**

  ```
  GET /suggestions
  ```

- **Send Friend Request:**

  ```
  POST /sendrequest/id
  ```

- **Accept Friend Request:**

  ```
  PATCH /acceptrequest/id
  ```

- **Reject Friend Request:**

  ```
  DELETE /rejectrequest/id
  ```

- **List Friends:**

  ```
  GET /friends
  ```

- **List Pending Friend Requests:**
  ```
  GET /requests
  ```

## Postman Collection

The Postman collection link for testing all API endpoints is given Below.
[Postman Link](https://www.postman.com/satellite-observer-65859535/workspace/public/request/28828937-35f95da9-e095-4df1-adc5-d6e52fe48b5c)

## Requirements

See `requirements.txt` for a list of dependencies.

## Notes

- Ensure Docker and Docker Compose are installed and running on your machine.
- Use the Postman collection for quick testing and evaluation of the API endpoints.
