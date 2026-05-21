import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


DATA_FILE = "data.txt"

CATEGORIES = ["Food", "Accommodation", "Transport", "Shopping", "Activities", "Other"]

CONTINENTS = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]

COUNTRIES = [
    ["Egypt", "Kenya", "Morocco", "South Africa", "Tanzania"],
    ["China", "India", "Indonesia", "Japan", "Singapore", "South Korea", "Thailand", "Vietnam"],
    ["France", "Germany", "Greece", "Italy", "Spain", "United Kingdom"],
    ["Canada", "Mexico", "United States"],
    ["Australia", "Fiji", "New Zealand"],
    ["Argentina", "Brazil", "Chile", "Peru"],
]


class Expense:
    def __init__(self, day, category, description, amount):
        self.day = day
        self.category = category
        self.description = description
        self.amount = amount


class Trip:
    def __init__(self, destination, days, total_budget):
        self.destination = destination
        self.days = days
        self.total_budget = total_budget
        self.daily_budget = total_budget / days
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def total_spent(self):
        total = 0
        for expense in self.expenses:
            total = total + expense.amount
        return total

    def remaining_budget(self):
        return self.total_budget - self.total_spent()

    def day_total(self, day):
        total = 0
        for expense in self.expenses:
            if expense.day == day:
                total = total + expense.amount
        return total


trips = []


def selected_trip(show_warning=True):
    selected = plan_table.selection()
    if len(selected) == 0:
        if show_warning == True:
            messagebox.showwarning("Choose plan", "Please select a travel plan first.")
        return None

    row_number = int(selected[0])
    return trips[row_number]


def selected_trip_index():
    selected = plan_table.selection()
    if len(selected) == 0:
        return -1
    return int(selected[0])


def update_everything():
    update_plan_table()
    update_details()


def update_details():
    update_expense_table()
    update_category_table()
    update_budget_panel()


def update_plan_table():
    for item in plan_table.get_children():
        plan_table.delete(item)

    for i in range(len(trips)):
        trip = trips[i]
        plan_table.insert(
            "",
            "end",
            iid=str(i),
            values=(
                trip.destination,
                trip.days,
                "$" + format(trip.total_budget, ".2f"),
                "$" + format(trip.daily_budget, ".2f"),
            ),
        )


def update_expense_table():
    for item in expense_table.get_children():
        expense_table.delete(item)

    trip = selected_trip(False)
    if trip == None:
        return

    for i in range(len(trip.expenses)):
        expense = trip.expenses[i]
        expense_table.insert(
            "",
            "end",
            iid=str(i),
            values=(
                i + 1,
                expense.day,
                expense.category,
                expense.description,
                "$" + format(expense.amount, ".2f"),
            ),
        )


def update_category_table():
    for item in category_table.get_children():
        category_table.delete(item)

    trip = selected_trip(False)
    if trip == None:
        return

    for category in CATEGORIES:
        total = 0
        for expense in trip.expenses:
            if expense.category == category:
                total = total + expense.amount
        category_table.insert("", "end", values=(category, "$" + format(total, ".2f")))


def update_budget_panel():
    trip = selected_trip(False)
    if trip == None:
        budget_title.config(text="No plan selected")
        total_budget_value.config(text="-")
        spent_value.config(text="-")
        remaining_value.config(text="-")
        daily_budget_value.config(text="-")
        status_value.config(text="-")
        budget_bar["value"] = 0
        budget_bar.configure(style="Neutral.Horizontal.TProgressbar")
        return

    spent = trip.total_spent()
    remaining = trip.remaining_budget()

    if spent > trip.total_budget:
        status = "Danger"
        percent = 100
    elif spent >= trip.total_budget * 0.7:
        status = "Warning"
        percent = spent / trip.total_budget * 100
    else:
        status = "Safe"
        percent = spent / trip.total_budget * 100

    budget_title.config(text=trip.destination)
    total_budget_value.config(text="$" + format(trip.total_budget, ".2f") + " AUD")
    spent_value.config(text="$" + format(spent, ".2f") + " AUD")
    remaining_value.config(text="$" + format(remaining, ".2f") + " AUD")
    daily_budget_value.config(text="$" + format(trip.daily_budget, ".2f") + " AUD")
    status_value.config(text=status)
    budget_bar["value"] = percent

    if status == "Safe":
        budget_bar.configure(style="Safe.Horizontal.TProgressbar")
    elif status == "Warning":
        budget_bar.configure(style="Warning.Horizontal.TProgressbar")
    else:
        budget_bar.configure(style="Danger.Horizontal.TProgressbar")


