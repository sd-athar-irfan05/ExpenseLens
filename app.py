import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="ExpenseLens",
    page_icon="💰",
    layout="wide"
)

# ==================================================
# CUSTOM CSS - EXPENSELENS
# ==================================================

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}

/* Main Content Spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Main Headings */
h1, h2, h3 {
    color: #F8FAFC;
    font-weight: 700;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Metric Labels */
[data-testid="stMetricLabel"] {
    color: #CBD5E1;
}

/* Metric Values */
[data-testid="stMetricValue"] {
    color: #38BDF8;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    border: 1px solid #38BDF8;
    transition: all 0.2s ease;
}

/* Button Hover */
.stButton > button:hover {
    border-color: #7DD3FC;
    color: #7DD3FC;
}

/* Input Fields */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    border-radius: 8px;
}

/* Multiselect Selected Tags — target the tag and its nested elements */
[data-testid="stMultiSelect"] [data-baseweb="tag"],
[data-testid="stMultiSelect"] [data-baseweb="tag"] > span,
[data-testid="stMultiSelect"] [data-baseweb="tag"] > div {
    background: #1E40AF !important;
    background-color: #1E40AF !important;
    color: #FFFFFF !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 6px !important;
}

/* Multiselect Tag Text */
[data-testid="stMultiSelect"] [data-baseweb="tag"] *,
[data-testid="stMultiSelect"] [data-baseweb="tag"] span {
    color: #FFFFFF !important;
}

/* Multiselect Tag Close Icon */
[data-testid="stMultiSelect"] [data-baseweb="tag"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* Streamlit theme fallback for selected multiselect chips */
[data-testid="stMultiSelect"] [data-baseweb="tag"] [role="presentation"] {
    background-color: #1E40AF !important;
    color: #FFFFFF !important;
}


/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid #334155;
    border-radius: 10px;
    margin-bottom: 8px;
}

/* DataFrames and Tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid #334155;
    border-radius: 10px;
}

/* Horizontal Dividers */
hr {
    border-color: #334155;
}

/* Info Messages */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Progress Bars */
.stProgress > div > div > div > div {
    background-color: #38BDF8;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 2. PAGE INTRODUCTION
# ==================================================

st.title("💰 ExpenseLens")

st.write(
    "Welcome to ExpenseLens — "
    "Your Personal Expense Insights Dashboard!"
)

st.info(
    "Track your expenses, understand your spending, "
    "and make better financial decisions."
)


# ==================================================
# 3. LOAD AND CLEAN DATA
# ==================================================

try:
    df = pd.read_csv("data/expenses_generated.csv")

except FileNotFoundError:
    st.error(
        "Expense dataset not found. "
        "Please check data/expenses_generated.csv."
    )
    st.stop()


required_columns = [
    "Date",
    "Category",
    "Description",
    "Amount",
    "Payment_Method"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"Missing required columns: {', '.join(missing_columns)}"
    )
    st.stop()


# Convert columns into suitable data types

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
)


# Remove invalid records

df = df.dropna(
    subset=["Date", "Category", "Amount"]
).copy()

df["Category"] = df["Category"].astype(str).str.strip()

df = df[df["Category"] != ""].copy()

if df.empty:
    st.warning("No valid expense records are available.")
    st.stop()


# ==================================================
# DATA VALIDATION SUMMARY
# ==================================================

with st.expander("🔍 Data Validation Summary"):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Valid Records", len(df))

    with col2:
        st.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )

    with col3:
        st.metric(
            "Missing Values",
            int(df.isna().sum().sum())
        )

    st.write("**Data Types**")
    st.dataframe(
        df.dtypes.astype(str).rename("Data Type"),
        use_container_width=True
    )


# ==================================================
# EXPENSE AMOUNT VALIDATION
# ==================================================

with st.expander("💰 Expense Amount Validation"):

    negative_amounts = int((df["Amount"] < 0).sum())
    zero_amounts = int((df["Amount"] == 0).sum())
    positive_amounts = int((df["Amount"] > 0).sum())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Positive Amounts", positive_amounts)

    with col2:
        st.metric("Zero Amounts", zero_amounts)

    with col3:
        st.metric("Negative Amounts", negative_amounts)

    if negative_amounts > 0 or zero_amounts > 0:
        st.warning("Some records have zero or negative amounts.")
    else:
        st.success("All expense amounts are positive.")


