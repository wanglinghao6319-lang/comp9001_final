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


def print_menu():
    print()
    print("Main Menu")
    print("1. Create new travel plan")
    print("2. View travel plan")
    print("3. Add expense")
    print("4. View all expenses")
    print("5. View expenses by category")
    print("6. Save data")
    print("7. Load data")
    print("8. Delete expense")
    print("9. Exit")


def print_one_plan(trip):
    print("Destination: " + trip.destination)
    print("Days: " + str(trip.days))
    print("Total budget: $" + format(trip.total_budget, ".2f") + " AUD")
    print("Daily budget: $" + format(trip.daily_budget, ".2f") + " AUD")


def print_budget_summary(trip):
    spent = trip.total_spent()
    remaining = trip.remaining_budget()

    if spent > trip.total_budget:
        status = "Danger"
        message = "You have exceeded your total budget."
    elif spent >= trip.total_budget * 0.7:
        status = "Warning"
        message = "You are close to your total budget."
    else:
        status = "Safe"
        message = "Your spending is under control."

    print()
    print("Budget Summary for " + trip.destination)
    print("Status: " + status)
    print(message)
    print("Total budget: $" + format(trip.total_budget, ".2f") + " AUD")
    print("Total spent: $" + format(spent, ".2f") + " AUD")
    print("Remaining budget: $" + format(remaining, ".2f") + " AUD")


def create_trip(trips):
    print()
    print("Choose a continent:")
    for i in range(len(CONTINENTS)):
        print(str(i + 1) + ". " + CONTINENTS[i])

    try:
        continent_number = int(input("Continent number: "))
    except:
        print("Please enter a valid number.")
        return

    if continent_number < 1 or continent_number > len(CONTINENTS):
        print("Invalid continent number.")
        return

    continent = CONTINENTS[continent_number - 1]
    country_list = COUNTRIES[continent_number - 1]

    print()
    print("Choose a country in " + continent + ":")
    for i in range(len(country_list)):
        print(str(i + 1) + ". " + country_list[i])

    try:
        country_number = int(input("Country number: "))
    except:
        print("Please enter a valid number.")
        return

    if country_number < 1 or country_number > len(country_list):
        print("Invalid country number.")
        return

    try:
        days = int(input("Number of travel days: "))
    except:
        print("Please enter a valid whole number.")
        return

    if days <= 0:
        print("Number of travel days must be greater than 0.")
        return

    try:
        total_budget = float(input("Total budget (AUD): "))
    except:
        print("Please enter a valid number.")
        return

    if total_budget <= 0:
        print("Total budget must be greater than 0.")
        return

    country = country_list[country_number - 1]
    destination = continent + " - " + country
    trip = Trip(destination, days, total_budget)
    trips.append(trip)

    print()
    print("Travel plan created successfully.")
    print_one_plan(trip)


def view_travel_plans(trips):
    if len(trips) == 0:
        print("Please create or load a travel plan first.")
        return

    print()
    print("Travel Plans")
    for i in range(len(trips)):
        print()
        print("Plan " + str(i + 1))
        print_one_plan(trips[i])


def add_expense(trips):
    if len(trips) == 0:
        print("Please create or load a travel plan first.")
        return

    if len(trips) == 1:
        trip = trips[0]
    else:
        print()
        print("Choose a travel plan:")
        for i in range(len(trips)):
            trip = trips[i]
            print(str(i + 1) + ". " + trip.destination + " | " + str(trip.days) + " days | $" + format(trip.total_budget, ".2f") + " AUD")

        try:
            plan_number = int(input("Plan number: "))
        except:
            print("Please enter a valid number.")
            return

        if plan_number < 1 or plan_number > len(trips):
            print("Invalid plan number.")
            return

        trip = trips[plan_number - 1]

    try:
        day = int(input("Travel day number: "))
    except:
        print("Please enter a valid whole number.")
        return

    if day < 1 or day > trip.days:
        print("Day must be between 1 and " + str(trip.days) + ".")
        return

    print()
    print("Choose a category:")
    for i in range(len(CATEGORIES)):
        print(str(i + 1) + ". " + CATEGORIES[i])

    try:
        category_number = int(input("Category number: "))
    except:
        print("Please enter a valid number.")
        return

    if category_number < 1 or category_number > len(CATEGORIES):
        print("Invalid category number.")
        return

    category = CATEGORIES[category_number - 1]
    description = input("Description: ")
    if description == "":
        description = "No description"
    description = description.replace("|", "/")

    try:
        amount = float(input("Amount: "))
    except:
        print("Please enter a valid number.")
        return

    if amount <= 0:
        print("Expense amount must be greater than 0.")
        return

    expense = Expense(day, category, description, amount)
    trip.add_expense(expense)

    print("Expense added successfully.")
    day_total = trip.day_total(day)
    if day_total > trip.daily_budget:
        print("Warning: You have exceeded the daily budget for this day.")
    print("Day " + str(day) + " total: $" + format(day_total, ".2f") + " AUD")
    print_budget_summary(trip)