def plan_selected(event):
    update_details()


def update_countries(event=None):
    continent = continent_box.get()
    index = CONTINENTS.index(continent)
    country_box["values"] = COUNTRIES[index]
    country_box.set(COUNTRIES[index][0])


def create_plan():
    continent = continent_box.get()
    country = country_box.get()

    try:
        days = int(days_entry.get())
        total_budget = float(budget_entry.get())
    except:
        messagebox.showerror("Create plan", "Please enter valid days and budget.")
        return

    if days <= 0:
        messagebox.showerror("Create plan", "Days must be greater than 0.")
        return

    if total_budget <= 0:
        messagebox.showerror("Create plan", "Budget must be greater than 0.")
        return

    destination = continent + " - " + country
    trip = Trip(destination, days, total_budget)
    trips.append(trip)
    update_plan_table()
    plan_table.selection_set(str(len(trips) - 1))
    update_details()
    status_label.config(text="Created plan: " + destination)


def add_expense():
    trip = selected_trip()
    if trip == None:
        return

    try:
        day = int(expense_day_entry.get())
        amount = float(amount_entry.get())
    except:
        messagebox.showerror("Add expense", "Please enter valid day and amount.")
        return

    if day < 1 or day > trip.days:
        messagebox.showerror("Add expense", "Day must be between 1 and " + str(trip.days) + ".")
        return

    if amount <= 0:
        messagebox.showerror("Add expense", "Amount must be greater than 0.")
        return

    category = category_box.get()
    description = description_entry.get()
    if description == "":
        description = "No description"
    description = description.replace("|", "/")

    expense = Expense(day, category, description, amount)
    trip.add_expense(expense)
    update_details()

    if trip.day_total(day) > trip.daily_budget:
        status_label.config(text="Expense added. Warning: daily budget exceeded.")
    else:
        status_label.config(text="Expense added.")


def delete_expense():
    trip = selected_trip()
    if trip == None:
        return

    selected = expense_table.selection()
    if len(selected) == 0:
        messagebox.showwarning("Delete expense", "Please select an expense from the table.")
        return

    expense_index = int(selected[0])
    deleted = trip.expenses.pop(expense_index)
    update_details()
    status_label.config(text="Deleted expense: " + deleted.description)


def load_data():
    global trips
    trips = []
    current_trip = None

    try:
        file = open(DATA_FILE, "r")
        lines = file.readlines()
        file.close()
    except:
        messagebox.showerror("Load data", "Could not load data.txt.")
        return

    for line in lines:
        line = line.strip()
        if line != "" and line != "TRIPWISE_SIMPLE_TXT":
            parts = line.split("|")

            if parts[0] == "TRIP":
                destination = parts[1]
                days = int(parts[2])
                total_budget = float(parts[3])
                current_trip = Trip(destination, days, total_budget)
                trips.append(current_trip)

            elif parts[0] == "EXPENSE":
                day = int(parts[1])
                category = parts[2]
                description = parts[3]
                amount = float(parts[4])
                expense = Expense(day, category, description, amount)
                current_trip.add_expense(expense)

            elif parts[0] == "ENDTRIP":
                current_trip = None

    update_plan_table()
    if len(trips) > 0:
        plan_table.selection_set("0")
    update_details()
    status_label.config(text="Loaded data from data.txt.")


