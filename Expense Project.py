import csv
import datetime

""""
Defines a data model using __init__ method, it creates and initializes Transaction objects with the attributes: date, amount, category, and note.
Includes a display_info() method to output formatted transaction details.
"""

class Transaction:
    def __init__(self, date, amount, category="Misc", note=""):
        self.date = date
        self.amount = amount
        self.category = category
        self.note = note

    def display_info(self):
        print(f"{self.date} | {self.amount:.2f} | {self.category} | {self.note}")


"""
Initializes the ExpenseTracker object, setting up an empty list transactions and a predefined list of categories.
Calls load_data() to populate transactions from a CSV file and iteration over rows.
"""

class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.transactions = []
        self.categories = ["Food", "Transport", "Utilities", "Entertainment", "Misc"]
        self.filename = filename
        self.load_data()

    """
    validate_date: Uses datetime.strptime to parse and validate date strings.
    """
    def validate_date(self, date_vd):
        return datetime.datetime.strptime(date_vd, "%Y-%m-%d").date()


    """
    validate_amount: Converts input to float, raises Value error.
    """
    def validate_amount(self, amount):
        amount = float(amount)
        if amount < 0:
            raise ValueError("Invalid entry.")
        return amount

    """
    validate_month_year: Validates numeric input for month and year, ensures month is between 1 and 12.
    """
    def validate_month_year(self, month_vd, year_vd):
        if not month_vd.isdigit() or not year_vd.isdigit():
            print("Please enter numbers.")
            return None
        month = int(month_vd)
        year = int(year_vd)
        if not (1 <= month <= 12):
            print("Month must be between 1 to 12.")
            return None
        return month, year



    """
    Validates the date and amount using validate_date and validate_amount. 
    Formats the category and checks it against the allowed list. 
    Creates a Transaction object and adds it to the list of transactions. 
    Calls save_data() to write all transactions to the CSV file.
    """
    def add_expense(self, date, amount, category="Misc", note=""):
        date_obj = self.validate_date(date)
        amount_val = self.validate_amount(amount)
        category = category.strip().title()

        if category not in self.categories:
            raise ValueError(f"Invalid category '{category}'")

        transaction = Transaction(date_obj, amount_val, category, note)
        self.transactions.append(transaction)
        self.save_data()
        print("Expense added successfully.")



    """
    Iterates through transactions and calls each Transaction's display_info() to print the expense details.
    """
    def view_expenses(self):
        if not self.transactions:
            print("No transactions found.")
        else:
            print("\nAll Transactions:")
            for k in self.transactions:
                k.display_info()



    """
    Validates the given category and calculates the total spending for it  
    by summing the amounts of all matching transactions.
    """
    def total_by_category(self, category):
        category = category.strip().title()
        if category not in self.categories:
            print("Invalid category.")
            return
        total = sum(d.amount for d in self.transactions if d.category == category)
        print(f"Total spent on {category}: {total:.2f}")



    """
    Filters transactions by the given month and year, groups the amounts by category in a dictionary,  
    and computes the total spending for the specified period.
    """
    def get_monthly_summary(self, month, year):
        summary = {}
        total = 0
        for x in self.transactions:
            if x.date.month == month and x.date.year == year:
                category = x.category.strip().title()
                summary[category] = summary.get(category, 0) + x.amount
                total += x.amount
        return summary, total



    """
    Prints a summary of expenses for a given month, including totals by category,  
    the top spending category, and the overall total.
    """
    def monthly_summary(self, month, year):
        summary, total = self.get_monthly_summary(month, year)

        print(f"\nSummary for {month}/{year}:")
        if summary:
            for cat, amt in summary.items():
                print(f"{cat}: {amt:.2f}")
            highest = max(summary, key=summary.get)
            print(f"Highest spending category: {highest}")
            print(f"Total monthly spending: {total:.2f}")
        else:
            print("No data for this month.")

    """
    write_to_csv: Opens CSV file for writing, iterates over transactions, and writes their data rows.
    """
    def write_to_csv(self, filename):
        with open(filename, "w", newline="") as zy:
            writer = csv.writer(zy)
            writer.writerow(["Date", "Amount", "Category", "Note"])
            for x in self.transactions:
                writer.writerow([x.date.isoformat(), x.amount, x.category, x.note])

    """
    Saves all current transactions to the default CSV file.
    """
    def save_data(self):
        self.write_to_csv(self.filename)

    """
    Exports all transactions to the specified CSV file and confirms export.
    """
    def export_to_csv(self, filename):
        self.write_to_csv(filename)
        print(f"Report exported to {filename}")

    """
    Loads transactions from the default CSV file into the tracker.
    Skips the header row and validates data before adding transactions.
    """
    def load_data(self):
        try:
            with open(self.filename, "r") as zy:
                reader = csv.reader(zy)
                next(reader)  # Skip header

                for row in reader:
                    date_vd = row[0]
                    amount_vd = row[1]
                    category = row[2].strip().title()
                    note = row[3]

                    date = self.validate_date(date_vd)
                    amount = self.validate_amount(amount_vd)
                    self.transactions.append(Transaction(date, amount, category, note))

        except FileNotFoundError:
            pass

    """
    Shows a numbered menu of categories and asks the user to choose one by number.
    If the input is valid, returns the chosen category; otherwise, displays an error and returns None.
    """
    def select_category_by_number(self):
        print("\nAvailable Categories:")
        for k, category in enumerate(self.categories, start=1):
            print(f"{k}. {category}")

        selected = input("Select category by number: ").strip()
        if not selected.isdigit():
            print("Please enter a valid number.")
            return

        selected_index = int(selected) - 1
        if 0 <= selected_index < len(self.categories):
            print(f"Selected category: {self.categories[selected_index]}")
            return self.categories[selected_index]
        else:
            print("Choose a num from the list.")


