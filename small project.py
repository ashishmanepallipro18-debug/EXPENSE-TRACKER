# ============================================
# 💰 Personal Expense Tracker
# ============================================
# This program helps you track your daily expenses.
# It saves your data, shows summaries, and helps
# you understand where your money is going.
#
# CONCEPTS YOU WILL LEARN:
# - Variables and data types
# - Lists and Dictionaries
# - Functions (def)
# - Loops (while, for)
# - If/else conditions
# - File handling (reading/writing CSV)
# - String formatting
# ============================================


# ── STEP 1: IMPORT TOOLS ──────────────────────────────────────
# We import 'csv' to save/read data like a spreadsheet
# We import 'os' to check if a file exists on the computer
# We import 'datetime' to get today's date automatically

import csv
import os
from datetime import datetime


# ── STEP 2: SET UP CONSTANTS ──────────────────────────────────
# A constant is a value that never changes in the program
# We store the filename here so we only need to change it once

FILE_NAME = "expenses.csv"   # All expenses will be saved here

# These are the allowed spending categories
# Using a list keeps our categories organised
CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Shopping",
    "Bills",
    "Others"
]


# ── STEP 3: FILE FUNCTIONS ────────────────────────────────────
# These functions handle saving and loading data from the CSV file

def setup_file():
    """
    Creates the CSV file with headers if it doesn't exist yet.
    This runs once when the program starts.
    """
    # os.path.exists() checks if the file already exists
    # If it does NOT exist, we create it
    if not os.path.exists(FILE_NAME):

        # 'open()' opens a file. "w" means write mode.
        # 'newline=""' prevents extra blank lines in the CSV
        with open(FILE_NAME, "w", newline="") as file:

            # csv.writer helps us write rows into the CSV
            writer = csv.writer(file)

            # writerow() writes one row — this is the header row
            writer.writerow(["Date", "Category", "Amount", "Description"])

        print(f"  ✅ New expense file created: {FILE_NAME}")


def save_expense(date, category, amount, description):
    """
    Saves one expense entry to the CSV file.
    'a' means append mode — adds to the file without deleting old data.
    """
    # "a" = append mode, so we ADD to the file, not overwrite it
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        # Write the new expense as a new row
        writer.writerow([date, category, amount, description])


def load_expenses():
    """
    Reads ALL expenses from the CSV file and returns them as a list.
    Each expense is a dictionary like:
    {"Date": "2024-01-15", "Category": "Food", "Amount": 5.50, "Description": "Lunch"}
    """
    expenses = []   # Start with an empty list

    # Open the file in read mode ("r")
    with open(FILE_NAME, "r") as file:

        # csv.DictReader reads each row as a dictionary
        # So we can use expense["Category"] instead of expense[1]
        reader = csv.DictReader(file)

        # Loop through every row in the file
        for row in reader:
            # Convert Amount from string to float (number with decimals)
            # CSV files store everything as text, so we need to convert
            row["Amount"] = float(row["Amount"])
            expenses.append(row)   # Add this expense to our list

    return expenses   # Return the full list of expenses


# ── STEP 4: CORE FEATURES ────────────────────────────────────

def add_expense():
    """
    Asks the user to enter a new expense and saves it.
    """
    print("\n  ➕  ADD NEW EXPENSE")
    print("  " + "-"*35)

    # Get today's date automatically using datetime
    # strftime() formats the date as "YYYY-MM-DD"
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"  Date: {today}")

    # Show the categories with numbers so user can pick one
    print("\n  Categories:")
    for i, category in enumerate(CATEGORIES):
        # enumerate() gives us both the index (i) and the value (category)
        print(f"    {i+1}. {category}")

    # Keep asking until user picks a valid category number
    while True:
        try:
            # input() gets text from the user
            # int() converts that text to a whole number
            choice = int(input("\n  Pick a category (1-6): "))

            # Check if choice is within valid range
            if 1 <= choice <= len(CATEGORIES):
                category = CATEGORIES[choice - 1]   # -1 because lists start at 0
                break   # Exit the while loop
            else:
                print("  ⚠️  Please pick a number between 1 and 6.")

        except ValueError:
            # ValueError happens if user types letters instead of numbers
            print("  ⚠️  Please enter a number.")

    # Get the amount spent
    while True:
        try:
            amount = float(input("  Amount spent (SGD): $"))
            if amount > 0:
                break
            else:
                print("  ⚠️  Amount must be more than 0.")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")

    # Get a short description
    description = input("  Short description (e.g. Lunch at hawker): ").strip()
    if description == "":
        description = "No description"   # Default if user skips it

    # Save everything to the file
    save_expense(today, category, amount, description)
    print(f"\n  ✅ Expense saved! ${amount:.2f} for {category} — {description}")