def save_data():
    if len(trips) == 0:
        messagebox.showwarning("Save data", "There is no data to save.")
        return

    try:
        file = open(DATA_FILE, "w")
        file.write("TRIPWISE_SIMPLE_TXT\n")

        for trip in trips:
            file.write("TRIP|" + trip.destination + "|" + str(trip.days) + "|" + str(trip.total_budget) + "\n")
            for expense in trip.expenses:
                line = "EXPENSE|"
                line = line + str(expense.day) + "|"
                line = line + expense.category + "|"
                line = line + expense.description.replace("|", "/") + "|"
                line = line + str(expense.amount)
                file.write(line + "\n")
            file.write("ENDTRIP\n")

        file.close()
        status_label.config(text="Saved data to data.txt.")
        messagebox.showinfo("Save data", "Data saved to data.txt.")
    except:
        messagebox.showerror("Save data", "Could not save data.")


window = tk.Tk()
window.title("TripWise")
window.geometry("1180x720")
window.minsize(1040, 640)
window.configure(bg="#f5f5f7")

style = ttk.Style()
style.theme_use("clam")
style.configure(".", font=(".AppleSystemUIFont", 12), background="#f5f5f7", foreground="#1d1d1f")
style.configure("TFrame", background="#f5f5f7")
style.configure("Card.TFrame", background="#ffffff", relief="flat")
style.configure("TLabel", background="#f5f5f7", foreground="#1d1d1f")
style.configure("Card.TLabel", background="#ffffff", foreground="#1d1d1f")
style.configure("Muted.TLabel", background="#ffffff", foreground="#6e6e73")
style.configure("Title.TLabel", font=(".AppleSystemUIFont", 28, "bold"), background="#f5f5f7", foreground="#1d1d1f")
style.configure("Subtitle.TLabel", font=(".AppleSystemUIFont", 13), background="#f5f5f7", foreground="#6e6e73")
style.configure("Header.TLabel", font=(".AppleSystemUIFont", 15, "bold"), background="#ffffff", foreground="#1d1d1f")
style.configure("TButton", padding=(16, 8), background="#ffffff", foreground="#1d1d1f", borderwidth=0)
style.map("TButton", background=[("active", "#e8e8ed")])
style.configure("Accent.TButton", padding=(18, 9), background="#007aff", foreground="#ffffff", borderwidth=0)
style.map("Accent.TButton", background=[("active", "#0a84ff")], foreground=[("active", "#ffffff")])
style.configure("Treeview", rowheight=30, background="#ffffff", fieldbackground="#ffffff", foreground="#1d1d1f", borderwidth=0)
style.configure("Treeview.Heading", font=(".AppleSystemUIFont", 12, "bold"), background="#f2f2f7", foreground="#1d1d1f", borderwidth=0)
style.map("Treeview", background=[("selected", "#d6e9ff")], foreground=[("selected", "#1d1d1f")])
style.configure("TNotebook", background="#f5f5f7", borderwidth=0)
style.configure("TNotebook.Tab", padding=(18, 9), background="#e8e8ed", foreground="#1d1d1f")
style.map("TNotebook.Tab", background=[("selected", "#ffffff")])
style.configure("TLabelframe", background="#ffffff", borderwidth=0, relief="flat")
style.configure("TLabelframe.Label", background="#ffffff", foreground="#1d1d1f", font=(".AppleSystemUIFont", 13, "bold"))
style.configure("TEntry", padding=5)
style.configure("TCombobox", padding=5)
style.configure("Neutral.Horizontal.TProgressbar", troughcolor="#e5e5ea", background="#c7c7cc")
style.configure("Safe.Horizontal.TProgressbar", troughcolor="#e5e5ea", background="#34c759")
style.configure("Warning.Horizontal.TProgressbar", troughcolor="#e5e5ea", background="#ffcc00")
style.configure("Danger.Horizontal.TProgressbar", troughcolor="#e5e5ea", background="#ff3b30")

top_frame = ttk.Frame(window, padding=14)
top_frame.pack(fill="x")

title_label = ttk.Label(top_frame, text="TripWise", style="Title.TLabel")
title_label.pack(side="left")
subtitle_label = ttk.Label(top_frame, text="Travel budget tracker", style="Subtitle.TLabel")
subtitle_label.pack(side="left", padx=(12, 0), pady=(10, 0))

