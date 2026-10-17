# ExpenseLens — Expense Insights Dashboard

ExpenseLens is an interactive expense analytics dashboard built with Python, Streamlit, Pandas, and Matplotlib.

It helps users explore spending patterns, analyse expenses by category and payment method, track monthly budgets, and understand their spending habits through visualisations.

## Features

- Interactive expense dashboard
- Add new expense records
- Date range and category filters
- Total expenses, average expense, and transaction metrics
- Category-wise expense analysis
- Payment method analysis
- Daily spending trends
- Weekday spending analysis
- Monthly expense comparison
- Monthly budget planner
- Category-wise budget tracking and alerts
- Filtered expense data download
- Input validation and duplicate record detection

## Tech Stack

- Python
- Streamlit
- Pandas
- Matplotlib

## Project Structure

```text
ExpenseLens/
├── app.py
├── generate_data.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── expenses_generated.csv
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sd-athar-irfan05/ExpenseLens.git
```

### 2. Navigate to the project folder

```bash
cd ExpenseLens
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install the required libraries

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

## Dataset

The project uses a CSV file to store expense records.

The included dataset contains synthetic expense data for demonstration and analysis. It is not real financial data.

Users can also add new expense records through the dashboard.

## Future Improvements

- Database integration
- User authentication
- Automated expense categorisation
- Advanced spending insights
- Cloud deployment

## Author

**Syed Athar Irfan**

## License

This project is available for learning and portfolio demonstration.