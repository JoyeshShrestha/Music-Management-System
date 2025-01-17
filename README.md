# Music Management System Documentation

## Overview
This is a Flask-based web application for managing users, artists, and music tracks. The application provides features such as user registration, login, artist and music management, and pagination for listing data. It uses `Flask-Login` for authentication and session management, and `Flask-SQLAlchemy` for database interactions.

## Features
- User authentication (login, registration, logout).
- Role-based access for managing users, artists, and music.
- CRUD operations for users, artists, and music.
- Pagination for user, artist, and music lists.
- Flash messages for user feedback.

## Prerequisites
- Python 3.7+
- Flask 2.0+
- Flask-Login
- pymysql
- Werkzeug
- dotenv

## Installation

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate   # For Windows
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    - Create a `.env` file in the root directory and add the following:
      ```env
      SECRET_KEY=your_secret_key_here
      DATABASE_URL=your_database_connection_string
      ```

5. **Run the Application**:
    ```bash
    python app.py
    ```

6. **Access the Application**:
    - Open a browser and go to: `http://127.0.0.1:5000`

## Folder Structure
```
|-- app.py              # Main application file
|-- db/                 # Database connection and helpers
|   |-- get_db_connection.py
|-- models/             # Models for database interactions
|   |-- user_db.py
|   |-- artist_db.py
|   |-- music_db.py
|-- templates/          # HTML templates
|   |-- register.html
|   |-- login.html
|   |-- dashboard.html
|   |-- user.html
|   |-- artist.html
|   |-- music.html
|-- static/             # Static files (CSS, JS, images)
```

## Routes

### Authentication
| Route               | Method | Description                          |
|---------------------|--------|--------------------------------------|
| `/`                 | GET/POST | User registration                   |
| `/login`            | GET/POST | User login                          |
| `/logout`           | GET     | User logout                         |

### Dashboard
| Route               | Method | Description                          |
|---------------------|--------|--------------------------------------|
| `/dashboard`        | GET     | Dashboard view                      |

### Users
| Route                           | Method | Description                          |
|---------------------------------|--------|--------------------------------------|
| `/dashboard/users`              | GET    | List all users with pagination       |
| `/dashboard/users/adduser`      | GET/POST | Add a new user                       |
| `/dashboard/users/edituser/<id>`| GET/POST | Edit an existing user                |
| `/dashboard/users/delete/<id>`  | GET    | Delete a user                        |

### Artists
| Route                           | Method | Description                          |
|---------------------------------|--------|--------------------------------------|
| `/dashboard/artists`            | GET    | List all artists with pagination     |
| `/dashboard/artists/addartist`  | GET/POST | Add a new artist                     |
| `/dashboard/artists/editartist/<id>`| GET/POST | Edit an existing artist          |
| `/dashboard/artist/delete/<id>` | GET    | Delete an artist                     |

### Music
| Route                                      | Method | Description                          |
|-------------------------------------------|--------|--------------------------------------|
| `/dashboard/artists/<artist_id>/music`    | GET    | List all music tracks of an artist   |
| `/dashboard/artists/<artist_id>/music/addmusic` | GET/POST | Add a new music track      |
| `/dashboard/artist/<artist_id>/music/delete/<id>`| GET | Delete a music track         |
| `/dashboard/artists/<artist_id>/music/update/<id>`| GET/POST | Edit a music track      |

## Key Files and Functions

### `app.py`
- **Routes**: Handles the application’s endpoints and logic.
- **Authentication**:
  - `@login_manager.user_loader`: Loads the user by ID for Flask-Login.
  - `login_user`, `logout_user`: Manages user sessions.

### `user_db.py`, `artist_db.py`, `music_db.py`
- Handles database operations for users, artists, and music respectively.

### Templates
- HTML files for rendering pages with `Flask-Jinja2`.
- Includes forms for CRUD operations and pagination.

### Static Files
- CSS and JavaScript files for styling and interactivity.

## Pagination
Pagination is implemented in the following routes:
- `/dashboard/users`
- `/dashboard/artists`
- `/dashboard/artists/<artist_id>/music`

**Logic**:
- Each route uses `page` and `per_page` query parameters.
- Calculates total pages using `total_items` and `per_page`.

## Security Features
- Passwords are hashed using `Werkzeug.security.generate_password_hash`.
- Sessions are managed securely with `Flask-Login`.


- Add testing for routes and database functions.
- Enhance UI/UX with modern frameworks like Bootstrap or Tailwind CSS.

---
Feel free to contribute or raise issues via GitHub!