# ==================================================
# CATEGORY & PAYMENT METHOD VALIDATION
# ==================================================

with st.expander("🧹 Category & Payment Method Validation"):

    empty_categories = int(
        (df["Category"].astype(str).str.strip() == "").sum()
    )

    valid_payment_methods = ["UPI", "Cash", "Card"]

    invalid_payment_methods = int(
        (~df["Payment_Method"].isin(valid_payment_methods)).sum()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Empty Categories", empty_categories)

    with col2:
        st.metric("Invalid Payment Methods", invalid_payment_methods)

    if empty_categories == 0 and invalid_payment_methods == 0:
        st.success("All categories and payment methods are valid.")
    else:
        st.warning("Some records need category or payment method correction.")



# ==================================================
# ADD NEW EXPENSE
# ==================================================

st.divider()
st.header("➕ Add New Expense")

with st.form("add_expense_form"):

    expense_date = st.date_input(
        "Expense Date",
        value=pd.Timestamp.today().date()
    )

    expense_categories = sorted(
        df["Category"].dropna().unique().tolist()
    )

    new_category = st.selectbox(
        "Category",
        options=expense_categories
    )

    new_description = st.text_input(
        "Description",
        placeholder="e.g. Lunch, Bus Ticket"
    )

    new_amount = st.number_input(
        "Amount (₹)",
        min_value=0.01,
        value=100.0,
        step=10.0
    )

    new_payment_method = st.selectbox(
        "Payment Method",
        options=["UPI", "Cash", "Card"]
    )

    submitted = st.form_submit_button("Save Expense")

    if submitted:

        if not new_description.strip():
            st.error("Please enter an expense description.")

        elif new_amount <= 0:
            st.error("Expense amount must be greater than zero.")

        elif new_category not in df["Category"].unique():
            st.error("Please select a valid category.")

        elif new_payment_method not in ["UPI", "Cash", "Card"]:
            st.error("Please select a valid payment method.")

        else:

            # Check whether the same expense already exists

            duplicate_expense = (
                (df["Date"].dt.date == expense_date)
                & (df["Category"] == new_category)
                & (
                    df["Description"].astype(str).str.strip().str.lower()
                    == new_description.strip().lower()
                )
                & (df["Amount"] == new_amount)
                & (df["Payment_Method"] == new_payment_method)
            ).any()

            if duplicate_expense:

                st.warning(
                    "A similar expense already exists. "
                    "Please verify before saving."
                )

            else:

                new_expense = pd.DataFrame([{
                    "Date": pd.Timestamp(expense_date),
                    "Category": new_category,
                    "Description": new_description.strip(),
                    "Amount": new_amount,
                    "Payment_Method": new_payment_method
                }])

                try:

                    new_expense.to_csv(
                        "data/expenses_generated.csv",
                        mode="a",
                        header=False,
                        index=False,
                        date_format="%Y-%m-%d"
                    )

                    st.success("Expense saved successfully!")
                    st.rerun()
                    

                except OSError as error:

                    st.error(
                        f"Could not save expense: {error}"
                    )


# ==================================================
# 4. DATE RANGE FILTER
# ==================================================

st.divider()
st.header("📅 Filter Your Expenses")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_col1, date_col2 = st.columns(2)

with date_col1:
    start_date = st.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        key="dashboard_start_date"
    )

with date_col2:
    end_date = st.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        key="dashboard_end_date"
    )


if start_date > end_date:
    st.error("Start date cannot be after end date.")
    st.stop()