def menu(tracker):
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total by Category")
        print("4. View Monthly Summary")
        print("5. Export Report")
        print("6. Exit")

        choice = input("Choose an option (1–6): ")

        try:
            if choice == "1":
                date = input("Enter date (YYYY-MM-DD): ")
                amount = input("Enter amount: ")
                category = tracker.select_category_by_number()
                if not category:
                    print("Failed to select category.")
                    continue
                note = input("Enter note: ")
                tracker.add_expense(date, amount, category, note)

            elif choice == "2":
                tracker.view_expenses()

            elif choice == "3":
                print("\nTotal by Category:")
                for category in tracker.categories:
                    tracker.total_by_category(category)

            elif choice == "4":
                month_vd = input("Enter month: ")
                year_vd = input("Enter year: ")
                result = tracker.validate_month_year(month_vd, year_vd)
                if result:
                    month, year = result
                    tracker.monthly_summary(month, year)
                else:
                    print("Invalid values.")

            elif choice == "5":
                filename = input("Enter filename to export : ")
                tracker.export_to_csv(filename)

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("oopsie!!! Invalid option")

        except Exception:
            print("Error")


if __name__ == "__main__":
    tracker = ExpenseTracker()

    test_data = [

        ("2025-08-02", 20.00, "Food", "Lunch"),
        ("2025-08-05", 60.00, "Transport", "Monthly bus pass"),
        ("2025-08-12", 100.00, "Utilities", "Water bill"),
        ("2025-08-18", 25.00, "Entertainment", "Movie"),
        ("2025-08-22", 5.00, "Misc", "Coffee"),
        ("2025-08-28", 35.00, "Food", "Groceries"),

        ("2025-09-01", 18.50, "Food", "Breakfast"),
        ("2025-09-07", 55.00, "Transport", "Train ticket"),
        ("2025-09-11", 90.00, "Utilities", "Gas bill"),
        ("2025-09-15", 40.00, "Entertainment", "Theater"),
        ("2025-09-21", 12.00, "Misc", "Books"),
        ("2025-09-25", 28.00, "Food", "Lunch"),
    ]

    menu(tracker)
