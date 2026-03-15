"""
╔══════════════════════════════════════════════════════════════════╗
║           Personal Finance Tracker v2.1                          ║
║           Author: Spoorti Inganalli                              ║
║           GitHub: github.com/Spoorti-I                          ║
║           Tech: Python | Pandas | Matplotlib | Scikit-learn     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import csv
import json
from datetime import datetime, date
from collections import defaultdict

# Optional rich libraries — gracefully degrade if not installed
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from sklearn.linear_model import LinearRegression
    PANDAS_AVAILABLE = True
    ML_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    ML_AVAILABLE = False

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
DATA_FILE = "transactions.csv"
BUDGET_FILE = "budgets.json"
GOALS_FILE = "savings_goals.json"
CATEGORIES = [
    "Food & Dining", "Transport", "Shopping", "Entertainment",
    "Health & Medical", "Education", "Utilities", "Rent/EMI",
    "Savings/Investment", "Salary/Income", "Freelance", "Other"
]
COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
    "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9",
    "#82E0AA", "#F0B27A"
]

# ─────────────────────────────────────────────
#  DATA LAYER
# ─────────────────────────────────────────────

def initialize_files():
    """Create CSV and budget JSON if they don't exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "type", "category", "amount", "description", "tags"])
        print(f"  ✅ Created {DATA_FILE}")

    if not os.path.exists(BUDGET_FILE):
        default_budgets = {cat: 0 for cat in CATEGORIES}
        with open(BUDGET_FILE, "w") as f:
            json.dump(default_budgets, f, indent=2)
        print(f"  ✅ Created {BUDGET_FILE}")

    if not os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, "w") as f:
            json.dump([], f)
        print(f"  ✅ Created {GOALS_FILE}")