filtered_df = df[
    (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
].copy()


# ==================================================
# CATEGORY FILTER
# ==================================================

st.subheader("🔎 Filter by Category")

available_categories = sorted(
    filtered_df["Category"].unique().tolist()
)

selected_categories = st.multiselect(
    "Select Categories",
    options=available_categories,
    default=available_categories
)

filtered_df = filtered_df[
    filtered_df["Category"].isin(selected_categories)
].copy()

# ==================================================
# 5. DASHBOARD METRICS
# ==================================================

total_expense = filtered_df["Amount"].sum()

average_expense = (
    filtered_df["Amount"].mean()
    if not filtered_df.empty
    else 0
)

total_transactions = len(filtered_df)


category_expenses = (
    filtered_df.groupby("Category")["Amount"].sum()
)


if not category_expenses.empty:

    highest_category = category_expenses.idxmax()

    highest_category_amount = category_expenses.max()

else:

    highest_category = "No data"

    highest_category_amount = 0


st.divider()
st.header("📊 Expense Dashboard")

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(
        "Total Expenses",
        f"₹{total_expense:,.2f}"
    )

with metric2:
    st.metric(
        "Average Expense",
        f"₹{average_expense:,.2f}"
    )

with metric3:
    st.metric(
        "Total Transactions",
        total_transactions
    )

with metric4:
    st.metric(
        "Highest Spending Category",
        highest_category,
        help=(
            f"Total spent: "
            f"₹{highest_category_amount:,.2f}"
        )
    )


# ==================================================
# 6. EXPENSE RECORDS TABLE
# ==================================================

st.subheader("📋 Expense Records")

# ==================================================
# SEARCH EXPENSE RECORDS
# ==================================================

search_text = st.text_input(
    "🔍 Search by Description",
    placeholder="e.g. Lunch, Bus Ticket, Groceries"
)

if search_text:
    display_filtered_df = filtered_df[
        filtered_df["Description"]
        .astype(str)
        .str.contains(search_text, case=False, na=False)
    ].copy()
else:
    display_filtered_df = filtered_df.copy()


if not display_filtered_df.empty:

    display_df = display_filtered_df.copy()

    display_df["Date"] = (
        display_df["Date"].dt.strftime("%Y-%m-%d")
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No matching expense records found.")


# ==================================================
# DOWNLOAD EXPENSE REPORT
# ==================================================

st.subheader("📥 Download Expense Report")

if not filtered_df.empty:

    download_df = filtered_df.copy()

    download_df["Date"] = (
        download_df["Date"].dt.strftime("%Y-%m-%d")
    )

    csv_data = download_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="expense_report.csv",
        mime="text/csv"
    )

else:
    st.info("No expense records available to download.")


# ==================================================
# 7. CATEGORY-WISE EXPENSE ANALYSIS
# ==================================================

st.divider()
st.header("📊 Category-wise Expense Analysis")


if not category_expenses.empty:

    chart_col1, chart_col2 = st.columns(2)

    # BAR CHART

    with chart_col1:

        st.subheader("Expenses by Category")

        fig_bar, ax_bar = plt.subplots(figsize=(8, 5))

        category_expenses.sort_values().plot(
            kind="bar",
            ax=ax_bar
        )

        ax_bar.set_xlabel("Category")
        ax_bar.set_ylabel("Total Expense (₹)")
        ax_bar.set_title("Category-wise Spending")

        ax_bar.tick_params(
            axis="x",
            rotation=45
        )

        fig_bar.tight_layout()

        st.pyplot(fig_bar)

        plt.close(fig_bar)


    # PIE CHART

    with chart_col2:

        st.subheader("Spending Distribution")

        fig_pie, ax_pie = plt.subplots(figsize=(8, 5))

        category_expenses.plot(
            kind="pie",
            autopct="%1.1f%%",
            startangle=90,
            ax=ax_pie
        )

        ax_pie.set_ylabel("")
        ax_pie.set_title("Expense Distribution")

        fig_pie.tight_layout()

        st.pyplot(fig_pie)

        plt.close(fig_pie)


else:

    st.info(
        "No category data is available for the selected dates."
    )

# ==================================================
# PAYMENT METHOD ANALYSIS
# ==================================================

st.divider()
st.header("💳 Payment Method Analysis")

if not filtered_df.empty:

    payment_summary = (
        filtered_df.groupby("Payment_Method")
        .agg(
            Total_Expenses=("Amount", "sum"),
            Total_Transactions=("Amount", "count")
        )
        .sort_values("Total_Expenses", ascending=False)
    )

    # Most used payment method by transaction count
    most_used_method = payment_summary["Total_Transactions"].idxmax()

    # Highest spending payment method
    highest_spending_method = payment_summary["Total_Expenses"].idxmax()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Most Used Payment Method",
            most_used_method
        )

    with col2:
        st.metric(
            "Highest Spending Method",
            highest_spending_method,
            help="Payment method with the highest total expense."
        )

    st.subheader("Payment Method Summary")

    st.dataframe(
        payment_summary.style.format({
            "Total_Expenses": "₹{:,.2f}",
            "Total_Transactions": "{:,.0f}"
        }),
        use_container_width=True
    )

    st.subheader("Expenses by Payment Method")

    fig_payment, ax_payment = plt.subplots(figsize=(10, 5))

    payment_summary["Total_Expenses"].plot(
        kind="bar",
        ax=ax_payment
    )

    ax_payment.set_xlabel("Payment Method")
    ax_payment.set_ylabel("Total Expenses (₹)")
    ax_payment.set_title("Payment Method-wise Spending")

    ax_payment.tick_params(axis="x", rotation=0)

    fig_payment.tight_layout()

    st.pyplot(fig_payment)

    plt.close(fig_payment)

