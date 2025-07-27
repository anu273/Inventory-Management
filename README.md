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

## 📂 Project Structure

For the application to work correctly, your project should follow this structure:

```
/your-project-folder
|-- static/
|   |-- index.html      # Your frontend user interface file
|
|-- app.py              # Main Flask application
|-- models.py           # Database models
|-- config.py           # Configuration settings
|-- init_db.py          # Database initialization script
|-- requirements.txt    # Python dependencies
|-- .env                # Environment variables (for secrets)
|-- .gitignore          # Files to be ignored by Git
```

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### **Prerequisites**

* Python 3.8+
* `pip` (Python package installer)

### **Setup Instructions**

**1. Clone the Repository**
```bash
git clone <your-repository-link>
cd <repository-folder>
```

**2. Create and Activate a Virtual Environment**
* **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* **On Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

**3. Install Dependencies**
Install all the required Python packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

**4. Set Up the Frontend**
Create a `static` folder in your project's root directory. Place your user interface file (e.g., the one we created earlier) inside this folder and name it `index.html`.

**5. Create the Environment File (`.env`)**
Create a `.env` file in the root directory. This file stores your secret keys and configuration settings. Copy the following content into it:

```
# Development secret keys (CHANGE THESE IN PRODUCTION!)
SECRET_KEY='dev-flask-secret-key-change-in-production-12345678901234567890'
JWT_SECRET_KEY='dev-jwt-secret-key-change-in-production-abcdefghijklmnopqrstuvwxyz'

# Database configuration
FLASK_ENV=development
```

**6. Initialize the Database**
Run the following Flask command to create the `inventory.db` file and all necessary tables.
```bash
flask init-db
```
You should see the output: `Initialized the database.`

**7. Run the Application**
You are now ready to run the full-stack application. The `flask run` command will start the backend server.
```bash
flask run
```
The server will start on `http://127.0.0.1:5000`.

To go to the webpage, open the `index.html` file located in the `static` folder in your web browser, or simply navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

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