button_frame = ttk.Frame(top_frame)
button_frame.pack(side="right")

ttk.Button(button_frame, text="Load Data", style="Accent.TButton", command=load_data).pack(side="left", padx=4)
ttk.Button(button_frame, text="Save Data", command=save_data).pack(side="left", padx=4)

body = ttk.Frame(window, padding=(14, 0, 14, 10))
body.pack(fill="both", expand=True)

left_panel = ttk.Frame(body)
left_panel.pack(side="left", fill="both", expand=True)

right_panel = ttk.Frame(body, width=280)
right_panel.pack(side="right", fill="y", padx=(12, 0))
right_panel.pack_propagate(False)

plan_frame = ttk.LabelFrame(left_panel, text="Travel Plans", padding=12)
plan_frame.pack(fill="x")

plan_columns = ("destination", "days", "budget", "daily")
plan_table = ttk.Treeview(plan_frame, columns=plan_columns, show="headings", height=6)
plan_table.heading("destination", text="Destination")
plan_table.heading("days", text="Days")
plan_table.heading("budget", text="Total Budget")
plan_table.heading("daily", text="Daily Budget")
plan_table.column("destination", width=260)
plan_table.column("days", width=70, anchor="center")
plan_table.column("budget", width=120, anchor="center")
plan_table.column("daily", width=120, anchor="center")
plan_table.pack(fill="x")
plan_table.bind("<<TreeviewSelect>>", plan_selected)

notebook = ttk.Notebook(left_panel)
notebook.pack(fill="both", expand=True, pady=(10, 0))

create_tab = ttk.Frame(notebook, padding=18, style="Card.TFrame")
expense_tab = ttk.Frame(notebook, padding=18, style="Card.TFrame")
category_tab = ttk.Frame(notebook, padding=18, style="Card.TFrame")
notebook.add(create_tab, text="Create Plan")
notebook.add(expense_tab, text="Expenses")
notebook.add(category_tab, text="Category Summary")

ttk.Label(create_tab, text="Create a Travel Plan", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

ttk.Label(create_tab, text="Continent").grid(row=1, column=0, sticky="w", pady=4)
continent_box = ttk.Combobox(create_tab, values=CONTINENTS, state="readonly", width=28)
continent_box.grid(row=1, column=1, sticky="w", pady=4)
continent_box.set(CONTINENTS[0])
continent_box.bind("<<ComboboxSelected>>", update_countries)

ttk.Label(create_tab, text="Country").grid(row=2, column=0, sticky="w", pady=4)
country_box = ttk.Combobox(create_tab, values=COUNTRIES[0], state="readonly", width=28)
country_box.grid(row=2, column=1, sticky="w", pady=4)
country_box.set(COUNTRIES[0][0])

ttk.Label(create_tab, text="Travel days").grid(row=3, column=0, sticky="w", pady=4)
days_entry = ttk.Entry(create_tab, width=30)
days_entry.grid(row=3, column=1, sticky="w", pady=4)

ttk.Label(create_tab, text="Total budget AUD").grid(row=4, column=0, sticky="w", pady=4)
budget_entry = ttk.Entry(create_tab, width=30)
budget_entry.grid(row=4, column=1, sticky="w", pady=4)

ttk.Button(create_tab, text="Create Plan", style="Accent.TButton", command=create_plan).grid(row=5, column=1, sticky="w", pady=14)

expense_form = ttk.Frame(expense_tab, style="Card.TFrame")
expense_form.pack(fill="x")

ttk.Label(expense_form, text="Add Expense", style="Header.TLabel").grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))
ttk.Label(expense_form, text="Day").grid(row=1, column=0, sticky="w", padx=(0, 4))
expense_day_entry = ttk.Entry(expense_form, width=8)
expense_day_entry.grid(row=1, column=1, sticky="w", padx=(0, 12))

ttk.Label(expense_form, text="Category").grid(row=1, column=2, sticky="w", padx=(0, 4))
category_box = ttk.Combobox(expense_form, values=CATEGORIES, state="readonly", width=16)
category_box.grid(row=1, column=3, sticky="w", padx=(0, 12))
category_box.set(CATEGORIES[0])

