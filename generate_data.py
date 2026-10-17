import random
from datetime import date, timedelta

import pandas as pd


# Make the dataset reproducible
random.seed(42)

# Expense categories and their sample descriptions
expense_options = {
    "Food": {
        "descriptions": [
            "Breakfast",
            "Lunch",
            "Dinner",
            "Evening snacks",
            "Tea and coffee"
        ],
        "min_amount": 20,
        "max_amount": 350
    },
    "Travel": {
        "descriptions": [
            "Bus fare",
            "Auto fare",
            "Train ticket",
            "Cab ride"
        ],
        "min_amount": 20,
        "max_amount": 300
    },
    "Fuel": {
        "descriptions": [
            "Petrol"
        ],
        "min_amount": 100,
        "max_amount": 1200
    },
    "Education": {
        "descriptions": [
            "Notebook",
            "Books",
            "Online course",
            "Stationery"
        ],
        "min_amount": 30,
        "max_amount": 1500
    },
    "Shopping": {
        "descriptions": [
            "Clothes",
            "Accessories",
            "Shoes",
            "Household items"
        ],
        "min_amount": 100,
        "max_amount": 2500
    },
    "Bills": {
        "descriptions": [
            "Mobile recharge",
            "Electricity bill",
            "Internet bill"
        ],
        "min_amount": 100,
        "max_amount": 1500
    },
    "Entertainment": {
        "descriptions": [
            "Movie ticket",
            "Game subscription",
            "Streaming subscription"
        ],
        "min_amount": 100,
        "max_amount": 800
    },
    "Health": {
        "descriptions": [
            "Medicines",
            "Doctor consultation",
            "Health checkup"
        ],
        "min_amount": 50,
        "max_amount": 1200
    },
    "Personal Care": {
        "descriptions": [
            "Haircut",
            "Toiletries",
            "Personal care products"
        ],
        "min_amount": 50,
        "max_amount": 700
    },
    "Other": {
        "descriptions": [
            "Miscellaneous expense",
            "Small purchase",
            "Unexpected expense"
        ],
        "min_amount": 20,
        "max_amount": 1000
    }
}

payment_methods = ["UPI", "Cash", "Card"]


# Generate dates from October to December 2026
start_date = date(2026, 10, 1)
end_date = date(2026, 12, 31)

records = []
current_date = start_date

while current_date <= end_date:

    # Generate 2 to 6 transactions per day
    transactions_today = random.randint(2, 6)

    for _ in range(transactions_today):

        category = random.choice(list(expense_options.keys()))
        category_details = expense_options[category]

        description = random.choice(
            category_details["descriptions"]
        )

        amount = random.randint(
            category_details["min_amount"],
            category_details["max_amount"]
        )

        payment_method = random.choice(payment_methods)

        records.append({
            "Date": current_date.isoformat(),
            "Category": category,
            "Description": description,
            "Amount": amount,
            "Payment_Method": payment_method
        })

    current_date += timedelta(days=1)


# Create a DataFrame
df = pd.DataFrame(records)

# Sort transactions by date
df = df.sort_values("Date").reset_index(drop=True)

# Save the generated dataset
df.to_csv("data/expenses_generated.csv", index=False)

# Display a summary
print("Expense dataset generated successfully!")
print("Total transactions:", len(df))
print("Start date:", df["Date"].min())
print("End date:", df["Date"].max())
print("Total expense:", df["Amount"].sum())

print("\nFirst 5 records:")
print(df.head())