
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import (
    init_db,
    add_expense,
    get_all_expenses,
    get_total_expenses,
    delete_expense,
    get_filtered_expenses,
    get_all_categories,
    get_category_totals,
    get_daily_totals,
    get_expense_by_id,
    update_expense
)

from datetime import date


app = Flask(__name__)
app.secret_key = "expense-tracker-secret-key"



# Convert and validate date strings
def parse_date(date_string):

    if not date_string:
        return None

    try:
        return date.fromisoformat(date_string)

    except ValueError:
        return None



# Dashboard and Add Expense Route
@app.route("/", methods=["GET", "POST"])
def dashboard():

    # Handle form submission
    if request.method == "POST":

        description = request.form.get("description", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("date", "").strip()

        # Check empty fields
        if not all([description, amount, category]):
            flash("Please fill in all fields.", "error")
            return redirect(url_for("dashboard"))

        # Validate amount
        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            flash("Please enter a valid positive amount.", "error")
            return redirect(url_for("dashboard"))

        # Save expense
        add_expense(description, amount, category, expense_date)

        flash("Expense added successfully!", "success")

        return redirect(url_for("dashboard"))

    
    # Get dates and category from URL
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    selected_category = request.args.get("category", "")

    # Validate dates
    start_date = parse_date(start)
    end_date = parse_date(end)

    # Check invalid dates
    if (start and start_date is None) or (end and end_date is None):
        flash("Please enter valid dates.", "error")
        return redirect(url_for("dashboard"))

    # Check date range
    if start_date and end_date and end_date < start_date:
        flash("End date cannot be before start date.", "error")
        return redirect(url_for("dashboard"))

    # Fetch filtered expenses
    expenses = get_filtered_expenses(
    start,
    end,
    selected_category
)

    categories = get_all_categories()

    # Get category-wise expense totals
    category_totals = get_category_totals(
        start,
        end,
        selected_category
)

    # Get daily expense totals
    daily_totals = get_daily_totals(
        start,
        end,
        selected_category
)

    # Prepare data for daily bar chart
    daylabels = []
    dayvalues = []

    for row in daily_totals:
        daylabels.append(row["date"])
        dayvalues.append(round(float(row["total"]), 2))


    # Prepare data for category pie chart
    catlabels = []
    catvalues = []

    for row in category_totals:
        catlabels.append(row["category"])
        catvalues.append(round(float(row["total"]), 2))

    # Calculate filtered total
    total = sum(expense["amount"] for expense in expenses)

    return render_template(
    "dashboard.html",
    expenses=expenses,
    total=total,
    start=start,
    end=end,
    categories=categories,
    selected_category=selected_category,
    today=date.today().isoformat(),
    catlabels=catlabels,
    catvalues=catvalues,
    daylabels=daylabels,
    dayvalues=dayvalues
)



# Edit Expense Route (GET)

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit(expense_id):

    # Get existing expense
    expense = get_expense_by_id(expense_id)

    if expense is None:
        flash("Expense not found.", "error")
        return redirect(url_for("dashboard"))

    # Handle form submission
    if request.method == "POST":

        description = request.form.get("description", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("date", "").strip()

        # Validate empty fields
        if not all([description, amount, category, expense_date]):
            flash("Please fill in all fields.", "error")
            return redirect(url_for("edit", expense_id=expense_id))

        # Validate amount
        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            flash("Please enter a valid positive amount.", "error")
            return redirect(url_for("edit", expense_id=expense_id))

        # Handle missing date
        if not expense_date:
            expense_date = date.today().isoformat()
        else:
            try:
                expense_date = date.fromisoformat(expense_date).isoformat()
            except ValueError:
                flash("Please enter a valid date.", "error")
                return redirect(url_for("edit", expense_id=expense_id))

        # Update expense in database
        update_expense(
            expense_id,
            description,
            amount,
            category,
            expense_date
        )

        flash("Expense updated successfully!", "success")

        return redirect(url_for("dashboard"))

    categories = get_all_categories()

    return render_template(
        "edit.html",
        expense=expense,
        categories=categories
    )



# Transactions Management Route
@app.route("/transactions")
def transactions():

    # Get filter values from URL
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    selected_category = request.args.get("category", "")
    search = request.args.get("search", "").strip()
    

    # Validate dates
    start_date = parse_date(start)
    end_date = parse_date(end)

    if (start and start_date is None) or (end and end_date is None):
        flash("Please enter valid dates.", "error")
        return redirect(url_for("transactions"))

    # Validate date range
    if start_date and end_date and end_date < start_date:
        flash("End date cannot be before start date.", "error")
        return redirect(url_for("transactions"))

    # Fetch filtered and searched transactions
    expenses = get_filtered_expenses(
    start,
    end,
    selected_category,
    search
)

    # Get available categories
    categories = get_all_categories()

    # Calculate total spending
    total = sum(float(expense["amount"]) for expense in expenses)

    # Display transactions page
    return render_template(
        "transactions.html",
        expenses=expenses,
        total=total,
        categories=categories,
        start=start,
        end=end,
        selected_category=selected_category,
        search=search
    )



# Delete Expense Route
@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):

    delete_expense(expense_id)

    flash("Expense deleted successfully!", "success")

    return_to = request.form.get("return_to", "dashboard")

    if return_to == "transactions":
        return redirect(url_for("transactions"))

    return redirect(url_for("dashboard"))



# Analytics Route
@app.route("/analytics")
def analytics():

    # Get filter values
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    selected_category = request.args.get("category", "")

    # Validate dates
    start_date = parse_date(start)
    end_date = parse_date(end)

    if (start and start_date is None) or (end and end_date is None):
        flash("Please enter valid dates.", "error")
        return redirect(url_for("analytics"))

    # Validate date range
    if start_date and end_date and end_date < start_date:
        flash("End date cannot be before start date.", "error")
        return redirect(url_for("analytics"))

    # Get category-wise totals
    category_totals = get_category_totals(
        start,
        end,
        selected_category
    )

    # Get daily totals
    daily_totals = get_daily_totals(
        start,
        end,
        selected_category
    )

    # Prepare category chart data
    catlabels = []
    catvalues = []

    for row in category_totals:
        catlabels.append(row["category"])
        catvalues.append(round(float(row["total"]), 2))

    # Prepare daily chart data
    daylabels = []
    dayvalues = []

    for row in daily_totals:
        daylabels.append(row["date"])
        dayvalues.append(round(float(row["total"]), 2))

    # Calculate total spending
    total = sum(catvalues)

    # Get categories
    categories = get_all_categories()

    return render_template(
        "analytics.html",
        total=total,
        categories=categories,
        selected_category=selected_category,
        start=start,
        end=end,
        catlabels=catlabels,
        catvalues=catvalues,
        daylabels=daylabels,
        dayvalues=dayvalues
    )



# Run Flask Application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