def view_all_expenses(trips):
    if len(trips) == 0:
        print("Please create or load a travel plan first.")
        return

    if len(trips) == 1:
        trip = trips[0]
    else:
        print()
        print("Choose a travel plan:")
        for i in range(len(trips)):
            trip = trips[i]
            print(str(i + 1) + ". " + trip.destination + " | " + str(trip.days) + " days | $" + format(trip.total_budget, ".2f") + " AUD")

        try:
            plan_number = int(input("Plan number: "))
        except:
            print("Please enter a valid number.")
            return

        if plan_number < 1 or plan_number > len(trips):
            print("Invalid plan number.")
            return

        trip = trips[plan_number - 1]

    if len(trip.expenses) == 0:
        print("No expenses recorded yet.")
        print_budget_summary(trip)
        return

    print()
    print("All Expenses for " + trip.destination)
    for i in range(len(trip.expenses)):
        expense = trip.expenses[i]
        print(str(i + 1) + ". Day " + str(expense.day) + " | " + expense.category + " | " + expense.description + " | $" + format(expense.amount, ".2f") + " AUD")

    print_budget_summary(trip)


def view_expenses_by_category(trips):
    if len(trips) == 0:
        print("Please create or load a travel plan first.")
        return

    if len(trips) == 1:
        trip = trips[0]
    else:
        print()
        print("Choose a travel plan:")
        for i in range(len(trips)):
            trip = trips[i]
            print(str(i + 1) + ". " + trip.destination + " | " + str(trip.days) + " days | $" + format(trip.total_budget, ".2f") + " AUD")

        try:
            plan_number = int(input("Plan number: "))
        except:
            print("Please enter a valid number.")
            return

        if plan_number < 1 or plan_number > len(trips):
            print("Invalid plan number.")
            return

        trip = trips[plan_number - 1]

    print()
    print("Expenses by Category for " + trip.destination)
    for category in CATEGORIES:
        total = 0
        for expense in trip.expenses:
            if expense.category == category:
                total = total + expense.amount
        print(category + ": $" + format(total, ".2f") + " AUD")


def delete_expense(trips):
    if len(trips) == 0:
        print("Please create or load a travel plan first.")
        return

    if len(trips) == 1:
        trip = trips[0]
    else:
        print()
        print("Choose a travel plan:")
        for i in range(len(trips)):
            trip = trips[i]
            print(str(i + 1) + ". " + trip.destination + " | " + str(trip.days) + " days | $" + format(trip.total_budget, ".2f") + " AUD")

        try:
            plan_number = int(input("Plan number: "))
        except:
            print("Please enter a valid number.")
            return

        if plan_number < 1 or plan_number > len(trips):
            print("Invalid plan number.")
            return

        trip = trips[plan_number - 1]

    if len(trip.expenses) == 0:
        print("No expenses recorded yet.")
        return

    print()
    print("All Expenses for " + trip.destination)
    for i in range(len(trip.expenses)):
        expense = trip.expenses[i]
        print(str(i + 1) + ". Day " + str(expense.day) + " | " + expense.category + " | " + expense.description + " | $" + format(expense.amount, ".2f") + " AUD")

    try:
        expense_number = int(input("Expense number to delete: "))
    except:
        print("Please enter a valid number.")
        return

    if expense_number < 1 or expense_number > len(trip.expenses):
        print("Invalid expense number.")
        return

    deleted_expense = trip.expenses.pop(expense_number - 1)
    print("Deleted: " + deleted_expense.description)


def save_data(trips):
    if len(trips) == 0:
        print("Please create or load a travel plan first.")
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
        print("Data saved successfully to " + DATA_FILE + ".")
    except:
        print("Could not save data.")


def load_data():
    trips = []
    current_trip = None

    try:
        file = open(DATA_FILE, "r")
        lines = file.readlines()
        file.close()
    except:
        print("Could not load data. The file does not exist.")
        return trips

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

    print("Data loaded successfully from " + DATA_FILE + ".")
    return trips


def main():
    trips = []
    print("Welcome to TripWise!")

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            create_trip(trips)
        elif choice == "2":
            view_travel_plans(trips)
        elif choice == "3":
            add_expense(trips)
        elif choice == "4":
            view_all_expenses(trips)
        elif choice == "5":
            view_expenses_by_category(trips)
        elif choice == "6":
            save_data(trips)
        elif choice == "7":
            trips = load_data()
        elif choice == "8":
            delete_expense(trips)
        elif choice == "9":
            print("Thank you for using TripWise. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main()
