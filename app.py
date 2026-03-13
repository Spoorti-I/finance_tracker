"""
app.py — Finance Tracker v3
User-friendly, mobile-first, guided flow.
Run: streamlit run app.py  OR  double-click RUN_ME.bat
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
from database import Database, Transaction

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="💰 My Finance Tracker",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Mobile-friendly CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Mobile-first base */
    .block-container { padding: 1rem 1rem 2rem; max-width: 800px; }

    /* Big friendly metric cards */
    .metric-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-card .amount {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    .metric-card .label {
        font-size: 0.85rem;
        margin: 4px 0 0;
        opacity: 0.85;
    }
    .card-income  { background: #d1fae5; color: #065f46; }
    .card-expense { background: #fee2e2; color: #991b1b; }
    .card-balance-pos { background: #dbeafe; color: #1e40af; }
    .card-balance-neg { background: #fef3c7; color: #92400e; }
    .card-count   { background: #f3e8ff; color: #6b21a8; }

    /* Step indicator */
    .step-pill {
        display: inline-block;
        background: #6366f1;
        color: white;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 8px;
    }

    /* Big action buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        width: 100%;
    }

    /* Transaction rows */
    .txn-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 8px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
    }
    .txn-row .txn-left { font-size: 0.9rem; }
    .txn-row .txn-cat  { font-size: 0.75rem; color: #6b7280; margin-top: 2px; }
    .txn-row .txn-amt  { font-size: 1.05rem; font-weight: 700; }
    .txn-inc { color: #059669; }
    .txn-exp { color: #dc2626; }

    /* Welcome card */
    .welcome-card {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .welcome-card h2 { font-size: 1.6rem; margin: 0 0 8px; }
    .welcome-card p  { opacity: 0.9; margin: 0; font-size: 0.95rem; }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        margin: 1.5rem 0 0.75rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Hide streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── DB Init ───────────────────────────────────────────────────────────────────
@st.cache_resource
def get_db():
    return Database("finance_tracker.db")

db = get_db()

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "show_add" not in st.session_state:
    st.session_state.show_add = False


# ── Helper: format currency ───────────────────────────────────────────────────
def fmt(amount):
    return f"₹{amount:,.0f}"


# ── Data ──────────────────────────────────────────────────────────────────────
summary      = db.get_summary()
transactions = db.get_all()
monthly      = db.get_monthly()
is_new_user  = len(transactions) == 0


# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════

# ── Welcome banner ────────────────────────────────────────────────────────────
if is_new_user:
    st.markdown("""
    <div class="welcome-card">
        <h2>👋 Welcome to Finance Tracker!</h2>
        <p>Track your money in seconds. Add your first transaction below to get started.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    today = datetime.now().strftime("%A, %d %B %Y")
    st.markdown(f"""
    <div class="welcome-card">
        <h2>💰 My Finances</h2>
        <p>{today}</p>
    </div>
    """, unsafe_allow_html=True)

# ── Big KPI Cards ─────────────────────────────────────────────────────────────
bal_class = "card-balance-pos" if summary["balance"] >= 0 else "card-balance-neg"
bal_label = "✅ You're saving!" if summary["balance"] >= 0 else "⚠️ Overspending"

