import json
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Expense Tracker")
app.geometry("520x760")

expenses = []

# ===== fox: storage =====

def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file)

def load_expenses():
    global expenses

    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)

        for expense in expenses:
            if "currency" not in expense:
                expense["currency"] = "USD"
            if "category" not in expense:
                expense["category"] = "Other"

    except FileNotFoundError:
        expenses = []

# ===== fox: logic =====

def update_expense_list():
    expense_list.delete("0.0", "end")

    for expense in expenses:
        title = expense.get("title", "Untitled")
        amount = expense.get("amount", 0)
        currency = expense.get("currency", "USD")
        category = expense.get("category", "Other")

        expense_list.insert(
            "end",
            f"{title} | {amount} {currency} | {category}\n"
        )

def update_totals():
    total_usd = 0
    total_irr = 0

    for expense in expenses:
        currency = expense.get("currency", "USD")
        amount = expense.get("amount", 0)

        if currency == "USD":
            total_usd += amount
        elif currency == "IRR":
            total_irr += amount

    total_usd_label.configure(text=f"Total USD: {total_usd}")
    total_irr_label.configure(text=f"Total IRR: {total_irr}")

def add_expense():
    title = title_entry.get().strip()
    amount = amount_entry.get().strip()
    category = category_dropdown.get()
    currency = currency_dropdown.get()

    if title == "" or amount == "":
        status_label.configure(text="Please fill title and amount")
        return

    try:
        amount = float(amount)
    except ValueError:
        status_label.configure(text="Amount must be a number")
        return

    expense = {
        "title": title,
        "amount": amount,
        "category": category,
        "currency": currency
    }

    expenses.append(expense)

    save_expenses()
    update_expense_list()
    update_totals()

    title_entry.delete(0, "end")
    amount_entry.delete(0, "end")
    category_dropdown.set("Food")
    currency_dropdown.set("USD")
    status_label.configure(text="Expense added")

def delete_last():
    if len(expenses) > 0:
        expenses.pop()
        save_expenses()
        update_expense_list()
        update_totals()
        status_label.configure(text="Last expense deleted")
    else:
        status_label.configure(text="No expenses to delete")

# ===== fox: ui =====

title_label = ctk.CTkLabel(app, text="Expense Tracker", font=("Arial", 24))
title_label.pack(pady=15)

title_entry = ctk.CTkEntry(app, placeholder_text="Title (e.g. Coffee)", width=320)
title_entry.pack(pady=5)

amount_entry = ctk.CTkEntry(app, placeholder_text="Amount (e.g. 4.5)", width=320)
amount_entry.pack(pady=5)

category_options = ["Food", "Travel", "Shopping", "Bills", "Health", "Other"]
category_dropdown = ctk.CTkOptionMenu(app, values=category_options, width=320)
category_dropdown.pack(pady=5)
category_dropdown.set("Food")

currency_options = ["USD", "IRR"]
currency_dropdown = ctk.CTkOptionMenu(app, values=currency_options, width=320)
currency_dropdown.pack(pady=5)
currency_dropdown.set("USD")

add_button = ctk.CTkButton(app, text="Add Expense", command=add_expense, width=220)
add_button.pack(pady=10)

delete_button = ctk.CTkButton(
    app,
    text="Delete Last",
    command=delete_last,
    width=220,
    fg_color="red"
)
delete_button.pack(pady=5)

expense_list = ctk.CTkTextbox(app, width=430, height=260)
expense_list.pack(pady=15)

total_usd_label = ctk.CTkLabel(app, text="Total USD: 0", font=("Arial", 18))
total_usd_label.pack(pady=5)

total_irr_label = ctk.CTkLabel(app, text="Total IRR: 0", font=("Arial", 18))
total_irr_label.pack(pady=5)

status_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
status_label.pack(pady=10)

# ===== fox: startup =====

load_expenses()
update_expense_list()
update_totals()

app.mainloop()
