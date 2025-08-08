# Inventory Management Tool

A comprehensive backend service and user interface for managing product inventory. The backend is built with Python and Flask, featuring JWT-based authentication, while the frontend is a single-page application.

## ✨ Features

* **Full-Stack Application**: A complete solution with a backend API and a user-friendly frontend.
* **User Authentication**: Secure user registration and login using JWT (JSON Web Tokens).
* **Product Management**: Full CRUD (Create, Read, Update, Delete) functionality for inventory products.
* **Soft Deletion**: Products are marked as inactive instead of being permanently deleted.
* **Modular Design**: Backend code is organized into separate files for the application, models, and configuration.

## 🛠️ Tech Stack

* **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended
* **Frontend**: HTML, CSS, JavaScript (served statically by Flask)
* **Database**: SQLite
* **CORS Handling**: Flask-Cors
* **Containerization**: Docker

## 📂 Project Structure

For the application to work correctly, your project should follow this structure:

```
/your-project-folder
|-- static/
|   |-- index.html           # Your frontend user interface file
|
|-- routes/
|   |-- api_routes.py        # API endpoint definitions
|
|-- services/
|   |-- auth_service.py      # Authentication business logic
|   |-- product_service.py   # Product management business logic
|
|-- app.py                   # Main Flask application
|-- models.py                # Database models
|-- config.py                # Configuration settings
|-- init_db.py               # Database initialization script
|-- requirements.txt         # Python dependencies
|-- Dockerfile               # Docker container configuration
|-- .dockerignore           # Files to exclude from Docker build
|-- run.bat                 # Windows batch script to run with auto-browser
|-- .env                    # Environment variables (for secrets)
|-- .gitignore              # Files to be ignored by Git
```

## 🚀 Getting Started

You can run this application in two ways: **Docker (Recommended)** or **Local Setup**.

---

## 🐳 Docker Setup 

### **Prerequisites**
* Docker Desktop installed on your system
* Download from: https://www.docker.com/products/docker-desktop/

### **Quick Start with Docker**

**1. Clone the Repository**
```bash
git clone <repository-link>
cd  <repository-link>
```

**2. Build the Docker Image**
```bash
docker build -t inventory-app .
```

**3. Run the Application**

**Option A: Basic Run**
```bash
docker run -p 5000:5000 inventory-app
```

**Option B: Run with Auto-Browser Opening**

*Windows:*
```bash
docker run -p 5000:5000 inventory-app & start http://localhost:5000
```

*Mac/Linux:*
```bash
docker run -p 5000:5000 inventory-app & open http://localhost:5000
```


**4. Access Your Application**
- API: http://localhost:5000
- Frontend: http://localhost:5000 (if index.html is in static folder)

**5. Stop the Application**
Press `Ctrl+C` in the terminal where Docker is running.

---

## 📖 API Documentation

The backend exposes the following REST API endpoints.

**Base URL:** `http://127.0.0.1:5000`

### **Authentication**
All protected endpoints require an `Authorization` header with a Bearer token.
**Format:** `Authorization: Bearer <your_jwt_token>`

### **API Endpoints**

#### User Management
| Method | Endpoint    | Auth Required | Description                                    |
| :----- | :---------- | :------------ | :--------------------------------------------- |
| `POST` | `/register` | No            | Registers a new user.                          |
| `POST` | `/login`    | No            | Authenticates a user and returns a JWT.        |
| `GET`  | `/profile`  | **Yes** | Gets the profile of the currently logged-in user. |
| `PUT`  | `/profile`  | **Yes** | Updates the current user's profile information. |

#### Product Management
| Method   | Endpoint                  | Auth Required | Description                                    |
| :------- | :------------------------ | :------------ | :--------------------------------------------- |
| `POST`   | `/products`               | **Yes** | Adds a new product to the inventory.           |
| `GET`    | `/products`               | **Yes** | Retrieves a list of all active products.       |
| `GET`    | `/products/<id>`          | **Yes** | Retrieves a single product by its ID.          |
| `PUT`    | `/products/<id>`          | **Yes** | Updates a product's details.                   |
| `PUT`    | `/products/<id>/quantity` | **Yes** | Updates only the quantity of a product.        |
| `DELETE` | `/products/<id>`          | **Yes** | Soft-deletes a product (marks as inactive).    |