def load_transactions():
    """Load all transactions. Returns a list of dicts."""
    transactions = []
    if not os.path.exists(DATA_FILE):
        return transactions
    with open(DATA_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            transactions.append(row)
    return transactions


def save_transaction(txn: dict):
    """Append a single transaction to CSV."""
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "type", "category", "amount", "description", "tags"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(txn)


def load_budgets():
    """Load budget limits from JSON."""
    if not os.path.exists(BUDGET_FILE):
        return {}
    with open(BUDGET_FILE, "r") as f:
        return json.load(f)


def save_budgets(budgets: dict):
    """Save budget limits to JSON."""
    with open(BUDGET_FILE, "w") as f:
        json.dump(budgets, f, indent=2)


def get_next_id(transactions):
    """Auto-increment transaction ID."""
    if not transactions:
        return 1
    return max(int(t["id"]) for t in transactions) + 1


# ─────────────────────────────────────────────
#  CORE FEATURES
# ─────────────────────────────────────────────

def add_transaction():
    """Interactive: add income or expense."""
    print("\n" + "─" * 50)
    print("  ➕ ADD TRANSACTION")
    print("─" * 50)

    # Type
    print("  Type:  1. Income   2. Expense")
    choice = input("  Select (1/2): ").strip()
    txn_type = "Income" if choice == "1" else "Expense"

    # Category
    print(f"\n  Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i:2}. {cat}")
    cat_choice = int(input("  Select category number: ").strip()) - 1
    category = CATEGORIES[cat_choice] if 0 <= cat_choice < len(CATEGORIES) else "Other"

    # Amount
    amount = float(input("  Amount (₹): ").strip())

    # Description
    description = input("  Description: ").strip()

    # Tags (optional)
    tags = input("  Tags (comma-separated, optional): ").strip()

    # Date
    date_input = input("  Date (YYYY-MM-DD) [Enter for today]: ").strip()
    txn_date = date_input if date_input else str(date.today())

    transactions = load_transactions()
    txn = {
        "id": get_next_id(transactions),
        "date": txn_date,
        "type": txn_type,
        "category": category,
        "amount": amount,
        "description": description,
        "tags": tags
    }
    save_transaction(txn)
    print(f"\n  ✅ {txn_type} of ₹{amount:.2f} ({category}) saved! [ID: {txn['id']}]")


def view_transactions(filter_month=None):
    """Display all (or monthly) transactions in a formatted table."""
    transactions = load_transactions()
    if filter_month:
        transactions = [t for t in transactions if t["date"].startswith(filter_month)]

    if not transactions:
        print("\n  ⚠️  No transactions found.")
        return

    print("\n" + "─" * 80)
    print(f"  {'ID':<5} {'Date':<12} {'Type':<10} {'Category':<22} {'Amount':>10}  Description")
    print("─" * 80)
    total_income = 0
    total_expense = 0
    for t in transactions:
        sign = "+" if t["type"] == "Income" else "-"
        color_flag = "🟢" if t["type"] == "Income" else "🔴"
        print(f"  {t['id']:<5} {t['date']:<12} {color_flag} {t['type']:<8} {t['category']:<22} {sign}₹{t['amount']:>8.2f}  {t['description']}")
        if t["type"] == "Income":
            total_income += t["amount"]
        else:
            total_expense += t["amount"]
    print("─" * 80)
    net = total_income - total_expense
    net_icon = "✅" if net >= 0 else "⚠️ "
    print(f"  {'':5} {'':12} {'Total Income':>32}  +₹{total_income:,.2f}")
    print(f"  {'':5} {'':12} {'Total Expense':>32}  -₹{total_expense:,.2f}")
    print(f"  {'':5} {'':12} {net_icon} {'Net Savings':>30}   ₹{net:,.2f}")
    print("─" * 80)


def summary_dashboard():
    """Rich text dashboard: monthly summary, budget alerts, category breakdown."""
    transactions = load_transactions()
    if not transactions:
        print("\n  ⚠️  No data yet. Add some transactions first!")
        return

    budgets = load_budgets()
    current_month = datetime.now().strftime("%Y-%m")
    monthly = [t for t in transactions if t["date"].startswith(current_month)]

    income = sum(t["amount"] for t in monthly if t["type"] == "Income")
    expense = sum(t["amount"] for t in monthly if t["type"] == "Expense")
    savings = income - expense
    savings_rate = (savings / income * 100) if income > 0 else 0

    print("\n" + "═" * 55)
    print(f"  📊  FINANCE DASHBOARD — {datetime.now().strftime('%B %Y')}")
    print("═" * 55)
    print(f"  💰  Total Income   :  ₹{income:>10,.2f}")
    print(f"  💸  Total Expenses :  ₹{expense:>10,.2f}")
    print(f"  🏦  Net Savings    :  ₹{savings:>10,.2f}  ({savings_rate:.1f}%)")

    # Category breakdown
    cat_expense = defaultdict(float)
    for t in monthly:
        if t["type"] == "Expense":
            cat_expense[t["category"]] += t["amount"]

    if cat_expense:
        print("\n  📂  Expense Breakdown:")
        print("  " + "─" * 50)
        for cat, amt in sorted(cat_expense.items(), key=lambda x: -x[1]):
            bar_len = int((amt / expense) * 25) if expense > 0 else 0
            bar = "█" * bar_len
            budget = budgets.get(cat, 0)
            over = " ⚠️  OVER BUDGET!" if budget > 0 and amt > budget else ""
            print(f"  {cat:<22} ₹{amt:>8,.2f}  {bar}{over}")

    # Budget status
    print("\n  🎯  Budget Status:")
    print("  " + "─" * 50)
    has_budget = False
    for cat, limit in budgets.items():
        if limit > 0:
            spent = cat_expense.get(cat, 0)
            pct = (spent / limit * 100)
            status = "✅" if pct < 80 else ("⚠️ " if pct < 100 else "🚨")
            print(f"  {status} {cat:<22} ₹{spent:>7,.2f} / ₹{limit:,.2f}  ({pct:.0f}%)")
            has_budget = True
    if not has_budget:
        print("  No budgets set. Use option 5 to set budgets.")

    print("═" * 55)


def set_budgets():
    """Set monthly budget limits per category."""
    print("\n" + "─" * 50)
    print("  🎯 SET MONTHLY BUDGETS")
    print("─" * 50)
    budgets = load_budgets()
    for i, cat in enumerate(CATEGORIES, 1):
        current = budgets.get(cat, 0)
        val = input(f"  {i:2}. {cat:<22} [Current: ₹{current:,.0f}] New limit (Enter to skip): ").strip()
        if val:
            budgets[cat] = float(val)
    save_budgets(budgets)
    print("\n  ✅ Budgets saved!")


def search_transactions():
    """Search/filter transactions by keyword, category, or date range."""
    print("\n  🔍 SEARCH TRANSACTIONS")
    keyword = input("  Keyword (description/tags, Enter to skip): ").strip().lower()
    category = input("  Category filter (Enter to skip): ").strip()
    start = input("  Start date YYYY-MM-DD (Enter to skip): ").strip()
    end = input("  End date YYYY-MM-DD (Enter to skip): ").strip()

    transactions = load_transactions()
    results = []
    for t in transactions:
        if keyword and keyword not in t["description"].lower() and keyword not in t["tags"].lower():
            continue
        if category and category.lower() not in t["category"].lower():
            continue
        if start and t["date"] < start:
            continue
        if end and t["date"] > end:
            continue
        results.append(t)

    print(f"\n  Found {len(results)} transaction(s):")
    for t in results:
        sign = "+" if t["type"] == "Income" else "-"
        print(f"  [{t['date']}] {t['category']:<20} {sign}₹{t['amount']:.2f}  {t['description']}")


def delete_transaction():
    """Delete a transaction by ID."""
    txn_id = input("\n  Enter transaction ID to delete: ").strip()
    transactions = load_transactions()
    new_list = [t for t in transactions if str(t["id"]) != txn_id]
    if len(new_list) == len(transactions):
        print(f"  ⚠️  Transaction ID {txn_id} not found.")
        return
    with open(DATA_FILE, "w", newline="") as f:
        if new_list:
            writer = csv.DictWriter(f, fieldnames=new_list[0].keys())
            writer.writeheader()
            writer.writerows(new_list)
        else:
            f.write("id,date,type,category,amount,description,tags\n")
    print(f"  ✅ Transaction {txn_id} deleted.")


# ─────────────────────────────────────────────
#  PANDAS ANALYTICS (if available)
# ─────────────────────────────────────────────

def analytics_pandas():
    """Advanced analytics using Pandas — monthly trends, category stats."""
    if not PANDAS_AVAILABLE:
        print("\n  ⚠️  Pandas not installed. Run: pip install pandas numpy")
        return

    transactions = load_transactions()
    if not transactions:
        print("\n  ⚠️  No data available for analysis.")
        return

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    print("\n" + "═" * 55)
    print("  📈  PANDAS ANALYTICS REPORT")
    print("═" * 55)

    # Monthly summary
    monthly = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
    print("\n  📅  Monthly Income vs Expense:")
    print("  " + "─" * 48)
    for month, row in monthly.iterrows():
        inc = row.get("Income", 0)
        exp = row.get("Expense", 0)
        net = inc - exp
        flag = "✅" if net >= 0 else "⚠️ "
        print(f"  {flag} {str(month):<12}  Income: ₹{inc:>8,.0f}  Expense: ₹{exp:>8,.0f}  Net: ₹{net:>8,.0f}")

    # Top spending categories
    expense_df = df[df["type"] == "Expense"]
    if not expense_df.empty:
        top_cats = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False).head(5)
        print("\n  🏆  Top 5 Spending Categories (All Time):")
        print("  " + "─" * 40)
        for cat, total in top_cats.items():
            print(f"  {'💸'} {cat:<25}  ₹{total:>8,.2f}")

    # Descriptive stats
    print("\n  📊  Descriptive Statistics:")
    print("  " + "─" * 40)
    for txn_type in ["Income", "Expense"]:
        subset = df[df["type"] == txn_type]["amount"]
        if not subset.empty:
            print(f"\n  {txn_type}:")
            print(f"    Count   : {len(subset)}")
            print(f"    Total   : ₹{subset.sum():,.2f}")
            print(f"    Average : ₹{subset.mean():,.2f}")
            print(f"    Median  : ₹{subset.median():,.2f}")
            print(f"    Largest : ₹{subset.max():,.2f}")

    print("═" * 55)