else:
    st.info("No expenses available for payment method analysis.")


# ==================================================
# SPENDING INSIGHTS
# ==================================================

st.divider()
st.header("💡 Spending Insights")

if not filtered_df.empty:

    # Highest spending category
    category_totals = filtered_df.groupby("Category")["Amount"].sum()

    highest_category = category_totals.idxmax()
    highest_category_amount = category_totals.max()

    # Average daily spending
    daily_totals = (
        filtered_df.groupby(filtered_df["Date"].dt.date)["Amount"].sum()
    )

    average_daily_expense = daily_totals.mean()

    # Total transactions
    total_transactions = len(filtered_df)

    # Most used payment method
    most_used_payment = filtered_df["Payment_Method"].mode().iloc[0]

    st.subheader("Your Spending Summary")

    st.write(
        f"🛍️ **Highest Spending Category:** {highest_category} "
        f"(₹{highest_category_amount:,.2f})"
    )

    st.write(
        f"📅 **Average Daily Expense:** "
        f"₹{average_daily_expense:,.2f}"
    )

    st.write(
        f"🧾 **Total Transactions:** {total_transactions}"
    )

    st.write(
        f"💳 **Most Used Payment Method:** {most_used_payment}"
    )

else:
    st.info("No expense data available to generate insights.")


# ==================================================
# DAILY SPENDING LIMIT ALERT
# ==================================================

st.divider()
st.header("🚨 Daily Spending Limit Alert")

daily_limit = st.number_input(
    "Set Your Daily Spending Limit (₹)",
    min_value=0.0,
    value=2000.0,
    step=100.0,
    key="daily_spending_limit"
)

if not filtered_df.empty and daily_limit > 0:

    daily_totals = (
        filtered_df.groupby(filtered_df["Date"].dt.date)["Amount"]
        .sum()
    )

    exceeded_days = daily_totals[daily_totals > daily_limit]

    if not exceeded_days.empty:

        st.warning(
            f"Your daily limit was exceeded on "
            f"{len(exceeded_days)} day(s)."
        )

        for date, amount in exceeded_days.items():
            st.error(
                f"{date}: Spending ₹{amount:,.2f} "
                f"(Limit: ₹{daily_limit:,.2f})"
            )

    else:
        st.success(
            "Great! No day exceeded your spending limit "
            "in the selected data."
        )

elif daily_limit == 0:
    st.info("Set a daily limit greater than ₹0 to activate alerts.")

else:
    st.info("No expenses available for the selected filters.")


# ==================================================
# 8. DAILY SPENDING TREND
# ==================================================

st.divider()
st.header("📈 Daily Spending Trend")


if not filtered_df.empty:

    daily_expenses = (
        filtered_df.groupby(
            filtered_df["Date"].dt.date
        )["Amount"].sum()
    )

    fig_daily, ax_daily = plt.subplots(figsize=(12, 5))

    daily_expenses.plot(
        kind="line",
        marker="o",
        ax=ax_daily
    )

    ax_daily.set_xlabel("Date")
    ax_daily.set_ylabel("Total Expense (₹)")
    ax_daily.set_title("Daily Spending Over Selected Period")

    fig_daily.tight_layout()

    st.pyplot(fig_daily)

    plt.close(fig_daily)

else:

    st.info(
        "No data available for the daily spending trend."
    )


