# Inventory Management Tool

A comprehensive backend service for managing product inventory, built with Python, Flask, and SQLAlchemy. It features JWT-based authentication for securing API endpoints, a modular structure for configuration and models, and a full suite of features for user and product management.

## ✨ Features

* **User Authentication**: Secure user registration and login using JWT (JSON Web Tokens).
* **Product Management**: Full CRUD (Create, Read, Update, Delete) functionality for inventory products.
* **Profile Management**: Users can view and update their own profiles.
* **Soft Deletion**: Products are marked as inactive instead of being permanently deleted from the database.
* **Modular Design**: Code is organized into separate files for the main application (`app.py`), database models (`models.py`), and configuration (`config.py`).
* **CLI Commands**: Includes easy-to-use command-line commands to initialize or reset the database.

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Database**: SQLite (default), easily configurable for others like PostgreSQL.
* **ORM**: Flask-SQLAlchemy
* **Authentication**: Flask-JWT-Extended
* **CORS Handling**: Flask-Cors

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
Using a virtual environment is a best practice for managing dependencies.

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
Create a file named `requirements.txt` in the root of your project with the following content:
```txt
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-Cors
python-dotenv
Werkzeug
```
Then, install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

**4. Create the Environment File (`.env`)**
The application requires a `.env` file in the root directory to store your secret key for signing JWTs. Create the file and add the following line.

**Important**: Replace `'your-super-secret-and-long-jwt-key'` with a strong, randomly generated string.
```
JWT_SECRET_KEY='your-super-secret-and-long-jwt-key'
```

**5. Initialize the Database**
The application uses a custom Flask command to create the `inventory.db` file and set up all the necessary tables. Run this command from your terminal:
```bash
flask init-db
```
You should see the output: `Initialized the database.`

Alternatively, you can use the provided `init_db.py` script:
```bash
python init_db.py
```

**6. Run the Application**
You're all set! Start the Flask development server with the following command:
```bash
flask run
```
The API will now be running on `http://127.0.0.1:5000`.

## 📖 API Documentation

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