# ─────────────────────────────────────────────
#  CHARTS (Matplotlib)
# ─────────────────────────────────────────────

def generate_charts():
    """Generate and save charts using Matplotlib."""
    if not PANDAS_AVAILABLE:
        print("\n  ⚠️  Install matplotlib: pip install matplotlib")
        return

    transactions = load_transactions()
    if not transactions:
        print("\n  ⚠️  No data to chart.")
        return

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Personal Finance Dashboard", fontsize=16, fontweight="bold", color="#2C3E50")
    fig.patch.set_facecolor("#F8F9FA")

    # 1. Monthly Income vs Expense (Bar)
    ax1 = axes[0, 0]
    monthly = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
    x = range(len(monthly))
    width = 0.35
    ax1.bar([i - width/2 for i in x], monthly.get("Income", [0]*len(monthly)), width, label="Income", color="#2ECC71", alpha=0.85)
    ax1.bar([i + width/2 for i in x], monthly.get("Expense", [0]*len(monthly)), width, label="Expense", color="#E74C3C", alpha=0.85)
    ax1.set_title("Monthly Income vs Expense", fontweight="bold")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(monthly.index, rotation=30, ha="right", fontsize=8)
    ax1.legend()
    ax1.set_ylabel("Amount (₹)")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"₹{v:,.0f}"))
    ax1.set_facecolor("#FAFAFA")

    # 2. Expense by Category (Pie)
    ax2 = axes[0, 1]
    expense_df = df[df["type"] == "Expense"]
    if not expense_df.empty:
        cat_totals = expense_df.groupby("category")["amount"].sum()
        wedges, texts, autotexts = ax2.pie(
            cat_totals, labels=None, autopct="%1.1f%%",
            colors=COLORS[:len(cat_totals)], startangle=140,
            pctdistance=0.82, wedgeprops={"edgecolor": "white", "linewidth": 1.5}
        )
        for at in autotexts:
            at.set_fontsize(8)
        ax2.legend(wedges, cat_totals.index, loc="lower left", fontsize=7, bbox_to_anchor=(-0.1, -0.1))
        ax2.set_title("Expense Distribution", fontweight="bold")

    # 3. Net Savings Trend (Line)
    ax3 = axes[1, 0]
    monthly_inc = df[df["type"] == "Income"].groupby("month")["amount"].sum()
    monthly_exp = df[df["type"] == "Expense"].groupby("month")["amount"].sum()
    all_months = sorted(set(monthly_inc.index) | set(monthly_exp.index))
    savings = [monthly_inc.get(m, 0) - monthly_exp.get(m, 0) for m in all_months]
    colors_line = ["#27AE60" if s >= 0 else "#E74C3C" for s in savings]
    ax3.bar(all_months, savings, color=colors_line, alpha=0.8)
    ax3.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax3.set_title("Monthly Net Savings", fontweight="bold")
    ax3.set_ylabel("Amount (₹)")
    ax3.set_xticklabels(all_months, rotation=30, ha="right", fontsize=8)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"₹{v:,.0f}"))
    ax3.set_facecolor("#FAFAFA")

    # 4. Cumulative Savings (Area)
    ax4 = axes[1, 1]
    cumulative = [sum(savings[:i+1]) for i in range(len(savings))]
    ax4.fill_between(all_months, cumulative, alpha=0.3, color="#3498DB")
    ax4.plot(all_months, cumulative, "o-", color="#2980B9", linewidth=2, markersize=5)
    ax4.set_title("Cumulative Savings Over Time", fontweight="bold")
    ax4.set_ylabel("Amount (₹)")
    ax4.set_xticklabels(all_months, rotation=30, ha="right", fontsize=8)
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"₹{v:,.0f}"))
    ax4.set_facecolor("#FAFAFA")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    chart_file = "finance_charts.png"
    plt.savefig(chart_file, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"\n  ✅ Charts saved as '{chart_file}'")


