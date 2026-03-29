# Mechanic Shop API 🛠️

A production-ready RESTful API for managing mechanic shop operations, including customers, mechanics, and service tickets. Built with Python, Flask, and SQLAlchemy.

## 🚀 Live Demo
- **API URL:** [https://mechanic-shop-api-5noq.onrender.com](https://mechanic-shop-api-5noq.onrender.com)
- **Documentation:** [https://mechanic-shop-api-5noq.onrender.com/api/docs/](https://mechanic-shop-api-5noq.onrender.com/api/docs/)

## 🛠️ Tech Stack
- **Framework:** Flask
- **Database:** PostgreSQL (Hosted on Render)
- **Production Server:** Gunicorn
- **Testing:** Pytest
- **CI/CD:** GitHub Actions
- **Deployment:** Render

## ⚙️ Features & Integration
- **Automated Testing:** Every push to `main` triggers a GitHub Actions workflow to run unit tests.
- **Continuous Deployment:** Successful test runs trigger an automatic deployment to Render via Deploy Hooks.
- **Environment Safety:** Uses environment variables for sensitive data like `DATABASE_URL` and `SECRET_KEY`.

## 🛠️ Local Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/chengjack03/Mechanic-Shop-API.git](https://github.com/chengjack03/Mechanic-Shop-API.git)