"""
sample_data.py — Seeds the database with realistic sample transactions.
Run once: python sample_data.py
"""

from database import Database, Transaction


def seed():
    db = Database("finance_tracker.db")

    samples = [
        # Income
        Transaction(45000, "Salary",        "income",  "Monthly salary",        "2025-01-01"),
        Transaction(8000,  "Freelance",      "income",  "Web project payment",   "2025-01-10"),
        Transaction(45000, "Salary",        "income",  "Monthly salary",        "2025-02-01"),
        Transaction(2500,  "Investment",     "income",  "Mutual fund dividend",  "2025-02-15"),
        Transaction(45000, "Salary",        "income",  "Monthly salary",        "2025-03-01"),

        # Expenses
        Transaction(12000, "Rent",           "expense", "Monthly rent",          "2025-01-02"),
        Transaction(3200,  "Food",           "expense", "Groceries + Swiggy",    "2025-01-05"),
        Transaction(1500,  "Transport",      "expense", "Ola/Uber + fuel",       "2025-01-08"),
        Transaction(800,   "Utilities",      "expense", "Electricity bill",      "2025-01-09"),
        Transaction(2200,  "Shopping",       "expense", "Clothes - Myntra",      "2025-01-14"),
        Transaction(600,   "Health",         "expense", "Pharmacy",              "2025-01-20"),
        Transaction(999,   "Entertainment",  "expense", "Netflix + Spotify",     "2025-01-25"),

        Transaction(12000, "Rent",           "expense", "Monthly rent",          "2025-02-02"),
        Transaction(2800,  "Food",           "expense", "Groceries",             "2025-02-06"),
        Transaction(1200,  "Transport",      "expense", "Metro + cab",           "2025-02-10"),
        Transaction(1500,  "Education",      "expense", "Udemy course",          "2025-02-12"),
        Transaction(850,   "Utilities",      "expense", "Internet + water",      "2025-02-18"),
        Transaction(3500,  "Health",         "expense", "Doctor + medicines",    "2025-02-22"),

        Transaction(12000, "Rent",           "expense", "Monthly rent",          "2025-03-02"),
        Transaction(3100,  "Food",           "expense", "Groceries + dining",   "2025-03-07"),
        Transaction(1800,  "Transport",      "expense", "Petrol + parking",      "2025-03-11"),
        Transaction(4200,  "Shopping",       "expense", "Electronics",           "2025-03-15"),
        Transaction(999,   "Entertainment",  "expense", "OTT subscriptions",     "2025-03-20"),
    ]

    for t in samples:
        db.add(t)

    print(f"✅ Seeded {len(samples)} transactions into finance_tracker.db")


if __name__ == "__main__":
    seed()