# ─────────────────────────────────────────────
#  ML: SPENDING PREDICTION (Scikit-learn)
# ─────────────────────────────────────────────

def predict_spending():
    """Use Linear Regression to predict next month's expenses."""
    if not ML_AVAILABLE or not PANDAS_AVAILABLE:
        print("\n  ⚠️  Install scikit-learn: pip install scikit-learn")
        return

    transactions = load_transactions()
    if len(transactions) < 4:
        print("\n  ⚠️  Need at least 4 months of data for prediction.")
        return

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    monthly_exp = df[df["type"] == "Expense"].groupby("month")["amount"].sum().reset_index()
    monthly_exp.columns = ["month", "expense"]
    monthly_exp["month_num"] = range(len(monthly_exp))

    if len(monthly_exp) < 3:
        print("\n  ⚠️  Not enough monthly expense data for prediction.")
        return

    X = monthly_exp[["month_num"]].values
    y = monthly_exp["expense"].values

    model = LinearRegression()
    model.fit(X, y)
    next_month_num = len(monthly_exp)
    predicted = model.predict([[next_month_num]])[0]
    r2 = model.score(X, y)

    print("\n" + "═" * 50)
    print("  🤖  ML SPENDING PREDICTION (Linear Regression)")
    print("═" * 50)
    print(f"  Training months : {len(monthly_exp)}")
    print(f"  Model R² Score  : {r2:.3f} ({'Good fit' if r2 > 0.7 else 'Low confidence'})")
    print(f"\n  📅  Historical monthly expenses:")
    for _, row in monthly_exp.iterrows():
        print(f"     {str(row['month']):<12}  ₹{row['expense']:>8,.2f}")
    print(f"\n  🔮  Predicted next month's expense:  ₹{max(0, predicted):,.2f}")
    print(f"  ⚠️  Note: Prediction is based on trend only. Actual may vary.")
    print("═" * 50)


