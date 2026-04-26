import json
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Expense Tracker")
app.geometry("500x700")

expenses = []

# -------------------- FILE FUNCTIONS -------------------
def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file)

def load_expenses():
    global expenses 


    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []
# -------------------- APP FUNCTIONS --------------------

def update_expense_list():
    expense_list.delete("0.0", "end")

    for expense in expenses:
        expense_list.insert(
            "end",
            f"{expense['title']} | ${expense['amount']} | {expense['category']}\n"
        )

def update_total():
    total = 0

    for expense in expenses:
        total += expense["amount"]

    total_label.configure(text=f"Total: ${total}")

def add_expense():
    title = title_entry.get()
    amount = amount_entry.get()
    category = category_entry.get()

    if title == "" or amount == "":
        total_label.configure(text="Please fill title and amount")
        return

    try:
        amount = float(amount)
    except ValueError:
        total_label.configure(text="Amount must be a number")
        return

    expense = {
        "title": title,
        "amount": amount,
        "category": category
    }

    expenses.append(expense)

    save_expenses()
    update_expense_list()
    update_total()

    title_entry.delete(0, "end")
    amount_entry.delete(0, "end")
    category_entry.delete(0, "end")

def delete_last():
    if len(expenses) > 0:
        expenses.pop()
        save_expenses()
        update_expense_list()
        update_total()

# -------------------- UI --------------------

title_label = ctk.CTkLabel(app, text="Expense Tracker", font=("Arial", 24))
title_label.pack(pady=15)

title_entry = ctk.CTkEntry(app, placeholder_text="Title (e.g. Coffee)", width=300)
title_entry.pack(pady=5)

amount_entry = ctk.CTkEntry(app, placeholder_text="Amount (e.g. 4.5)", width=300)
amount_entry.pack(pady=5)

category_options = ["Food","Travel","Shopping","Bills","Health","Other"]
category_dropdown = ctk.CTkOptionMenu(app, values=category_options, width=200)
category_dropdown.pack(pady=5)
category_dropdown.set("Food")

add_button = ctk.CTkButton(app, text="Add Expense", command=add_expense, width=200)
add_button.pack(pady=10)

delete_button = ctk.CTkButton(app, text="Delete Last", command=delete_last, width=200, fg_color="red")
delete_button.pack(pady=5)

expense_list = ctk.CTkTextbox(app, width=400, height=300)
expense_list.pack(pady=15)

total_label = ctk.CTkLabel(app, text="Total: $0", font=("Arial", 18))
total_label.pack(pady=10)

# ----------------- STARTUP -----------------

load_expenses()
update_expense_list()
update_total()

app.mainloop()