# ==================================================
# DATE-WISE EXPENSE SUMMARY
# ==================================================

st.divider()
st.header("🗓️ Date-wise Expense Summary")

if not filtered_df.empty:

    date_summary = (
        filtered_df.assign(
            Expense_Date=filtered_df["Date"].dt.date
        )
        .groupby("Expense_Date")["Amount"]
        .agg(
            Total_Expenses="sum",
            Transactions="count",
            Average_Expense="mean"
        )
        .reset_index()
        .sort_values("Expense_Date", ascending=False)
    )

    date_summary = date_summary.rename(columns={
        "Expense_Date": "Date",
        "Total_Expenses": "Total Expenses",
        "Average_Expense": "Average Expense"
    })

    date_summary["Date"] = date_summary["Date"].astype(str)

    st.dataframe(
        date_summary.style.format({
            "Total Expenses": "₹{:,.2f}",
            "Transactions": "{:,.0f}",
            "Average Expense": "₹{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No expenses available for the selected filters.")



# ==================================================
# WEEKDAY SPENDING ANALYSIS
# ==================================================

st.divider()
st.header("📆 Weekday Spending Analysis")

if not filtered_df.empty:

    weekday_df = filtered_df.copy()

    weekday_df["Weekday"] = weekday_df["Date"].dt.day_name()

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekday_summary = (
        weekday_df.groupby("Weekday")["Amount"]
        .agg(["sum", "mean", "count"])
        .reindex(weekday_order, fill_value=0)
    )

    weekday_summary.columns = [
        "Total Expenses",
        "Average Expense",
        "Transactions"
    ]

    busiest_day = weekday_summary["Total Expenses"].idxmax()
    highest_spending = weekday_summary["Total Expenses"].max()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Highest Spending Weekday", busiest_day)

    with col2:
        st.metric(
            "Total Spent on That Day",
            f"₹{highest_spending:,.2f}"
        )

    st.subheader("Weekday-wise Summary")

    st.dataframe(
        weekday_summary.style.format({
            "Total Expenses": "₹{:,.2f}",
            "Average Expense": "₹{:,.2f}",
            "Transactions": "{:,.0f}"
        }),
        use_container_width=True
    )

    st.subheader("Total Spending by Weekday")

    fig_weekday, ax_weekday = plt.subplots(figsize=(10, 5))

    weekday_summary["Total Expenses"].plot(
        kind="bar",
        ax=ax_weekday
    )

    ax_weekday.set_xlabel("Weekday")
    ax_weekday.set_ylabel("Total Expenses (₹)")
    ax_weekday.set_title("Weekday-wise Spending")

    ax_weekday.tick_params(axis="x", rotation=45)

    fig_weekday.tight_layout()

    st.pyplot(fig_weekday)

    plt.close(fig_weekday)

else:
    st.info("No expenses available for weekday analysis.")


# ==================================================
# 9. MONTHLY SPENDING ANALYSIS
# ==================================================

st.divider()
st.header("📅 Monthly Spending Analysis")

monthly_df = df.copy()

monthly_df["Month"] = (
    monthly_df["Date"].dt.to_period("M")
)


# Monthly totals

monthly_expenses = (
    monthly_df.groupby("Month")["Amount"].sum()
)


# ==================================================
# MONTH-OVER-MONTH SPENDING INSIGHT
# ==================================================

st.subheader("📈 Monthly Spending Insight")

if len(monthly_expenses) >= 2:

    current_month = monthly_expenses.index[-1]
    previous_month = monthly_expenses.index[-2]

    current_total = monthly_expenses.iloc[-1]
    previous_total = monthly_expenses.iloc[-2]

    difference = current_total - previous_total

    if previous_total != 0:
        percentage_change = (difference / previous_total) * 100
    else:
        percentage_change = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Latest Month",
            str(current_month),
            f"₹{current_total:,.2f}"
        )

    with col2:
        st.metric(
            "Previous Month",
            str(previous_month),
            f"₹{previous_total:,.2f}"
        )

    with col3:
        st.metric(
            "Spending Change",
            f"{percentage_change:+.1f}%",
            f"₹{difference:+,.2f}",
            delta_color="inverse"
        )

    if difference > 0:
        st.warning("Spending increased compared with the previous month.")
    elif difference < 0:
        st.success("Spending decreased compared with the previous month.")
    else:
        st.info("Spending remained unchanged.")

else:
    st.info("At least two months of expense data are required for comparison.")


st.subheader("Monthly Expense Comparison")

fig_monthly, ax_monthly = plt.subplots(figsize=(10, 5))

monthly_expenses.plot(
    kind="bar",
    ax=ax_monthly
)

ax_monthly.set_xlabel("Month")
ax_monthly.set_ylabel("Total Expenses (₹)")
ax_monthly.set_title("Month-wise Total Spending")

fig_monthly.tight_layout()

st.pyplot(fig_monthly)

plt.close(fig_monthly)


# Month-over-month comparison

st.subheader("Month-over-Month Spending Change")

monthly_change = monthly_expenses.pct_change() * 100

monthly_summary = pd.DataFrame({
    "Total Expenses": monthly_expenses,
    "Change from Previous Month (%)": monthly_change
})

monthly_summary.index = monthly_summary.index.astype(str)

st.dataframe(
    monthly_summary.style.format({
        "Total Expenses": "₹{:,.2f}",
        "Change from Previous Month (%)": "{:+.2f}%"
    }),
    use_container_width=True
)


# Monthly category breakdown

st.subheader("Monthly Category Breakdown")

monthly_category = (
    monthly_df.groupby(
        ["Month", "Category"]
    )["Amount"]
    .sum()
    .unstack(fill_value=0)
)

monthly_category.index = monthly_category.index.astype(str)

st.dataframe(
    monthly_category.style.format("₹{:,.2f}"),
    use_container_width=True
)


# ==================================================
# MONTHLY EXPENSE SUMMARY DOWNLOAD
# ==================================================

st.divider()
st.header("📤 Download Monthly Expense Summary")

report_months = sorted(
    df["Date"].dt.to_period("M").unique()
)

report_month_options = [str(month) for month in report_months]

selected_report_month = st.selectbox(
    "Select Month for Report",
    options=report_month_options,
    key="monthly_report_month"
)

report_period = pd.Period(selected_report_month, freq="M")

report_df = df[
    df["Date"].dt.to_period("M") == report_period
].copy()

if not report_df.empty:

    total_report_expense = report_df["Amount"].sum()
    total_report_transactions = len(report_df)

    category_report = (
        report_df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )
    category_report["Report_Type"] = "Category"

    payment_report = (
        report_df.groupby("Payment_Method")["Amount"]
        .sum()
        .reset_index()
    )
    payment_report["Report_Type"] = "Payment Method"

    category_report = category_report.rename(
        columns={"Category": "Name", "Amount": "Total_Amount"}
    )

    payment_report = payment_report.rename(
        columns={
            "Payment_Method": "Name",
            "Amount": "Total_Amount"
        }
    )

    summary_report = pd.concat(
        [category_report, payment_report],
        ignore_index=True
    )

    summary_report["Month"] = selected_report_month
    summary_report["Monthly_Total_Expenses"] = total_report_expense
    summary_report["Total_Transactions"] = total_report_transactions

    summary_report = summary_report[
        [
            "Month",
            "Report_Type",
            "Name",
            "Total_Amount",
            "Monthly_Total_Expenses",
            "Total_Transactions"
        ]
    ]

    st.metric(
        "Monthly Total Expenses",
        f"₹{total_report_expense:,.2f}"
    )

    st.metric(
        "Total Transactions",
        total_report_transactions
    )

    st.dataframe(
        summary_report,
        use_container_width=True,
        hide_index=True
    )

    report_csv = summary_report.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Monthly Summary CSV",
        data=report_csv,
        file_name=f"expense_summary_{selected_report_month}.csv",
        mime="text/csv"
    )

