# 💰 Personal Finance Tracker

> A Python-based personal finance management tool with data analytics, visualizations, and ML-powered spending predictions.

**Author:** Spoorti Inganalli · [LinkedIn](https://linkedin.com/in/spoortiinganalli) · [GitHub](https://github.com/Spoorti-I)  
**Stack:** Python · Pandas · NumPy · Matplotlib · Scikit-learn · CSV/JSON

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📝 **Transaction Management** | Add, view, search, and delete income/expense records |
| 📊 **Dashboard Summary** | Monthly income vs expense breakdown with budget alerts |
| 🎯 **Budget Tracker** | Set per-category budget limits with over-budget warnings |
| 📈 **Pandas Analytics** | Monthly trends, category stats, descriptive analysis |
| 📉 **Matplotlib Charts** | 4-panel visual dashboard — bar, pie, line, and area charts |
| 🤖 **ML Prediction** | Linear Regression model to predict next month's expenses |
| 💾 **CSV Export** | Export filtered transactions to CSV |
| 🔍 **Smart Search** | Filter by keyword, category, date range, and tags |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Spoorti-I/finance_tracker.git
cd finance_tracker
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python finance_tracker.py
```

---

## 📦 Requirements

```txt
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
scikit-learn>=1.3.0
```

> **Note:** The app works even without these libraries — it gracefully degrades to basic CSV-only mode. Analytics, charts, and ML features require the libraries above.

---

## 🖥️ Application Menu

```
  ┌─────────────────────────────────┐
  │   1.  ➕  Add Transaction       │
  │   2.  📋  View All Transactions │
  │   3.  📆  View This Month       │
  │   4.  📊  Dashboard Summary     │
  │   5.  🎯  Set Budgets           │
  │   6.  🔍  Search Transactions   │
  │   7.  🗑️   Delete Transaction   │
  │   8.  📈  Pandas Analytics      │
  │   9.  📉  Generate Charts       │
  │  10.  🤖  Predict Next Month    │
  │  11.  💾  Export to CSV         │
  │   0.  🚪  Exit                  │
  └─────────────────────────────────┘
```

---

## 📁 Project Structure

```
finance_tracker/
├── finance_tracker.py     # Main application
├── sample_data.py         # Script to load sample transactions
├── requirements.txt       # Python dependencies
├── transactions.csv       # Auto-created: all transaction records
├── budgets.json           # Auto-created: monthly budget limits
├── finance_charts.png     # Auto-generated: visualization dashboard
└── README.md
```

---

## 📊 Charts Preview

The `Generate Charts` option creates a 4-panel dashboard:

1. **Monthly Income vs Expense** — grouped bar chart
2. **Expense by Category** — pie chart with percentages
3. **Monthly Net Savings** — color-coded bar (green = surplus, red = deficit)
4. **Cumulative Savings Over Time** — area chart

---

## 🤖 ML Spending Predictor

Uses **Linear Regression** (scikit-learn) trained on your historical monthly expenses to forecast next month's spending. Displays model R² score for confidence evaluation.

```
  🤖  ML SPENDING PREDICTION (Linear Regression)
  ═══════════════════════════════════════════════
  Training months : 6
  Model R² Score  : 0.872 (Good fit)

  📅  Historical monthly expenses:
     2025-10       ₹  8,200.00
     2025-11       ₹  9,100.00
     ...

  🔮  Predicted next month's expense:  ₹10,450.00
```

---

## 🏷️ Supported Categories

`Food & Dining` · `Transport` · `Shopping` · `Entertainment` · `Health & Medical` · `Education` · `Utilities` · `Rent/EMI` · `Savings/Investment` · `Salary/Income` · `Freelance` · `Other`

---

## 🛠️ Technologies Used

- **Python 3.x** — Core application logic
- **Pandas** — Data wrangling and monthly aggregation
- **NumPy** — Numerical operations
- **Matplotlib** — Data visualization (4 chart types)
- **Scikit-learn** — Linear Regression for expense forecasting
- **CSV / JSON** — Lightweight file-based storage

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---

## 🙋‍♀️ About the Author

**Spoorti Inganalli**  
BE Computer Science Engineering · KLE Institute of Technology, Hubli (VTU)  
6th Semester · Graduating June 2027

- 💼 [LinkedIn](https://linkedin.com/in/spoortiinganalli)
- 🐙 [GitHub](https://github.com/Spoorti-I)
- 📧 spoortiinganalli255@gmail.com

---

*Built with ❤️ using Python · Pandas · Matplotlib · Scikit-learn*
