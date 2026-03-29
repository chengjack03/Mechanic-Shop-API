# Mechanic Shop API
A RESTful API for managing a mechanic shop's customers, mechanics, service tickets, and inventory. Built with Flask, SQLAlchemy, and MySQL.

## 🚀 Setup Instructions
1. **Clone the repository:**
   `git clone https://github.com/chengjack03/Mechanic-Shop-API.git`
2. **Create a virtual environment:** `python -m venv venv`
3. **Activate it:** `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac)
4. **Install dependencies:** `pip install -r requirements.txt`
5. **Create MySQL database:** `CREATE DATABASE mechanic_shop_db;`
6. **Update Configuration:** Update `config.py` with your MySQL credentials.
7. **Run the app:** `python app.py`

---

## 🧪 Testing
This project uses the built-in `unittest` library. The suite includes 23 tests covering all blueprints, including positive CRUD operations and negative validation testing.

**To run all tests:**
```powershell
python -m unittest discover tests