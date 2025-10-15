# final-project2

Smart Expense Tracker

A Python-based expense tracker that helps you log, manage, clean, filter, summarize, and visualize your daily expenses. It stores data in a CSV file and provides insights with charts and statistics.

🚀 Features

✅ Log new expenses (Date, Amount, Category, Description)

✅ Store expenses in a CSV file (expenses.csv)

✅ Automatically load and clean data (remove missing values)

✅ View summary reports (total, average, category-wise spending)

✅ Filter expenses by category and date range

✅ Generate visualizations:

Bar chart: Expenses by category

Line chart: Spending trends over time

Pie chart: Proportional spending by category

Histogram: Frequency of expense amounts

📂 Project Structure
SmartExpenseTracker/
│── expense_tracker.py   # Main code
│── expenses.csv         # Data file (auto-created if missing)
│── README.md            # Documentation

⚙️ Requirements

Python 3.x

Libraries:

pip install pandas numpy matplotlib seaborn

▶️ How to Run

Clone or download the project.

Run the Python file:

python expense_tracker.py


Use the menu options:

===== Smart Expense Tracker =====
1. Log New Expense
2. View Summary
3. Clean Data
4. Filter Expenses
5. Visualize Data
6. Exit

📝 Example Workflow

Log a new expense:

Enter date (YYYY-MM-DD): 2025-10-15
Enter amount: 500
Enter category: Food
Enter description: Lunch with friends


View summary:

----- Expense Summary -----
Total Expenses: ₹500.00
Average Expense: ₹500.00

Category-wise Spending:
Food    500.0
---------------------------

📊 Visualizations

Bar Chart – total expenses by category

Line Chart – spending trends over time

Pie Chart – proportional spending by category

Histogram – frequency of expense amounts

🔮 Future Improvements

Add monthly/weekly reports

Export reports to PDF/Excel

Build a simple GUI or Web App