# ─────────────────────────────────────────────
#  EXPORT
# ─────────────────────────────────────────────

def export_to_csv():
    """Export filtered transactions to a new CSV file."""
    month = input("\n  Export month (YYYY-MM) or Enter for all: ").strip()
    transactions = load_transactions()
    if month:
        transactions = [t for t in transactions if t["date"].startswith(month)]
    filename = f"export_{month or 'all'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as f:
        if transactions:
            writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
            writer.writeheader()
            writer.writerows(transactions)
    print(f"\n  ✅ Exported {len(transactions)} transactions to '{filename}'")


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

def print_banner():
    print("\n" + "═" * 55)
    print("  💰  Personal Finance Tracker v2.1")
    print("  👩‍💻  by Spoorti Inganalli | github.com/Spoorti-I")
    print("  🐍  Python | Pandas | Matplotlib | Scikit-learn")
    print("═" * 55)


# ─────────────────────────────────────────────
#  SAVINGS GOAL TRACKER
# ─────────────────────────────────────────────

# load goals from json file
def load_goals():
    if not os.path.exists(GOALS_FILE):
        return []
    with open(GOALS_FILE, "r") as f:
        return json.load(f)

# save goals back to json
def save_goals(goals):
    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, indent=2)

# figure out how much user has saved so far (from Savings/Investment transactions)
def get_total_saved():
    transactions = load_transactions()
    total = 0.0
    for t in transactions:
        if t["type"] == "Income" and t["category"] == "Savings/Investment":
            total += t["amount"]
        elif t["type"] == "Expense" and t["category"] == "Savings/Investment":
            total += t["amount"]  # treat savings deposits as positive
    # actually let's just count all transactions tagged as savings
    total = sum(
        t["amount"] for t in transactions
        if t["category"] == "Savings/Investment" and t["type"] == "Income"
    )
    return total

