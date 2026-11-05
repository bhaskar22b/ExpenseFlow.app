
import sqlite3
import os

DATABASE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "expenses.db"
)


# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Initialize database
def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Add expense
def add_expense(description, amount, category, expense_date):
    conn = get_db_connection()

    conn.execute("""
        INSERT INTO expenses
        (description, amount, category, date)
        VALUES (?, ?, ?, ?)
    """, (description, amount, category, expense_date))

    conn.commit()
    conn.close()


# Get all expenses
def get_all_expenses():
    conn = get_db_connection()

    expenses = conn.execute("""
        SELECT * FROM expenses
        ORDER BY date DESC, id DESC
    """).fetchall()

    conn.close()

    return expenses


# Calculate total expenses
def get_total_expenses():
    conn = get_db_connection()

    total = conn.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
    """).fetchone()["total"]

    conn.close()

    return total




# Delete an expense
def delete_expense(expense_id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()





# Get expenses filtered by date, category and description
def get_filtered_expenses(
    start_date=None,
    end_date=None,
    category=None,
    search=None
):

    conn = get_db_connection()

    query = "SELECT * FROM expenses WHERE 1=1"

    parameters = []

    # Apply start date
    if start_date:
        query += " AND date >= ?"
        parameters.append(start_date)

    # Apply end date
    if end_date:
        query += " AND date <= ?"
        parameters.append(end_date)

    # Apply category
    if category:
        query += " AND category = ?"
        parameters.append(category)

    # Search by expense description
    if search:
        query += " AND description LIKE ?"
        parameters.append(f"%{search}%")

    # Show newest expenses first
    query += " ORDER BY date DESC, id DESC"

    expenses = conn.execute(query, parameters).fetchall()

    conn.close()

    return expenses



# Get all unique categories
def get_all_categories():
    conn = get_db_connection()

    categories = conn.execute("""
        SELECT DISTINCT category
        FROM expenses
        ORDER BY category ASC
    """).fetchall()

    conn.close()

    return [row["category"] for row in categories]


# Get expense totals grouped by category
def get_category_totals(start_date=None, end_date=None, category=None):

    conn = get_db_connection()

    query = """
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE 1=1
    """

    parameters = []

    if start_date:
        query += " AND date >= ?"
        parameters.append(start_date)

    if end_date:
        query += " AND date <= ?"
        parameters.append(end_date)

    if category:
        query += " AND category = ?"
        parameters.append(category)

    query += " GROUP BY category ORDER BY category ASC"

    results = conn.execute(query, parameters).fetchall()

    conn.close()

    return results


# Get daily expense totals
def get_daily_totals(start_date=None, end_date=None, category=None):

    conn = get_db_connection()

    query = """
        SELECT date, SUM(amount) AS total
        FROM expenses
        WHERE 1=1
    """

    parameters = []

    # Apply start date
    if start_date:
        query += " AND date >= ?"
        parameters.append(start_date)

    # Apply end date
    if end_date:
        query += " AND date <= ?"
        parameters.append(end_date)

    # Apply category
    if category:
        query += " AND category = ?"
        parameters.append(category)

    # Group expenses by date
    query += " GROUP BY date ORDER BY date ASC"

    results = conn.execute(query, parameters).fetchall()

    conn.close()

    return results

# Get a single expense by ID
def get_expense_by_id(expense_id):

    conn = get_db_connection()

    expense = conn.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    conn.close()

    return expense


# Update an existing expense
def update_expense(expense_id, description, amount, category, expense_date):

    conn = get_db_connection()

    conn.execute("""
        UPDATE expenses
        SET description = ?,
            amount = ?,
            category = ?,
            date = ?
        WHERE id = ?
    """, (description, amount, category, expense_date, expense_id))

    conn.commit()
    conn.close()