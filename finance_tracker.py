#!/usr/bin/env python3
"""
Personal Finance Tracker
A comprehensive tool to track income, expenses, and generate financial reports.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import argparse


class Transaction:
    """Represents a financial transaction."""
    
    def __init__(self, amount: float, category: str, description: str, 
                 transaction_type: str, date: str = None):
        self.id = self._generate_id()
        self.amount = abs(amount)  # Store as positive, type determines sign
        self.category = category
        self.description = description
        self.transaction_type = transaction_type.lower()  # 'income' or 'expense'
        self.date = date or datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def _generate_id():
        """Generate a unique transaction ID."""
        return int(datetime.now().timestamp() * 1000000) % 1000000
    
    def to_dict(self):
        """Convert transaction to dictionary."""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'type': self.transaction_type,
            'date': self.date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create transaction from dictionary."""
        transaction = cls(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            transaction_type=data['type'],
            date=data['date']
        )
        transaction.id = data['id']
        return transaction


class FinanceTracker:
    """Main finance tracker application."""
    
    def __init__(self, data_file: str = "finance_data.json"):
        self.data_file = data_file
        self.transactions = []
        self.categories = {
            'income': ['Salary', 'Freelance', 'Investment', 'Gift', 'Other Income'],
            'expense': ['Food', 'Transportation', 'Entertainment', 'Bills', 'Shopping', 
                       'Healthcare', 'Education', 'Travel', 'Other Expense']
        }
        self.load_data()
    
    def load_data(self):
        """Load transactions from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    self.transactions = [Transaction.from_dict(t) for t in data.get('transactions', [])]
                    # Update categories with any custom ones from file
                    file_categories = data.get('categories', {})
                    for cat_type, cats in file_categories.items():
                        if cat_type in self.categories:
                            # Merge categories, keeping unique ones
                            self.categories[cat_type] = list(set(self.categories[cat_type] + cats))
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading data: {e}. Starting with empty data.")
    
    def save_data(self):
        """Save transactions to JSON file."""
        data = {
            'transactions': [t.to_dict() for t in self.transactions],
            'categories': self.categories
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=2)
    
    def add_transaction(self, amount: float, category: str, description: str, 
                       transaction_type: str, date: str = None):
        """Add a new transaction."""
        # Validate transaction type
        if transaction_type.lower() not in ['income', 'expense']:
            raise ValueError("Transaction type must be 'income' or 'expense'")
        
        # Add custom category if it doesn't exist
        if category not in self.categories[transaction_type.lower()]:
            self.categories[transaction_type.lower()].append(category)
        
        transaction = Transaction(amount, category, description, transaction_type, date)
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def get_transactions(self, start_date: str = None, end_date: str = None, 
                        category: str = None, transaction_type: str = None) -> List[Transaction]:
        """Get filtered transactions."""
        filtered = self.transactions.copy()
        
        if start_date:
            filtered = [t for t in filtered if t.date >= start_date]
        if end_date:
            filtered = [t for t in filtered if t.date <= end_date]
        if category:
            filtered = [t for t in filtered if t.category.lower() == category.lower()]
        if transaction_type:
            filtered = [t for t in filtered if t.transaction_type == transaction_type.lower()]
        
        return sorted(filtered, key=lambda x: x.date, reverse=True)
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction by ID."""
        original_length = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.id != transaction_id]
        if len(self.transactions) < original_length:
            self.save_data()
            return True
        return False
    
    def get_balance(self, start_date: str = None, end_date: str = None) -> Dict[str, float]:
        """Calculate balance for given period."""
        transactions = self.get_transactions(start_date, end_date)
        
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        balance = total_income - total_expenses
        
        return {
            'income': total_income,
            'expenses': total_expenses,
            'balance': balance
        }
    
    def get_category_summary(self, start_date: str = None, end_date: str = None) -> Dict[str, Dict[str, float]]:
        """Get spending summary by category."""
        transactions = self.get_transactions(start_date, end_date)
        
        summary = {'income': {}, 'expense': {}}
        
        for transaction in transactions:
            cat_type = transaction.transaction_type
            category = transaction.category
            
            if category not in summary[cat_type]:
                summary[cat_type][category] = 0
            summary[cat_type][category] += transaction.amount
        
        return summary
    
    def generate_report(self, period: str = 'month') -> str:
        """Generate a financial report."""
        if period == 'week':
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        elif period == 'month':
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        elif period == 'year':
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        else:
            start_date = None
        
        balance = self.get_balance(start_date)
        category_summary = self.get_category_summary(start_date)
        
        report = f"\n{'='*50}\n"
        report += f"FINANCIAL REPORT - {period.upper()}\n"
        report += f"{'='*50}\n\n"
        
        report += f"SUMMARY:\n"
        report += f"Total Income:    ${balance['income']:>10.2f}\n"
        report += f"Total Expenses:  ${balance['expenses']:>10.2f}\n"
        report += f"Net Balance:     ${balance['balance']:>10.2f}\n\n"
        
        # Income breakdown
        if category_summary['income']:
            report += "INCOME BY CATEGORY:\n"
            for category, amount in sorted(category_summary['income'].items(), 
                                         key=lambda x: x[1], reverse=True):
                report += f"  {category:<20} ${amount:>8.2f}\n"
            report += "\n"
        
        # Expense breakdown
        if category_summary['expense']:
            report += "EXPENSES BY CATEGORY:\n"
            for category, amount in sorted(category_summary['expense'].items(), 
                                         key=lambda x: x[1], reverse=True):
                report += f"  {category:<20} ${amount:>8.2f}\n"
        
        return report


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Personal Finance Tracker")
    parser.add_argument('--file', '-f', default='finance_data.json', 
                       help='Data file to use (default: finance_data.json)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add transaction command
    add_parser = subparsers.add_parser('add', help='Add a new transaction')
    add_parser.add_argument('amount', type=float, help='Transaction amount')
    add_parser.add_argument('type', choices=['income', 'expense'], help='Transaction type')
    add_parser.add_argument('category', help='Transaction category')
    add_parser.add_argument('description', help='Transaction description')
    add_parser.add_argument('--date', help='Transaction date (YYYY-MM-DD, default: today)')
    
    # List transactions command
    list_parser = subparsers.add_parser('list', help='List transactions')
    list_parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    list_parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--type', choices=['income', 'expense'], help='Filter by type')
    list_parser.add_argument('--limit', type=int, default=10, help='Number of transactions to show')
    
    # Delete transaction command
    delete_parser = subparsers.add_parser('delete', help='Delete a transaction')
    delete_parser.add_argument('id', type=int, help='Transaction ID to delete')
    
    # Balance command
    balance_parser = subparsers.add_parser('balance', help='Show balance')
    balance_parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    balance_parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate financial report')
    report_parser.add_argument('--period', choices=['week', 'month', 'year'], 
                              default='month', help='Report period')
    
    # Categories command
    categories_parser = subparsers.add_parser('categories', help='List available categories')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tracker = FinanceTracker(args.file)
    
    try:
        if args.command == 'add':
            transaction = tracker.add_transaction(
                amount=args.amount,
                category=args.category,
                description=args.description,
                transaction_type=args.type,
                date=args.date
            )
            print(f"Added {args.type}: ${args.amount:.2f} - {args.description} (ID: {transaction.id})")
        
        elif args.command == 'list':
            transactions = tracker.get_transactions(
                start_date=args.start,
                end_date=args.end,
                category=args.category,
                transaction_type=args.type
            )
            
            if not transactions:
                print("No transactions found.")
                return
            
            print(f"\n{'ID':<8} {'Date':<12} {'Type':<8} {'Category':<15} {'Amount':<10} Description")
            print("-" * 70)
            
            for transaction in transactions[:args.limit]:
                sign = "+" if transaction.transaction_type == 'income' else "-"
                print(f"{transaction.id:<8} {transaction.date:<12} {transaction.transaction_type:<8} "
                      f"{transaction.category:<15} {sign}${transaction.amount:<9.2f} {transaction.description}")
        
        elif args.command == 'delete':
            if tracker.delete_transaction(args.id):
                print(f"Transaction {args.id} deleted successfully.")
            else:
                print(f"Transaction {args.id} not found.")
        
        elif args.command == 'balance':
            balance = tracker.get_balance(args.start, args.end)
            print(f"\nFINANCIAL SUMMARY")
            print("-" * 20)
            print(f"Total Income:   ${balance['income']:>10.2f}")
            print(f"Total Expenses: ${balance['expenses']:>10.2f}")
            print(f"Net Balance:    ${balance['balance']:>10.2f}")
        
        elif args.command == 'report':
            report = tracker.generate_report(args.period)
            print(report)
        
        elif args.command == 'categories':
            print("\nAVAILABLE CATEGORIES:")
            print("\nIncome Categories:")
            for cat in tracker.categories['income']:
                print(f"  - {cat}")
            print("\nExpense Categories:")
            for cat in tracker.categories['expense']:
                print(f"  - {cat}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
