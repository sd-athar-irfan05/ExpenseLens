# ExpenseLens — Expense Insights Dashboard

<p align="center">
  <strong>An interactive dashboard to understand, analyse, and manage personal spending.</strong>
</p>

<p align="center">
  <a href="https://expense-lens.streamlit.app/">
    <img src="https://img.shields.io/badge/Live%20Demo-Open%20Dashboard-brightgreen?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
</p>

ExpenseLens is an interactive expense analytics dashboard built with Python, Streamlit, Pandas, and Matplotlib.

It helps users explore spending patterns, analyse expenses by category and payment method, track monthly budgets, and understand their spending habits through visualisations.

## Features

* Interactive expense dashboard
* Add new expense records
* Date range and category filters
* Total expenses, average expense, and transaction metrics
* Category-wise expense analysis
* Payment method analysis
* Daily spending trends
* Weekday spending analysis
* Monthly expense comparison
* Monthly budget planner
* Category-wise budget tracking and alerts
* Filtered expense data download
* Input validation and duplicate record detection

## Tech Stack

* **Python** — Application logic and data processing
* **Streamlit** — Interactive dashboard and user interface
* **Pandas** — Data manipulation and analysis
* **Matplotlib** — Data visualisation

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

## Live Demo

Explore the deployed dashboard:

**[Open ExpenseLens Dashboard](https://expense-lens.streamlit.app/)**

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

**Windows PowerShell:**

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

* Database integration
* User authentication
* Automated expense categorisation
* Advanced spending insights

## Author

**Syed Athar Irfan**

* GitHub: [sd-athar-irfan05](https://github.com/sd-athar-irfan05)

## License

This project is available for learning and portfolio demonstration.
