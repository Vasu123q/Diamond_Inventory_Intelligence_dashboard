# 💎 Diamond Inventory Intelligence

A Streamlit-based analytics application for exploring diamond inventory, stone demand, sales probability, aging risk, and location-wise stone status.

The project combines multi-level inventory processing (L1, L2, and L3), data preparation, machine-learning predictions, and an interactive Streamlit dashboard.

## 🚀 Streamlit Dashboard

The project includes a Streamlit dashboard with two main sections:

### 1. Inventory Stones

The **Inventory Stones** page provides interactive analysis across Level 1, Level 2, and Level 3 inventory data.

Features include:

- Multi-level inventory views: **L1, L2, and L3**
- Filters for:
  - Shape
  - Color range
  - Clarity range
  - Cut
  - Lab
  - Polish
  - Symmetry
  - Fluorescence
  - Stone Location
  - Stock Classification
- Numeric range filters for:
  - Carat / Size
  - Depth %
  - Table %
  - Ratio
- Inventory distribution visualizations
- Size-range distribution
- Sales overview
- Selling recommendations
- Stone demand analysis
- Sales probability analysis
- Aging-risk analysis
- Filtered inventory data tables
- Manual data refresh and cached data loading

### 2. Stone Status

The **Stone Status** page provides location-wise inventory status analysis.

It supports filtering by:

- Stone Location
- Inventory/status category

The dashboard summarizes categories such as:

- Memo Out
- AVL Stock
- Unpublish AVL (Not On Rap)
- On Hand
- On Hold
- For Web
- Transit
- Reserved
- Consume
- Under Certification

It also provides location-level drill-down information for selected categories.

---

## 🧠 Project Workflow

The project is organized into three processing levels:

```text
Input Data
    │
    ▼
Level 1 (L1)
    │
    ▼
Level 2 (L2)
    │
    ▼
Level 3 (L3)
    │
    ▼
Predictions / Inventory Outputs
    │
    ▼
Final_Predicted.xlsx
    │
    ▼
Streamlit Dashboard
```

Each level contains data-processing scripts, intermediate Excel outputs, prediction files, and machine-learning artifacts.

The final dashboard primarily reads:

```text
Final_Predicted.xlsx
```

The workbook contains the dashboard data for:

```text
Level_1
Level_2
Level_3
```

---

## 🤖 Machine Learning

The project contains CatBoost-based prediction workflows at the inventory processing levels.

Model artifacts include predictions related to:

- Sales probability
- Age / aging risk
- Location-related classification
- Label-related classification
- Probability ranges

The project also contains probability models for different aging/sales ranges, including:

```text
0–30
30–90
90–150
150–365
365+
```

Model files are stored within the respective level directories under:

```text
L1/models/
L2/models/
L3/models/
```

The dashboard consumes the resulting prediction data rather than training the models every time the Streamlit application is opened.

---

## 📁 Project Structure

```text
Diamond Inventory Intelligence/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── Final_Predicted.xlsx
├── Inventory_SUMMARY_Table.xlsx
├── Inventory_summary_table.py
├── All_files_runner.py
├── Concater.py
│
├── Input/
│   ├── input req.xlsx
│   ├── Inventory_Summary.xlsx
│   ├── Rules.xlsx
│   ├── Sales_Summary.xlsx
│   └── size_range.xlsx
│
├── L1/
│   ├── Data.xlsx
│   ├── Grouped_Sales.xlsx
│   ├── Sales_Prediction.xlsx
│   ├── ML_Prediction_Level1.xlsx
│   ├── models/
│   ├── mapping_function.py
│   └── processing scripts
│
├── L2/
│   ├── Data.xlsx
│   ├── Grouped_Sales.xlsx
│   ├── Sales_Prediction.xlsx
│   ├── ML_Prediction_Level2.xlsx
│   ├── models/
│   └── processing scripts
│
├── L3/
│   ├── Data.xlsx
│   ├── Grouped_Sales.xlsx
│   ├── Sales_Prediction.xlsx
│   ├── ML_Prediction_Level3.xlsx
│   ├── models/
│   └── processing scripts
│
├── Summary Tables/
│   ├── Final_Inventory_Output_L1.xlsx
│   ├── Final_Inventory_Output_L2.xlsx
│   └── Final_Inventory_Output_L3.xlsx
│
└── pages/
    ├── 1_Inventory_Stones.py
    └── 2_Stone_Status.py
```

---

## 🛠️ Technologies Used

### Programming
- Python

### Data Processing
- Pandas
- NumPy
- OpenPyXL

### Visualization
- Plotly

### Machine Learning
- Scikit-learn
- LightGBM
- CatBoost

### Dashboard
- Streamlit

### Data Storage / Intermediate Outputs
- Excel (`.xlsx`)

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Vasu123q/Diamond_Inventory_Intelligence_dashboard.git
cd Diamond_Inventory_Intelligence_dashboard
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Streamlit Dashboard

From the project root:

```bash
streamlit run app.py
```

The application will open in your browser.

The main dashboard provides navigation to:

```text
💎 Diamond Inventory Intelligence
        │
        ├── Inventory Stones
        │
        └── Stone Status
```

---

## ☁️ Streamlit Deployment

The project can be deployed using **Streamlit Community Cloud**.

Use:

```text
Repository: Vasu123q/Diamond_Inventory_Intelligence_dashboard
Branch: main
Main file: app.py
```

The repository already contains:

```text
app.py
requirements.txt
Final_Predicted.xlsx
pages/
```

which are required by the dashboard.

---

## 📊 Main Output

The primary dashboard data source is:

```text
Final_Predicted.xlsx
```

The workbook is read by the Streamlit pages and contains:

```text
Level_1
Level_2
Level_3
```

The application uses this processed data to provide interactive inventory analysis without retraining the machine-learning models during normal dashboard usage.

---

## 🔄 Data Refresh

The Inventory Stones and Stone Status pages include a manual **Refresh Data** option.

The application also uses Streamlit caching to reduce unnecessary repeated Excel reads.

If the underlying `Final_Predicted.xlsx` file changes, the dashboard can detect the modification and prompt the user to refresh the displayed data.

---

## 📌 Notes

- The dashboard depends on the expected project file structure.
- `Final_Predicted.xlsx` should remain in the project root when running or deploying the application.
- The `pages/` directory should remain alongside `app.py`.
- Machine-learning model files are stored under the corresponding L1, L2, and L3 directories.
- The project contains intermediate Excel files generated throughout the processing pipeline.

---

## 👤 Author

**Vasu123q**

GitHub:  
https://github.com/Vasu123q

---

## 📄 License

No license is currently specified for this project.
