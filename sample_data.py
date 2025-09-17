#!/usr/bin/env python3
"""
Sample Data Generator for Finance Tracker
Creates realistic sample transactions for testing and demonstration purposes.
"""

import random
from datetime import datetime, timedelta
from finance_tracker import FinanceTracker


def generate_sample_data(tracker, num_transactions=50):
    """Generate sample transactions for the past few months."""
    
    # Sample data categories and descriptions
    income_data = {
        'Salary': ['Monthly salary', 'Bonus payment', 'Overtime pay'],
        'Freelance': ['Web development project', 'Consulting work', 'Design project'],
        'Investment': ['Stock dividends', 'Bond interest', 'Crypto gains'],
        'Gift': ['Birthday money', 'Holiday gift', 'Tax refund']
    }
    
    expense_data = {
        'Food': ['Grocery shopping', 'Restaurant dinner', 'Coffee', 'Fast food lunch', 'Takeout'],
        'Transportation': ['Gas', 'Bus ticket', 'Uber ride', 'Parking fee', 'Car maintenance'],
        'Entertainment': ['Movie tickets', 'Concert', 'Streaming service', 'Books', 'Video games'],
        'Bills': ['Rent', 'Electricity', 'Internet', 'Phone bill', 'Insurance'],
        'Shopping': ['Clothes', 'Electronics', 'Home supplies', 'Gifts for others'],
        'Healthcare': ['Doctor visit', 'Prescription', 'Dental checkup', 'Pharmacy'],
        'Education': ['Course fee', 'Books', 'Online subscription', 'Workshop'],
        'Travel': ['Flight ticket', 'Hotel', 'Vacation expenses', 'Gas for road trip']
    }
    
    # Generate random dates for the past 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    transactions_added = 0
    
    for _ in range(num_transactions):
        # Random date within the range
        random_days = random.randint(0, 90)
        transaction_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        
        # Decide if it's income or expense (80% expense, 20% income for realism)
        if random.random() < 0.2:  # 20% chance of income
            transaction_type = 'income'
            category = random.choice(list(income_data.keys()))
            description = random.choice(income_data[category])
            
            # Income amounts
            if category == 'Salary':
                amount = random.uniform(2000, 5000)
            elif category == 'Freelance':
                amount = random.uniform(200, 1500)
            elif category == 'Investment':
                amount = random.uniform(50, 500)
            else:  # Gift
                amount = random.uniform(25, 300)
        else:  # Expense
            transaction_type = 'expense'
            category = random.choice(list(expense_data.keys()))
            description = random.choice(expense_data[category])
            
            # Expense amounts based on category
            if category == 'Food':
                amount = random.uniform(5, 150)
            elif category == 'Transportation':
                amount = random.uniform(3, 80)
            elif category == 'Entertainment':
                amount = random.uniform(10, 100)
            elif category == 'Bills':
                amount = random.uniform(50, 1200)
            elif category == 'Shopping':
                amount = random.uniform(20, 300)
            elif category == 'Healthcare':
                amount = random.uniform(15, 250)
            elif category == 'Education':
                amount = random.uniform(25, 500)
            else:  # Travel
                amount = random.uniform(50, 1000)
        
        try:
            tracker.add_transaction(
                amount=round(amount, 2),
                category=category,
                description=description,
                transaction_type=transaction_type,
                date=transaction_date
            )
            transactions_added += 1
        except Exception as e:
            print(f"Error adding transaction: {e}")
    
    return transactions_added


def main():
    """Main function to generate sample data."""
    print("Finance Tracker Sample Data Generator")
    print("=" * 40)
    
    # Ask user for confirmation
    response = input("This will create sample transactions. Continue? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Ask for number of transactions
    try:
        num_transactions = input("Number of sample transactions to generate (default: 50): ")
        num_transactions = int(num_transactions) if num_transactions else 50
    except ValueError:
        num_transactions = 50
    
    # Create tracker with sample data file
    tracker = FinanceTracker("sample_finance_data.json")
    
    print(f"Generating {num_transactions} sample transactions...")
    
    # Generate the sample data
    added = generate_sample_data(tracker, num_transactions)
    
    print(f"Successfully generated {added} sample transactions!")
    print(f"Data saved to: sample_finance_data.json")
    print("\nYou can now test the finance tracker with:")
    print("python finance_tracker.py --file sample_finance_data.json list")
    print("python finance_tracker.py --file sample_finance_data.json balance")
    print("python finance_tracker.py --file sample_finance_data.json report")
    
    # Show a quick summary
    balance = tracker.get_balance()
    print(f"\nSample Data Summary:")
    print(f"Total Income:   ${balance['income']:>10.2f}")
    print(f"Total Expenses: ${balance['expenses']:>10.2f}")
    print(f"Net Balance:    ${balance['balance']:>10.2f}")


if __name__ == "__main__":
    main()