def view_all_expenses():
    """
    Loads and displays all expenses in a neat table.
    """
    expenses = load_expenses()

    # Check if there are any expenses at all
    if len(expenses) == 0:
        print("\n  ℹ️  No expenses recorded yet. Add some first!")
        return   # Exit the function early

    print("\n  📋  ALL EXPENSES")
    print("  " + "-"*65)
    # f-strings let us format text with padding using < and >
    print(f"  {'Date':<12} {'Category':<14} {'Amount':>8}  Description")
    print("  " + "-"*65)

    total = 0   # We'll add up all amounts

    for expense in expenses:
        # Access dictionary values using the key names
        date        = expense["Date"]
        category    = expense["Category"]
        amount      = expense["Amount"]
        description = expense["Description"]

        total += amount   # Add to running total

        # :.2f formats numbers to 2 decimal places e.g. 5.5 → 5.50
        print(f"  {date:<12} {category:<14} ${amount:>7.2f}  {description}")

    print("  " + "-"*65)
    print(f"  {'TOTAL':<27} ${total:>7.2f}")


def view_summary():
    """
    Shows a summary — total per category and overall spending.
    Great for understanding where money is going.
    """
    expenses = load_expenses()

    if len(expenses) == 0:
        print("\n  ℹ️  No expenses to summarise yet.")
        return

    print("\n  📊  SPENDING SUMMARY")
    print("  " + "-"*40)

    # A dictionary to store total per category
    # We start each category at 0
    category_totals = {}
    for category in CATEGORIES:
        category_totals[category] = 0   # e.g. {"Food": 0, "Transport": 0 ...}

    grand_total = 0

    # Loop through all expenses and add amounts to the right category
    for expense in expenses:
        cat    = expense["Category"]
        amount = expense["Amount"]
        category_totals[cat] += amount   # Add to that category's total
        grand_total           += amount  # Add to overall total

    # Display the summary
    for category, total in category_totals.items():
        if total > 0:   # Only show categories that have spending
            # Calculate percentage of total spending
            percentage = (total / grand_total) * 100

            # Visual bar made of █ characters
            bar = "█" * int(percentage // 5)

            print(f"  {category:<14} ${total:>7.2f}  {percentage:>5.1f}%  {bar}")

    print("  " + "-"*40)
    print(f"  {'GRAND TOTAL':<14} ${grand_total:>7.2f}")

    # Find the highest spending category using max()
    highest_cat = max(category_totals, key=category_totals.get)
    print(f"\n  💸 You spend the most on: {highest_cat}")


def view_by_category():
    """
    Filter and show expenses for one specific category.
    """
    print("\n  🔍  FILTER BY CATEGORY")
    print("  " + "-"*35)

    for i, category in enumerate(CATEGORIES):
        print(f"    {i+1}. {category}")

    while True:
        try:
            choice = int(input("\n  Pick a category (1-6): "))
            if 1 <= choice <= len(CATEGORIES):
                selected = CATEGORIES[choice - 1]
                break
            else:
                print("  ⚠️  Pick between 1 and 6.")
        except ValueError:
            print("  ⚠️  Numbers only.")

    expenses = load_expenses()

    # Filter — only keep expenses matching the selected category
    # This is called "list comprehension" — a short way to filter a list
    filtered = [e for e in expenses if e["Category"] == selected]

    if len(filtered) == 0:
        print(f"\n  ℹ️  No expenses found for {selected}.")
        return

    print(f"\n  📋  {selected.upper()} EXPENSES")
    print("  " + "-"*55)

    total = 0
    for expense in filtered:
        amount = expense["Amount"]
        total += amount
        print(f"  {expense['Date']}  ${amount:>7.2f}  {expense['Description']}")

    print("  " + "-"*55)
    print(f"  Total spent on {selected}: ${total:.2f}")


# ── STEP 5: MAIN MENU ─────────────────────────────────────────
# This is the control centre of the whole program

def print_header():
    print("\n" + "="*45)
    print("   💰  Personal Expense Tracker")
    print("="*45)

def main():
    # Run setup first — creates file if needed
    setup_file()
    print_header()

    # while True creates an infinite loop
    # The program keeps showing the menu until user exits
    while True:
        print("\n  MENU")
        print("  1. Add new expense")
        print("  2. View all expenses")
        print("  3. View spending summary")
        print("  4. Filter by category")
        print("  5. Exit")

        choice = input("\n  Enter choice (1-5): ").strip()

        # Match the choice to the right function
        if   choice == "1": add_expense()
        elif choice == "2": view_all_expenses()
        elif choice == "3": view_summary()
        elif choice == "4": view_by_category()
        elif choice == "5":
            print("\n  Goodbye! Keep saving money! 👋\n")
            break   # break exits the while loop
        else:
            print("  ⚠️  Invalid choice. Please enter 1-5.")


# ── STEP 6: RUN THE PROGRAM ───────────────────────────────────
# This line means: only run main() if we run THIS file directly
# If another file imports this file, main() won't run automatically
# This is a Python best practice

if __name__ == "__main__":
    main()