else:
    st.info("No expenses found for the selected month.")


# ==================================================
# 10. BUDGET PLANNER
# ==================================================

st.divider()
st.header("💰 Budget Planner")

st.write(
    "Set your monthly budget and monitor your spending "
    "across different expense categories."
)


# Available months

available_months = sorted(
    df["Date"].dt.to_period("M").unique()
)

month_options = [
    str(month)
    for month in available_months
]


selected_month = st.selectbox(
    "Select Budget Month",
    options=month_options,
    key="budget_selected_month"
)


selected_period = pd.Period(
    selected_month,
    freq="M"
)


# Complete selected-month data

budget_df = df[
    df["Date"].dt.to_period("M") == selected_period
].copy()


actual_monthly_expense = budget_df["Amount"].sum()


# ==================================================
# 11. MONTHLY BUDGET INPUT
# ==================================================

st.subheader("Monthly Budget")

monthly_budget = st.number_input(
    "Enter Your Monthly Budget (₹)",
    min_value=0.0,
    value=60000.0,
    step=1000.0,
    key=f"monthly_budget_{selected_month}"
)


# ==================================================
# 12. MONTHLY BUDGET METRICS
# ==================================================

remaining_budget = (
    monthly_budget - actual_monthly_expense
)


if monthly_budget > 0:

    budget_utilization = (
        actual_monthly_expense / monthly_budget
    ) * 100