ttk.Label(expense_form, text="Description").grid(row=1, column=4, sticky="w", padx=(0, 4))
description_entry = ttk.Entry(expense_form, width=24)
description_entry.grid(row=1, column=5, sticky="w", padx=(0, 12))

ttk.Label(expense_form, text="Amount").grid(row=1, column=6, sticky="w", padx=(0, 4))
amount_entry = ttk.Entry(expense_form, width=12)
amount_entry.grid(row=1, column=7, sticky="w", padx=(0, 12))

ttk.Button(expense_form, text="Add", style="Accent.TButton", command=add_expense).grid(row=1, column=8, sticky="w")

expense_columns = ("number", "day", "category", "description", "amount")
expense_table = ttk.Treeview(expense_tab, columns=expense_columns, show="headings", height=12)
expense_table.heading("number", text="#")
expense_table.heading("day", text="Day")
expense_table.heading("category", text="Category")
expense_table.heading("description", text="Description")
expense_table.heading("amount", text="Amount")
expense_table.column("number", width=50, anchor="center")
expense_table.column("day", width=60, anchor="center")
expense_table.column("category", width=130)
expense_table.column("description", width=330)
expense_table.column("amount", width=110, anchor="center")
expense_table.pack(fill="both", expand=True, pady=(14, 8))

delete_frame = ttk.Frame(expense_tab, style="Card.TFrame")
delete_frame.pack(fill="x")
ttk.Button(delete_frame, text="Delete Selected Expense", command=delete_expense).pack(side="left")

category_columns = ("category", "total")
category_table = ttk.Treeview(category_tab, columns=category_columns, show="headings", height=8)
category_table.heading("category", text="Category")
category_table.heading("total", text="Total")
category_table.column("category", width=250)
category_table.column("total", width=150, anchor="center")
category_table.pack(fill="x")

summary_frame = ttk.LabelFrame(right_panel, text="Budget Dashboard", padding=16)
summary_frame.pack(fill="x")

budget_title = ttk.Label(summary_frame, text="No plan selected", style="Header.TLabel", wraplength=240)
budget_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

ttk.Label(summary_frame, text="Total budget").grid(row=1, column=0, sticky="w", pady=4)
total_budget_value = ttk.Label(summary_frame, text="-")
total_budget_value.grid(row=1, column=1, sticky="e", pady=4)

ttk.Label(summary_frame, text="Total spent").grid(row=2, column=0, sticky="w", pady=4)
spent_value = ttk.Label(summary_frame, text="-")
spent_value.grid(row=2, column=1, sticky="e", pady=4)

ttk.Label(summary_frame, text="Remaining").grid(row=3, column=0, sticky="w", pady=4)
remaining_value = ttk.Label(summary_frame, text="-")
remaining_value.grid(row=3, column=1, sticky="e", pady=4)

ttk.Label(summary_frame, text="Daily budget").grid(row=4, column=0, sticky="w", pady=4)
daily_budget_value = ttk.Label(summary_frame, text="-")
daily_budget_value.grid(row=4, column=1, sticky="e", pady=4)

ttk.Label(summary_frame, text="Status").grid(row=5, column=0, sticky="w", pady=4)
status_value = ttk.Label(summary_frame, text="-")
status_value.grid(row=5, column=1, sticky="e", pady=4)

budget_bar = ttk.Progressbar(summary_frame, maximum=100, style="Neutral.Horizontal.TProgressbar")
budget_bar.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 4))

tip_frame = ttk.LabelFrame(right_panel, text="Quick Tips", padding=16)
tip_frame.pack(fill="x", pady=(12, 0))
tip_text = "1. Load data first.\n2. Select a plan.\n3. Add or view expenses.\n4. Save data after changes."
ttk.Label(tip_frame, text=tip_text, wraplength=240, justify="left").pack(anchor="w")

status_label = ttk.Label(window, text="Ready. Please click Load Data to show saved travel plans.", anchor="w", padding=(14, 8))
status_label.pack(fill="x", side="bottom")

window.mainloop()