def savings_goal_tracker():
    print("\n" + "═" * 55)
    print("  💰  SAVINGS GOAL TRACKER")
    print("═" * 55)

    goals = load_goals()

    # sub menu for goals
    print("\n  1. Add a new goal")
    print("  2. View all goals & progress")
    print("  3. Update saved amount for a goal")
    print("  4. Delete a goal")
    print("  0. Back")

    choice = input("\n  Choose: ").strip()

    if choice == "1":
        # add new goal
        print("\n  --- Add New Savings Goal ---")
        name = input("  Goal name (e.g. New Laptop, Trip to Goa): ").strip()
        if not name:
            print("  ⚠️  Name cannot be empty!")
            return

        try:
            target = float(input("  Target amount (₹): ").strip())
            saved = float(input("  Amount already saved (₹) [0 if starting fresh]: ").strip())
        except ValueError:
            print("  ⚠️  Please enter valid numbers.")
            return

        deadline = input("  Target date (YYYY-MM-DD) [optional, press Enter to skip]: ").strip()

        # create goal dict
        goal = {
            "id": len(goals) + 1,
            "name": name,
            "target": target,
            "saved": saved,
            "deadline": deadline if deadline else "No deadline",
            "created": str(date.today())
        }
        goals.append(goal)
        save_goals(goals)
        print(f"\n  ✅ Goal '{name}' added! Target: ₹{target:,.2f}")

    elif choice == "2":
        # show all goals with a simple progress bar
        if not goals:
            print("\n  No goals yet. Add one first!")
            return

        print("\n" + "─" * 55)
        for g in goals:
            pct = (g["saved"] / g["target"] * 100) if g["target"] > 0 else 0
            pct = min(pct, 100)  # cap at 100%
            remaining = max(0, g["target"] - g["saved"])

            # make a simple text progress bar
            filled = int(pct / 5)  # 20 blocks = 100%
            bar = "█" * filled + "░" * (20 - filled)

            # check if goal is done
            if pct >= 100:
                status = "🎉 COMPLETED!"
            elif pct >= 75:
                status = "🔥 Almost there!"
            elif pct >= 50:
                status = "💪 Halfway!"
            elif pct >= 25:
                status = "📈 Good start"
            else:
                status = "🚀 Just started"

            print(f"\n  🎯 Goal #{g['id']}: {g['name']}")
            print(f"     Target   : ₹{g['target']:>10,.2f}")
            print(f"     Saved    : ₹{g['saved']:>10,.2f}  ({pct:.1f}%)")
            print(f"     Remaining: ₹{remaining:>10,.2f}")
            print(f"     Deadline : {g['deadline']}")
            print(f"     Progress : [{bar}] {status}")

            # calculate how much to save per day if deadline is set
            if g["deadline"] != "No deadline":
                try:
                    dl = datetime.strptime(g["deadline"], "%Y-%m-%d").date()
                    days_left = (dl - date.today()).days
                    if days_left > 0 and remaining > 0:
                        daily = remaining / days_left
                        print(f"     💡 Save ₹{daily:.2f}/day to reach your goal!")
                    elif days_left <= 0:
                        print(f"     ⚠️  Deadline has passed!")
                except:
                    pass

        print("\n" + "─" * 55)

    elif choice == "3":
        # update saved amount
        if not goals:
            print("\n  No goals found.")
            return

        print("\n  Your goals:")
        for g in goals:
            print(f"    {g['id']}. {g['name']}  (saved: ₹{g['saved']:,.2f} / ₹{g['target']:,.2f})")

        try:
            gid = int(input("\n  Enter goal ID to update: ").strip())
            add_amt = float(input("  Amount to add to savings (₹): ").strip())
        except ValueError:
            print("  ⚠️  Invalid input.")
            return

        updated = False
        for g in goals:
            if g["id"] == gid:
                g["saved"] += add_amt
                updated = True
                pct = min((g["saved"] / g["target"] * 100), 100)
                print(f"\n  ✅ Updated! '{g['name']}' → ₹{g['saved']:,.2f} saved ({pct:.1f}%)")
                if g["saved"] >= g["target"]:
                    print(f"  🎉🎉 Congratulations! You've reached your goal: {g['name']}!")
                break

        if not updated:
            print("  ⚠️  Goal ID not found.")
            return

        save_goals(goals)

    elif choice == "4":
        # delete a goal
        if not goals:
            print("\n  No goals to delete.")
            return

        print("\n  Your goals:")
        for g in goals:
            print(f"    {g['id']}. {g['name']}")

        try:
            gid = int(input("\n  Enter goal ID to delete: ").strip())
        except ValueError:
            print("  ⚠️  Invalid input.")
            return

        new_goals = [g for g in goals if g["id"] != gid]
        if len(new_goals) == len(goals):
            print("  ⚠️  Goal not found.")
        else:
            save_goals(new_goals)
            print("  ✅ Goal deleted.")

    elif choice == "0":
        return
    else:
        print("  ⚠️  Invalid option.")


def main():
    initialize_files()
    print_banner()

    menu = {
        "1": ("➕  Add Transaction", add_transaction),
        "2": ("📋  View All Transactions", lambda: view_transactions()),
        "3": ("📆  View This Month", lambda: view_transactions(datetime.now().strftime("%Y-%m"))),
        "4": ("📊  Dashboard Summary", summary_dashboard),
        "5": ("🎯  Set Budgets", set_budgets),
        "6": ("🔍  Search Transactions", search_transactions),
        "7": ("🗑️   Delete Transaction", delete_transaction),
        "8": ("📈  Pandas Analytics", analytics_pandas),
        "9": ("📉  Generate Charts", generate_charts),
        "10": ("🤖  Predict Next Month (ML)", predict_spending),
        "11": ("💾  Export to CSV", export_to_csv),
        "12": ("💰  Savings Goal Tracker", savings_goal_tracker),
        "0": ("🚪  Exit", None),
    }

    while True:
        print("\n  ┌─────────────────────────────────┐")
        for key, (label, _) in menu.items():
            print(f"  │  {key:>2}.  {label:<28}│")
        print("  └─────────────────────────────────┘")

        choice = input("\n  Enter your choice: ").strip()

        if choice == "0":
            print("\n  👋  Thank you for using Finance Tracker! Goodbye.\n")
            break
        elif choice in menu:
            _, fn = menu[choice]
            try:
                fn()
            except (ValueError, IndexError) as e:
                print(f"\n  ❌ Input error: {e}. Please try again.")
            except KeyboardInterrupt:
                print("\n  ↩  Cancelled.")
        else:
            print("  ⚠️  Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
