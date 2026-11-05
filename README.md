
# ExpenseFlow — Personal Expense Tracker

ExpenseFlow is a personal finance management web application built with Python, Flask and SQLite. It helps users record expenses, organise transactions, analyse spending patterns and manage their finances through a clean, responsive dashboard.

## Features

- **Dashboard:** View total spending, transaction counts and recent expenses.
- **Add Expenses:** Record expenses with descriptions, amounts, categories and dates.
- **Transaction Management:** Search, filter, edit and delete transactions.
- **Expense Analytics:** Visualise category-wise and daily spending with interactive charts.
- **Date Filtering:** Filter expenses by a selected date range.
- **Category Filtering:** View expenses belonging to specific categories.
- **Responsive Design:** Access the application on desktop and mobile devices.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database |
| HTML5 | Page structure |
| Tailwind CSS | Styling and responsive design |
| JavaScript | Interactive functionality |
| Chart.js | Data visualisation |
| Jinja2 | HTML templating |

## Project Structure

```text
expense-tracker-app/
│
├── app.py
├── database.py
├── .gitignore
├── README.md
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── edit.html
│   ├── transactions.html
│   └── analytics.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│
└── expenses.db
```

Note: `expenses.db` is generated locally and is excluded from GitHub.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd expense-tracker-app
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Flask

```bash
pip install Flask
```

### 6. Run the application

```bash
python app.py
```

### 7. Open in your browser

```text
http://127.0.0.1:5000/
```

The SQLite database is automatically initialised when the application starts.

## Future Improvements

- User authentication and registration
- Custom expense category management
- Currency preferences
- Monthly budget management
- Expense reports and CSV export
- Dark mode

## Author

Developed as a Python Flask project to practise backend development, database management and frontend design.

---

**ExpenseFlow — Track your spending. Understand your habits. Manage your money smarter.**
