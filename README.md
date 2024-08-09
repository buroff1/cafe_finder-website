# Cafe Finder ☕
## 🧪Demo
<p align="center">
  <img src="https://github.com/user-attachments/assets/e116df34-a44a-4bc4-b6c4-3148a067fa30" alt="Demo">
</p>

## 📝Content

- [Overview](#%EF%B8%8Foverview)
- [Technologies](#technologies)
- [Features](#features)
- [Project Structure](#%EF%B8%8Fproject-structure)
- [Run Project](#run-project)
- [Admin Key](#admin-key)
- [Contributing](#contributing)
- [Contact](#contact)

## 🗺️Overview

Cafe Time is a Flask-based web application designed to help users find and manage the best cafes for working or studying. The app features detailed cafe listings, interactive maps, and admin functionalities for managing the listings.

## 👨‍💻Technologies

- **Flask**: A lightweight WSGI web application framework used for server setup.
- **Bootstrap**: For responsive front-end design.
- **SQLite**: Used for the application's database needs.
- **SQLAlchemy**: ORM used for database interactions.
- **Flask-WTF**: For form handling in Flask applications

## 👀Features

- **Cafe Listings**: View detailed information about each cafe, including hours, location, and amenities.
- **Interactive Map**: Locate cafes on a map to easily find them based on your location.
- **Admin Features**: Administrators can add, edit, or delete cafe listings using a special admin key.

## 🗃️Project Structure

- `/templates`
  - `add_cafe.html`: Form template for adding new cafes.
  - `index.html`: Main page template showing cafe listings and map.
- `main.py`: The main Flask application script.
- `requirements.txt`: Required libraries for running the project.

## ✅Run Project

1. **Clone the repository**:
```
git clone https://github.com/buroff1/cafe_finder-website.git
cd cafe_finder-website
```
2. **Set up a virtual environment**:
```
python3 -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```
3. **Install dependencies**:
```
pip install -r requirements.txt
```
4. **Run the application**:
```
python main.py
```
5. **Visit the website**:
- Open `http://localhost:5000` in your web browser.

## 🔑Admin Key

An admin key is used to manage cafe entries (edit/delete). Ensure this key is kept secure and is not hard-coded in your public codebase.

## 🤝Contributing

Interested in contributing? Follow these steps:

1. Fork the repo.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## 📧Contact

- Email: [artem.burov0205@gmail.com](mailto:artem.burov0205@gmail.com)
- GitHub: [buroff1](https://github.com/buroff1)
