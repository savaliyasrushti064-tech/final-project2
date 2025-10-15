import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class ExpenseTracker:
    def __init__(self, file_name='expenses.csv'):   # ✅ fixed constructor
        self.file_name = file_name
        try:
            self.data = pd.read_csv(self.file_name)
            print(f"Loaded data from {self.file_name}")
        except FileNotFoundError:
            print(f"{self.file_name} not found. Creating a new one.")
            self.data = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
            self.data.to_csv(self.file_name, index=False)

    def log_expense(self, date, amount, category, description):
        try:
            amount = float(amount)
            new_entry = pd.DataFrame([{
                "Date": date,
                "Amount": amount,
                "Category": category,
                "Description": description
            }])
            self.data = pd.concat([self.data, new_entry], ignore_index=True)
            self.data.to_csv(self.file_name, index=False)
            print("Expense added successfully!")
        except ValueError:
            print("Invalid input! Amount must be a number.")

    def load_data(self):
        try:
            self.data = pd.read_csv(self.file_name)
            print("Data loaded successfully!")
        except Exception as e:
            print(f"Error loading data: {e}")

    def clean_data(self):
        before = len(self.data)
        self.data.dropna(inplace=True)
        after = len(self.data)
        print(f"Removed {before - after} invalid entries.")
        self.data.to_csv(self.file_name, index=False)

    def get_summary(self):
        print("\n----- Expense Summary -----")
        total = self.data["Amount"].sum()
        avg = self.data["Amount"].mean()
        print(f"Total Expenses: ₹{total:.2f}")
        print(f"Average Expense: ₹{avg:.2f}")
        print("\nCategory-wise Spending:")
        print(self.data.groupby("Category")["Amount"].sum())
        print("---------------------------")

    def filter_expenses(self, category=None, start_date=None, end_date=None):
        filtered = self.data.copy()
        if category:
            filtered = filtered[filtered["Category"] == category]
        if start_date:
            filtered = filtered[pd.to_datetime(filtered["Date"]) >= pd.to_datetime(start_date)]
        if end_date:
            filtered = filtered[pd.to_datetime(filtered["Date"]) <= pd.to_datetime(end_date)]
        return filtered

    def visualize_expenses(self):
        if self.data.empty:
            print("No data available for visualization.")
            return
        
        self.data["Date"] = pd.to_datetime(self.data["Date"])  # ✅ Ensure datetime

        plt.figure(figsize=(10,6))
        sns.barplot(x="Category", y="Amount", data=self.data, estimator=np.sum)  # ✅ fixed
        plt.title("Total Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10,6))
        sns.lineplot(x="Date", y="Amount", data=self.data)
        plt.title("Spending Trends Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(8,6))
        self.data.groupby("Category")["Amount"].sum().plot.pie(autopct='%1.1f%%')
        plt.title("Proportional Spending by Category")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(8,6))
        sns.histplot(self.data["Amount"], bins=10, kde=True)
        plt.title("Frequency of Expense Amounts")
        plt.xlabel("Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


# ✅ Main loop
if __name__ == "__main__":   # ✅ fixed
    tracker = ExpenseTracker()
    while True:
        print("\n===== Smart Expense Tracker =====")
        print("1. Log New Expense")
        print("2. View Summary")
        print("3. Clean Data")
        print("4. Filter Expenses")
        print("5. Visualize Data")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            amount = input("Enter amount: ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.log_expense(date, amount, category, description)

        elif choice == "2":
            tracker.get_summary()

        elif choice == "3":
            tracker.clean_data()

        elif choice == "4":
            cat = input("Enter category (or press Enter to skip): ")
            sdate = input("Enter start date (or press Enter to skip): ")
            edate = input("Enter end date (or press Enter to skip): ")
            filtered = tracker.filter_expenses(cat or None, sdate or None, edate or None)
            print(filtered)

        elif choice == "5":
            tracker.visualize_expenses()

        elif choice == "6":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")
