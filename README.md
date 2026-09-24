# BusinessCalc 📊

BusinessCalc is a Django-based web application designed for automated econometric analysis of business sales data. It allows users to upload CSV files, map columns to internal variables, and instantly generate a comprehensive business report with strategic recommendations.

## Features ✨
* **Data Ingestion:** Secure upload of CSV files (supports both comma and semicolon separators).
* **Dynamic Column Mapping:** Interactive UI to map user-defined columns (Date, Revenue, Category) to the system's logic.
* **Data Quality Checks:** Built-in Pandas validation preventing mismatch errors (e.g., swapping Date with Revenue) and handling missing data.
* **Automated Business Analysis:**
  * Time-series analysis (Month-over-Month growth).
  * Category concentration analysis (identifying primary growth drivers and risks).
  * Volatility assessment (Coefficient of Variation).
* **Strategic Recommendations:** Context-aware business advice generated based on calculated financial metrics.
* **PDF Export:** One-click generation and download of a clean, professional PDF report using `xhtml2pdf`.

## Tech Stack 🛠️
* **Backend:** Python 3, Django
* **Data Processing:** Pandas, NumPy
* **Frontend:** HTML5, CSS3, Django Templates
* **PDF Generation:** xhtml2pdf

## Installation & Setup 🚀

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ryblus/BusinessCalc.git
   cd BusinessCalc
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Usage 💡
1. Upload your business data in `.csv` format.
2. Select which columns correspond to the Transaction Date, Revenue/Value, and optionally, Category.
3. Review the numerical summary and read the strategic recommendations.
4. Click **Download PDF Report** to export the analysis.