# Profit Analysis Dashboard (Streamlit)

Clean, seller-focused dashboard to answer: **"Where am I losing money?"**

## Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Data

- Upload a CSV in the app sidebar (prototype works even without upload).
- Expected columns (flexible mapping in the UI):
  - `order_id`, `product_name`, `revenue`, `marketplace_fees`, `taxes`