st.markdown(f"""
<div class="metric-row">
  <div class="metric-card card-income">
    <p class="amount">{fmt(summary['total_income'])}</p>
    <p class="label">💵 Total Income</p>
  </div>
  <div class="metric-card card-expense">
    <p class="amount">{fmt(summary['total_expense'])}</p>
    <p class="label">💸 Total Spent</p>
  </div>
</div>
<div class="metric-row">
  <div class="metric-card {bal_class}">
    <p class="amount">{fmt(summary['balance'])}</p>
    <p class="label">🏦 Balance · {bal_label}</p>
  </div>
  <div class="metric-card card-count">
    <p class="amount">{len(transactions)}</p>
    <p class="label">📝 Transactions</p>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Nav Tabs ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["➕  Add Money", "📊  Charts", "📋  History", "🤖  AI Insights"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ADD TRANSACTION (Step-by-step guided)
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### ➕ Add a Transaction")
    st.caption("Follow the steps below — takes less than 10 seconds!")

    # Step 1
    st.markdown('<div class="step-pill">Step 1 of 4 — Type</div>', unsafe_allow_html=True)
    t_type = st.radio(
        "Is this money coming IN or going OUT?",
        ["💸 Expense (money out)", "💵 Income (money in)"],
        horizontal=True,
        key="t_type_radio"
    )
    t_type_val = "expense" if "Expense" in t_type else "income"

    st.markdown("---")

    # Step 2
    st.markdown('<div class="step-pill">Step 2 of 4 — Amount</div>', unsafe_allow_html=True)
    t_amount = st.number_input(
        "How much? (₹)",
        min_value=0.0,
        step=100.0,
        format="%.0f",
        placeholder="e.g. 500",
        key="t_amount"
    )

    st.markdown("---")

    # Step 3
    st.markdown('<div class="step-pill">Step 3 of 4 — Category</div>', unsafe_allow_html=True)
    categories = Transaction.CATEGORIES[t_type_val]

    # Emoji map for categories
    cat_emoji = {
        "Food": "🍔", "Transport": "🚗", "Rent": "🏠",
        "Utilities": "💡", "Shopping": "🛍️", "Health": "💊",
        "Education": "📚", "Entertainment": "🎬", "Other": "📦",
        "Salary": "💼", "Freelance": "💻", "Investment": "📈",
        "Gift": "🎁",
    }
    cat_labels = [f"{cat_emoji.get(c, '•')} {c}" for c in categories]
    selected_label = st.selectbox("Pick a category", cat_labels, key="t_cat")
    t_category = selected_label.split(" ", 1)[1]  # strip emoji

    st.markdown("---")

    # Step 4
    st.markdown('<div class="step-pill">Step 4 of 4 — Details</div>', unsafe_allow_html=True)
    col_desc, col_date = st.columns([2, 1])
    with col_desc:
        t_desc = st.text_input(
            "Short note (optional)",
            placeholder="e.g. Swiggy dinner, Bus fare...",
            key="t_desc"
        )
    with col_date:
        t_date = st.date_input("Date", value=date.today(), key="t_date")

    st.markdown("---")

    # Save button
    if st.button("✅ Save Transaction", type="primary", key="save_btn"):
        if t_amount <= 0:
            st.error("⚠️ Please enter an amount greater than ₹0")
        else:
            txn = Transaction(
                amount=t_amount,
                category=t_category,
                type_=t_type_val,
                description=t_desc,
                date=str(t_date),
            )
            db.add(txn)
            sign = "+" if t_type_val == "income" else "-"
            st.success(f"🎉 Saved! {sign}₹{t_amount:,.0f} · {t_category}")
            st.balloons()
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CHARTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    if not transactions:
        st.info("📊 Add some transactions first to see your charts!")
    else:
        # ── Spending Breakdown ─────────────────────────────────────────────
        st.markdown("### 🍩 Where is your money going?")
        cat_df = pd.DataFrame(summary["by_category"])
        expenses_df = cat_df[cat_df["type"] == "expense"] if not cat_df.empty else pd.DataFrame()

        if not expenses_df.empty:
            fig1 = px.pie(
                expenses_df, values="total", names="category",
                hole=0.5,
                color_discrete_sequence=[
                    "#6366f1","#8b5cf6","#ec4899","#f59e0b",
                    "#10b981","#3b82f6","#ef4444","#14b8a6","#f97316"
                ],
            )
            fig1.update_traces(textposition="outside", textinfo="label+percent")
            fig1.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                height=350,
            )
            st.plotly_chart(fig1, use_container_width=True)

            # Top spends list
            st.markdown("**Your top spending areas:**")
            top = expenses_df.sort_values("total", ascending=False).head(3)
            for _, row in top.iterrows():
                pct = (row["total"] / summary["total_expense"] * 100) if summary["total_expense"] else 0
                emoji = cat_emoji.get(row["category"], "•")
                st.markdown(f"{emoji} **{row['category']}** — {fmt(row['total'])} ({pct:.0f}% of spending)")
        else:
            st.info("No expense data yet.")

        st.markdown("---")

        # ── Monthly Trend ──────────────────────────────────────────────────
        st.markdown("### 📅 Monthly Overview")
        if monthly:
            monthly_df = pd.DataFrame(monthly)
            monthly_pivot = monthly_df.pivot(
                index="month", columns="type", values="total"
            ).fillna(0).reset_index()

            fig2 = go.Figure()
            if "income" in monthly_pivot.columns:
                fig2.add_bar(
                    x=monthly_pivot["month"],
                    y=monthly_pivot["income"],
                    name="Income",
                    marker_color="#10b981",
                    text=[fmt(v) for v in monthly_pivot["income"]],
                    textposition="outside",
                )
            if "expense" in monthly_pivot.columns:
                fig2.add_bar(
                    x=monthly_pivot["month"],
                    y=monthly_pivot["expense"],
                    name="Expenses",
                    marker_color="#ef4444",
                    text=[fmt(v) for v in monthly_pivot["expense"]],
                    textposition="outside",
                )
            fig2.update_layout(
                barmode="group",
                margin=dict(t=20, b=20, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", y=1.1),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#e5e7eb", tickprefix="₹"),
                height=320,
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Simple insight below chart
            if "expense" in monthly_pivot.columns and len(monthly_pivot) >= 2:
                last  = monthly_pivot["expense"].iloc[-1]
                prev  = monthly_pivot["expense"].iloc[-2]
                diff  = last - prev
                arrow = "📈 up" if diff > 0 else "📉 down"
                st.info(f"Your spending is {arrow} **{fmt(abs(diff))}** compared to last month.")
        else:
            st.info("Add transactions across different months to see trends.")

        st.markdown("---")

        # ── Income vs Expense gauge ────────────────────────────────────────
        st.markdown("### 💡 Savings Rate")
        if summary["total_income"] > 0:
            savings_rate = max(0, (summary["balance"] / summary["total_income"]) * 100)
            fig3 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=round(savings_rate, 1),
                number={"suffix": "%", "font": {"size": 40}},
                delta={"reference": 20, "suffix": "%"},
                title={"text": "of income saved"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar":  {"color": "#6366f1"},
                    "steps": [
                        {"range": [0, 10],  "color": "#fee2e2"},
                        {"range": [10, 20], "color": "#fef3c7"},
                        {"range": [20, 100],"color": "#d1fae5"},
                    ],
                    "threshold": {
                        "line": {"color": "#6366f1", "width": 3},
                        "thickness": 0.75,
                        "value": 20,
                    },
                },
            ))
            fig3.update_layout(
                height=250,
                margin=dict(t=30, b=10, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig3, use_container_width=True)
            if savings_rate >= 20:
                st.success("🎉 Great job! You're saving more than 20% — financial experts recommend this.")
            elif savings_rate >= 10:
                st.warning("💪 Good start! Try to push your savings above 20% of income.")
            else:
                st.error("⚠️ Your savings rate is low. Try cutting your top expense category.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    if not transactions:
        st.info("No transactions yet. Add one in the ➕ tab!")
    else:
        st.markdown(f"### 📋 All Transactions ({len(transactions)} total)")

        # Filter bar
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_type = st.selectbox("Filter by", ["All", "💸 Expenses only", "💵 Income only"])
        with col_f2:
            filter_cat = st.selectbox("Category", ["All"] + list(
                set(t.category for t in transactions)
            ))

        # Apply filters
        filtered = transactions
        if filter_type == "💸 Expenses only":
            filtered = [t for t in filtered if t.type == "expense"]
        elif filter_type == "💵 Income only":
            filtered = [t for t in filtered if t.type == "income"]
        if filter_cat != "All":
            filtered = [t for t in filtered if t.category == filter_cat]

        st.caption(f"Showing {len(filtered)} transactions")
        st.markdown("---")

        # Transaction cards
        for t in filtered:
            emoji = cat_emoji.get(t.category, "•")
            sign  = "+" if t.type == "income" else "−"
            cls   = "txn-inc" if t.type == "income" else "txn-exp"
            desc  = t.description if t.description else t.category
            st.markdown(f"""
            <div class="txn-row">
              <div class="txn-left">
                <div>{emoji} <strong>{desc}</strong></div>
                <div class="txn-cat">{t.category} · {t.date}</div>
              </div>
              <div class="txn-amt {cls}">{sign}{fmt(t.amount)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Delete
        with st.expander("🗑️ Delete a transaction"):
            st.caption("Enter the transaction number to remove it.")
            del_id = st.number_input("Transaction ID", min_value=1, step=1, key="del_id")
            if st.button("Delete", type="secondary", key="del_btn"):
                if db.delete(int(del_id)):
                    st.success(f"Deleted transaction #{del_id}")
                    st.rerun()
                else:
                    st.error("ID not found. Check the transaction list above.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — AI INSIGHTS (Groq / LLaMA — Free)
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 🤖 AI Financial Insights")
    st.caption("Powered by Groq + LLaMA 3 · 100% free · No credit card needed")

    if not transactions:
        st.info("Add some transactions first so the AI has data to analyse!")
    else:
        # ── API Key input ──────────────────────────────────────────────────
        st.markdown("#### 🔑 Enter your Groq API Key")
        st.markdown(
            "Get a free key in 30 seconds → [console.groq.com](https://console.groq.com) "
            "· Sign up → API Keys → Create key · Paste it below 👇"
        )

        groq_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Your key is never stored — only used for this session."
        )

        if groq_key:
            col_a, col_b = st.columns(2)

            with col_a:
                if st.button("✨ Analyse my finances", type="primary", use_container_width=True):
                    with st.spinner("🧠 LLaMA is reading your finances..."):
                        try:
                            from ai_insights import FinanceAI
                            ai = FinanceAI(api_key=groq_key)
                            insights = ai.get_insights(summary, monthly)
                            st.session_state["insights"] = insights
                        except Exception as e:
                            st.error(f"Error: {e}")

            with col_b:
                if st.button("💡 Get saving tip", type="secondary", use_container_width=True):
                    with st.spinner("💭 Thinking of a tip..."):
                        try:
                            from ai_insights import FinanceAI
                            ai = FinanceAI(api_key=groq_key)
                            tip = ai.get_saving_tip(summary)
                            st.session_state["tip"] = tip
                        except Exception as e:
                            st.error(f"Error: {e}")

            # ── Show insights ──────────────────────────────────────────────
            if "insights" in st.session_state and st.session_state["insights"]:
                st.markdown("---")
                st.markdown("#### 📊 Your Financial Analysis")
                icons = ["💰", "📈", "⚠️", "🎯"]
                for i, insight in enumerate(st.session_state["insights"]):
                    icon = icons[i] if i < len(icons) else "💡"
                    st.markdown(f"""
                    <div style="background:#f0fdf4; border-left:4px solid #10b981;
                                border-radius:10px; padding:14px 16px; margin-bottom:10px;">
                        <span style="font-size:1.2rem;">{icon}</span>
                        <span style="font-size:0.95rem; color:#065f46; margin-left:8px;">{insight}</span>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Show saving tip ────────────────────────────────────────────
            if "tip" in st.session_state and st.session_state["tip"]:
                st.markdown("---")
                st.markdown("#### 💡 Your Saving Tip")
                st.markdown(f"""
                <div style="background:#eff6ff; border-left:4px solid #6366f1;
                            border-radius:10px; padding:14px 16px;">
                    <span style="font-size:0.95rem; color:#1e40af;">
                        {st.session_state["tip"]}
                    </span>
                </div>
                """, unsafe_allow_html=True)

            # ── Auto-categorise ────────────────────────────────────────────
            st.markdown("---")
            st.markdown("#### 🏷️ Auto-Categorise a Transaction")
            st.caption("Type any expense description and AI will suggest the right category")
            desc_input = st.text_input("Description", placeholder="e.g. Ola cab to airport", key="ai_desc")
            if st.button("Suggest category →", key="ai_cat_btn"):
                if desc_input:
                    with st.spinner("Thinking..."):
                        try:
                            from ai_insights import FinanceAI
                            ai = FinanceAI(api_key=groq_key)
                            suggested = ai.categorise_transaction(desc_input)
                            st.success(f"Suggested category: **{suggested}**")
                        except Exception as e:
                            st.error(str(e))
                else:
                    st.warning("Enter a description first.")
        else:
            st.info("👆 Paste your Groq API key above to unlock AI features.")
            st.markdown("""
            **How to get your free Groq key (30 seconds):**
            1. Go to [console.groq.com](https://console.groq.com)
            2. Sign up with Google or email
            3. Click **API Keys** → **Create API Key**
            4. Copy and paste it above
            """)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#9ca3af; font-size:0.8rem;'>"
    "💰 Finance Tracker · Built by Spoorti Inganalli"
    "</p>",
    unsafe_allow_html=True
)


# ══════════════════════════════════════════════════════════════════════════════
# AI INSIGHTS SECTION — injected below charts in tab2
# This is imported and called from the main app above.
# ══════════════════════════════════════════════════════════════════════════════
