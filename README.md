# Food Ordering Behaviour and Consumer Trends

An interactive data analytics project built with Python, Pandas, Plotly and Streamlit.

## Features
- Upload a CSV dataset or use the included 600-row synthetic sample
- Data cleaning: duplicate removal, missing-value handling, type conversion
- Interactive filters for city, platform and food category
- KPI cards: total orders, average order value, rating and delivery time
- Visualizations for food preferences, platform choice, age-group spending, order timing, delivery and ratings
- Download cleaned and filtered datasets

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:
   `pip install -r requirements.txt`
5. Start the app:
   `streamlit run app.py`

## Dataset
`data/food_orders_sample.csv` contains generated synthetic data. It is suitable for demonstrating the dashboard and code, not for claiming actual consumer behaviour. For academic submission, collect survey responses or use a properly cited public dataset and document its source.

## CSV format
Your uploaded CSV should contain these columns:
`order_id, order_date, city, age_group, food_category, platform, order_time, order_amount, payment_method, delivery_minutes, rating, orders_per_month`

## Suggested project workflow
1. Data collection: Google Forms or a public dataset with source citation.
2. Data preparation: inspect missing values, duplicates, invalid values and outliers.
3. Visualization: compare categories, platforms, spending and delivery experience.
4. Dashboard: use the Streamlit app; optional Power BI recreation.
5. Story: write conclusions based only on observed results.
6. Testing: test filters, empty selections, CSV upload and download buttons.

## GitHub upload
Create a new public repository on GitHub, for example `food-ordering-consumer-trends`.
Then, from this folder run:

```bash
git init
git add .
git commit -m "Initial food ordering trends analytics project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/food-ordering-consumer-trends.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.