else:

    budget_utilization = 0


st.subheader(f"Budget Overview — {selected_month}")

budget_col1, budget_col2, budget_col3, budget_col4 = (
    st.columns(4)
)


with budget_col1:

    st.metric(
        "Monthly Budget",
        f"₹{monthly_budget:,.2f}"
    )


with budget_col2:

    st.metric(
        "Actual Expenses",
        f"₹{actual_monthly_expense:,.2f}"
    )


with budget_col3:

    st.metric(
        "Remaining Budget",
        f"₹{remaining_budget:,.2f}"
    )


with budget_col4:

    st.metric(
        "Budget Utilization",
        f"{budget_utilization:.1f}%"
    )


# ==================================================
# 13. MONTHLY BUDGET STATUS
# ==================================================

st.subheader("Budget Status")


if monthly_budget == 0 and actual_monthly_expense > 0:

    st.error(
        "Your budget is ₹0, but expenses have been recorded. "
        "Please set a monthly budget."
    )

elif actual_monthly_expense > monthly_budget:

    overspending = (
        actual_monthly_expense - monthly_budget
    )

    st.error(
        f"Over Budget! You exceeded your budget by "
        f"₹{overspending:,.2f}."
    )

elif actual_monthly_expense == monthly_budget:

    st.warning(
        "Budget Fully Used! You have reached your "
        "monthly spending limit."
    )

else:

    st.success(
        f"Under Budget! You have "
        f"₹{remaining_budget:,.2f} remaining."
    )


# Progress bar

st.subheader("Budget Utilization Progress")

if monthly_budget > 0:

    progress_value = min(
        budget_utilization / 100,
        1.0
    )

    st.progress(progress_value)

    st.caption(
        f"{budget_utilization:.1f}% of your monthly budget used."
    )

else:

    st.progress(0.0)

    st.caption(
        "Set a budget greater than zero to calculate utilization."
    )


# ==================================================
# 14. CATEGORY-WISE BUDGET TRACKING
# ==================================================

st.divider()
st.header("🧾 Category-wise Budget Tracking")

st.write(
    "Set a separate monthly budget for each category. "
    "Budgets are currently stored for this Streamlit session."
)

budget_categories = sorted(
    df["Category"].dropna().unique().tolist()
)

# Default category budgets: Total = ₹60,000

default_category_budgets = {
    "Bills": 8000.0,
    "Education": 8000.0,
    "Entertainment": 4000.0,
    "Food": 5000.0,
    "Fuel": 8000.0,
    "Health": 5000.0,
    "Other": 5000.0,
    "Personal Care": 5000.0,
    "Shopping": 9000.0,
    "Travel": 3000.0
}

# Initialize session state

if "category_budgets" not in st.session_state:
    st.session_state["category_budgets"] = {}

if selected_month not in st.session_state["category_budgets"]:
    st.session_state["category_budgets"][selected_month] = {
        category: default_category_budgets.get(category, 2000.0)
        for category in budget_categories
    }

# Add budgets for any new categories

for category in budget_categories:
    if category not in st.session_state["category_budgets"][selected_month]:
        st.session_state["category_budgets"][selected_month][category] = (
            default_category_budgets.get(category, 2000.0)
        )

# Display category budget inputs

st.subheader("Set Category Budgets")

category_budget_values = {}
budget_input_columns = st.columns(2)

