# *** Brain Parsers Django Project ***

📖 **Overview**

This project contains web scrapers for [brain.com.ua](https://brain.com.ua) using three approaches:

- **BS4 (BeautifulSoup)** – lightweight HTML parsing 🟢  
- **Selenium** – browser automation for dynamic content ⚡  
- **Playwright** – modern async browser automation 🚀  

Each parser saves data to PostgreSQL, JSON, and CSV 📊.

---

## 🏠 Why Local Database Only

Originally, PostgreSQL ran via Docker 🐳, but for faster development:

- Parsers run locally while connecting to local PostgreSQL 💻  
- Avoids complex Docker setup for browsers and drivers 🛠️  
- Local DB expected at **127.0.0.1:5432**  

> Docker is still available for the Django app if needed, but local parser runs are faster ⚡

---

## 🧩 Requirements

- Python 3.11+ 🐍  
- PostgreSQL (running locally) 🗄️  
- Chrome/Chromium browser (for Selenium/Playwright) 🌐  
- Python packages from `requirements.txt` 📦  

---

## ⚙️ Setup

### 1️⃣ Clone the repository 📥

```bash
git clone https://github.com/kravetst/brain-parsers-django.git
cd brain-parsers-django


2️⃣ Create and activate virtual environment
python -m venv .venv
source .venv/Scripts/activate


3️⃣ Install dependencies

pip install --upgrade pip
pip install -r requirements.txt


4️⃣ Configure .env

Copy .env.example to .env and update credentials if needed:

5️⃣ Run migrations

python manage.py makemigrations
python manage.py migrate


## 🚀 Running Parsers Individually 

BS4 Parser
python manage.py parse_brain_bs4

Selenium Parser
python manage.py parse_brain_selenium

Playwright Parser
python manage.py parse_brain_playwright


Each parser will update the database, save JSON, and generate CSV files in results/ 📂

📝 Notes

All parsers can be run separately; the previous run_all_parsers.py script is removed ❌

modules/load_django.py is used to setup Django environment in standalone scripts 🔧

Playwright and Selenium require browsers installed locally; no Docker browser is used 🌐

Errors in dynamic content parsing may appear if page structure changes ⚠️