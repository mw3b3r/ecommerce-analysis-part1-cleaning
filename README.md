# 🧼 E-commerce Analysis – Part 1: Data Cleaning

This repository contains the first part of an e-commerce data analysis project: **data cleaning**.

The dataset includes anonymized sales transactions from an online store. Before any meaningful analysis or visualization can take place, the data must be cleaned and prepared. This step ensures that the data is reliable, consistent, and ready for further exploration.

---

## 📂 Data Access

To keep the repository lightweight, the dataset is **not included directly here** due to file size limitations.

Instead, you can download both the **raw** and **cleaned** versions of the dataset from this Kaggle link:

🔗 [E-Commerce Sales Data (Raw & Cleaned) on Kaggle](https://www.kaggle.com/datasets/martweber/e-commerce-sales-data-raw-cleaned)

### Contents:
- `ecommerce_raw_data.csv` – Original messy dataset  
- `cleaned_sales_data.csv` – Cleaned and processed version used in further analysis

> Once downloaded, place the files in your working directory to run the cleaning script or continue with part 2 of the analysis.

---

## 📋 Dataset Overview

Each row in the original dataset represents a line item in a customer transaction and includes:

- `TransactionNo`: Unique transaction identifier
- `CustomerNo`: Unique customer identifier
- `Date`: Purchase date
- `ProductName`: Product description
- `Quantity`: Number of items sold
- `Price`: Price per item
- `Country`: Customer's country

---

## 🧹 Data Cleaning Steps

The cleaning script performs the following operations:

- Converts data types (e.g., `Date` to datetime)
- Removes empty or missing product names
- Handles negative quantities and identifies product returns
- Drops rows with invalid prices or missing transaction info
- Removes test rows (e.g., entries marked as cancelled or test orders)
- Calculates total revenue per row (`Revenue = Quantity × Price`)
- Creates a `ReturnFlag` column to identify returns

The final cleaned dataset is saved as `cleaned_sales_data.csv`.

---

## 🚀 How to Use

1. Clone the repository or download the files
2. Make sure you have `pandas` and `numpy` installed
3. Run the cleaning script:

```bash
python sales_transactions_cleaning.py
```
---

## ✅ What’s Next?

This is **Part 1** of a multi-stage e-commerce data project.

📊 In [Part 2 – Interactive Analysis in Streamlit](https://github.com/mw3b3r/ecommerce-analysis-part1-cleaning), you'll find dynamic dashboards and visual insights built using the cleaned dataset.

---

## 🧠 Why This Project?

This project was created as a **portfolio piece** to demonstrate real-world data preparation skills using Python. It focuses on:

- 🔍 Identifying and fixing common data quality issues  
- 🧼 Writing clean and readable data cleaning logic  
- 🔁 Creating a reusable, reproducible cleaning pipeline

Whether you're preparing data for machine learning, BI tools, or dashboard apps, this kind of preprocessing is a foundational step for trustworthy insights.

---