for index, category in enumerate(budget_categories):
    column = budget_input_columns[index % 2]

    with column:
        category_budget_values[category] = st.number_input(
            f"{category} Budget (₹)",
            min_value=0.0,
            value=float(
                st.session_state["category_budgets"][
                    selected_month
                ][category]
            ),
            step=500.0,
            key=f"category_budget_{selected_month}_{category}"
        )

# Save updated category budgets

st.session_state["category_budgets"][selected_month] = (
    category_budget_values.copy()
)



# ==================================================
# 15. CATEGORY BUDGET CALCULATIONS
# ==================================================

category_actuals = (
    budget_df.groupby("Category")["Amount"].sum()
)


category_budget_rows = []


for category in budget_categories:

    category_budget = category_budget_values[category]

    category_actual = float(
        category_actuals.get(category, 0)
    )

    category_remaining = (
        category_budget - category_actual
    )

    if category_budget > 0:

        category_utilization = (
            category_actual / category_budget
        ) * 100

    else:

        category_utilization = 0


    if category_budget == 0 and category_actual > 0:

        status = "No Budget Set"

    elif category_actual > category_budget:

        status = "Over Budget"

    elif category_actual == category_budget:

        status = "Budget Fully Used"

    else:

        status = "Under Budget"


    category_budget_rows.append({
        "Category": category,
        "Monthly Budget": category_budget,
        "Actual Expenses": category_actual,
        "Remaining Budget": category_remaining,
        "Utilization (%)": category_utilization,
        "Status": status
    })


category_budget_df = pd.DataFrame(
    category_budget_rows
)


# ==================================================
# 16. CATEGORY BUDGET SUMMARY
# ==================================================

st.subheader("Category Budget Summary")

st.dataframe(
    category_budget_df.style.format({
        "Monthly Budget": "₹{:,.2f}",
        "Actual Expenses": "₹{:,.2f}",
        "Remaining Budget": "₹{:,.2f}",
        "Utilization (%)": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)


# ==================================================
# 17. CATEGORY BUDGET WARNINGS
# ==================================================

st.subheader("Category Budget Alerts")

over_budget_categories = category_budget_df[
    category_budget_df["Status"] == "Over Budget"
]

no_budget_categories = category_budget_df[
    category_budget_df["Status"] == "No Budget Set"
]


if not over_budget_categories.empty:

    for _, row in over_budget_categories.iterrows():

        exceeded_amount = (
            row["Actual Expenses"] - row["Monthly Budget"]
        )

        st.error(
            f"{row['Category']}: Over budget by "
            f"₹{exceeded_amount:,.2f}"
        )


if not no_budget_categories.empty:

    for _, row in no_budget_categories.iterrows():

        st.warning(
            f"{row['Category']}: Expenses recorded, "
            "but no budget has been set."
        )


if (
    over_budget_categories.empty
    and no_budget_categories.empty
):

    st.success(
        "All categories are within their assigned budgets."
    )


# ==================================================
# 18. CATEGORY BUDGET VS ACTUAL CHART
# ==================================================

st.subheader("Category Budget vs Actual Expenses")


if not category_budget_df.empty:

    chart_data = category_budget_df.set_index("Category")[
        ["Monthly Budget", "Actual Expenses"]
    ]

    fig_budget, ax_budget = plt.subplots(figsize=(12, 6))

    chart_data.plot(
        kind="bar",
        ax=ax_budget
    )

    ax_budget.set_xlabel("Category")
    ax_budget.set_ylabel("Amount (₹)")
    ax_budget.set_title(
        f"Budget vs Actual Expenses — {selected_month}"
    )

    ax_budget.tick_params(
        axis="x",
        rotation=45
    )

    ax_budget.legend(
        ["Monthly Budget", "Actual Expenses"]
    )

    fig_budget.tight_layout()

    st.pyplot(fig_budget)

    plt.close(fig_budget)


# ==================================================
# 19. CATEGORY BUDGET UTILIZATION
# ==================================================

st.subheader("Category Budget Utilization")

for _, row in category_budget_df.iterrows():

    category = row["Category"]

    utilization = row["Utilization (%)"]

    st.write(
        f"**{category}:** {utilization:.1f}% used"
    )

    st.progress(
        min(max(utilization / 100, 0.0), 1.0)
    )