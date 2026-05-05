from __future__ import annotations

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Profit Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _currency(x: float) -> str:
    if pd.isna(x):
        return "—"
    return f"${x:,.2f}"


def _pct(x: float) -> str:
    if pd.isna(x):
        return "—"
    return f"{x * 100:.1f}%"


def make_dummy_orders() -> pd.DataFrame:
    # Prototype dataset: includes 2–3 "abusive costs" rows.
    data = [
        {
            "order_id": "A-10421",
            "product_name": "Wireless Earbuds Pro",
            "revenue": 129.90,
            "marketplace_fees": 32.48,
            "taxes": 22.10,
        },
        {
            "order_id": "A-10422",
            "product_name": "Wireless Earbuds Pro",
            "revenue": 129.90,
            "marketplace_fees": 41.20,  # high fee
            "taxes": 26.50,
        },
        {
            "order_id": "B-88210",
            "product_name": "Smartwatch Lite",
            "revenue": 89.00,
            "marketplace_fees": 18.15,
            "taxes": 13.10,
        },
        {
            "order_id": "C-55109",
            "product_name": "USB-C Charger 30W",
            "revenue": 24.99,
            "marketplace_fees": 9.90,  # abusive relative to revenue
            "taxes": 4.85,
        },
        {
            "order_id": "D-33007",
            "product_name": "Laptop Stand (Aluminum)",
            "revenue": 39.90,
            "marketplace_fees": 8.25,
            "taxes": 6.80,
        },
        {
            "order_id": "E-77812",
            "product_name": "Premium Phone Case",
            "revenue": 19.90,
            "marketplace_fees": 6.95,
            "taxes": 4.25,
        },
        {
            "order_id": "F-12003",
            "product_name": "Premium Phone Case",
            "revenue": 19.90,
            "marketplace_fees": 10.25,  # likely unprofitable
            "taxes": 5.95,
        },
    ]
    return pd.DataFrame(data)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df


def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["revenue", "marketplace_fees", "taxes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["total_costs"] = df["marketplace_fees"].fillna(0) + df["taxes"].fillna(0)
    df["net_profit"] = df["revenue"].fillna(0) - df["total_costs"]
    df["profit_margin"] = df["net_profit"] / df["revenue"]
    return df


def inject_css() -> None:
    st.markdown(
        """
        <style>
          /* --- overall typography --- */
          html, body, [class*="css"]  {
            font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif;
          }

          /* --- page background and spacing --- */
          .stApp {
            background: #F7F8FA;
          }

          /* --- header strip (portal-like) --- */
          .pa-header {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 16px;
            padding: 18px 18px;
            border-radius: 14px;
            background: #FFFFFF;
            border: 1px solid rgba(15, 23, 42, 0.06);
            box-shadow: 0 6px 24px rgba(15, 23, 42, 0.06);
            margin-bottom: 14px;
          }
          .pa-title {
            font-size: 20px;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.2;
            margin: 0;
          }
          .pa-subtitle {
            font-size: 12px;
            color: rgba(15, 23, 42, 0.62);
            margin-top: 6px;
          }
          .pa-pill {
            font-size: 12px;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(59, 130, 246, 0.10); /* blue */
            color: rgb(30, 64, 175);
            border: 1px solid rgba(59, 130, 246, 0.22);
            white-space: nowrap;
          }

          /* --- KPI cards --- */
          .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin: 6px 0 10px 0;
          }
          .kpi-card {
            background: #FFFFFF;
            border: 1px solid rgba(15, 23, 42, 0.06);
            border-radius: 14px;
            padding: 14px 14px 12px 14px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
          }
          .kpi-label {
            font-size: 12px;
            color: rgba(15, 23, 42, 0.62);
            margin-bottom: 6px;
          }
          .kpi-value {
            font-size: 22px;
            font-weight: 750;
            color: #0F172A;
            letter-spacing: -0.02em;
          }
          .kpi-delta {
            margin-top: 8px;
            font-size: 12px;
            color: rgba(15, 23, 42, 0.62);
          }
          .tone-good { color: rgb(21, 128, 61); }      /* green */
          .tone-neutral { color: rgb(2, 132, 199); }   /* blue */
          .tone-bad { color: rgb(185, 28, 28); }       /* red */
          .tone-warn { color: rgb(194, 65, 12); }      /* orange */

          /* --- section cards --- */
          .section-card {
            background: #FFFFFF;
            border: 1px solid rgba(15, 23, 42, 0.06);
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
          }
          .section-title {
            font-size: 14px;
            font-weight: 700;
            color: #0F172A;
            margin: 0 0 8px 0;
          }
          .section-caption {
            font-size: 12px;
            color: rgba(15, 23, 42, 0.62);
            margin: 0 0 10px 0;
          }

          /* --- make Streamlit dataframe feel "native" --- */
          div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(15, 23, 42, 0.06);
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_cards(
    *,
    total_orders: int,
    revenue_sum: float,
    fees_taxes_sum: float,
    net_profit_sum: float,
    fees_rate: float,
    profit_margin: float,
    fees_alert_threshold: float,
    margin_alert_threshold: float,
) -> None:
    fees_tone = "tone-warn" if fees_rate >= fees_alert_threshold else "tone-neutral"
    profit_tone = "tone-bad" if profit_margin <= margin_alert_threshold else "tone-good"

    st.markdown(
        f"""
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-delta">Orders in dataset</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Total Revenue (Gross)</div>
            <div class="kpi-value tone-neutral">{_currency(revenue_sum)}</div>
            <div class="kpi-delta">Before fees & taxes</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Total Fees & Taxes (Net Cost)</div>
            <div class="kpi-value {fees_tone}">{_currency(fees_taxes_sum)}</div>
            <div class="kpi-delta">Share of revenue: <b>{_pct(fees_rate)}</b></div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Net Profit</div>
            <div class="kpi-value {profit_tone}">{_currency(net_profit_sum)}</div>
            <div class="kpi-delta">Net margin: <b>{_pct(profit_margin)}</b></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_alert_table(df: pd.DataFrame, low_margin_threshold: float) -> pd.io.formats.style.Styler:
    def net_profit_cell_style(value: float, is_flagged: bool) -> str:
        if pd.isna(value):
            return ""
        if is_flagged:
            return "background-color: rgba(239, 68, 68, 0.14); color: rgb(127, 29, 29); font-weight: 700;"
        return "color: rgb(15, 23, 42); font-weight: 600;"

    def row_border_style(_: pd.Series) -> str:
        return "border-bottom: 1px solid rgba(15, 23, 42, 0.06);"

    margin = pd.to_numeric(df.get("Profit Margin"), errors="coerce")
    profit = pd.to_numeric(df.get("Net Profit"), errors="coerce")
    flagged = (profit < 0) | (margin < low_margin_threshold)

    def style_net_profit_col(col: pd.Series) -> list[str]:
        # We need the row index to align styles with `flagged`.
        return [net_profit_cell_style(v, bool(flagged.loc[idx])) for idx, v in col.items()]

    styler = (
        df.style.format(
            {
                "Revenue": _currency,
                "Marketplace Fees": _currency,
                "Taxes": _currency,
                "Net Profit": _currency,
                "Profit Margin": _pct,
            }
        )
        .apply(lambda r: [row_border_style(r)] * len(r), axis=1)
        .apply(style_net_profit_col, subset=["Net Profit"], axis=0)
        .set_properties(**{"font-size": "13px"})
    )
    return styler


inject_css()


with st.sidebar:
    st.markdown("### Data")
    uploaded_file = st.file_uploader("Upload orders CSV", type=["csv"], accept_multiple_files=False)

    st.markdown("### Alerts")
    low_margin_threshold = st.slider(
        "Low profit margin threshold",
        min_value=0.0,
        max_value=0.5,
        value=0.10,
        step=0.01,
        help="Rows are flagged when Net Profit is negative or margin is below this value.",
    )
    fees_alert_threshold = st.slider(
        "Fees & taxes share alert",
        min_value=0.0,
        max_value=1.0,
        value=0.35,
        step=0.01,
        help="KPI turns orange/red when Fees+Taxes share exceeds this value.",
    )

    st.markdown("### Column mapping")
    st.caption("If your CSV uses different names, map them here.")


def _is_streamlit_upload(x: object) -> bool:
    # Defensive: ensures we don't treat a stray float/str as an upload handle.
    return hasattr(x, "read") and hasattr(x, "name")


if uploaded_file is not None and _is_streamlit_upload(uploaded_file):
    raw = pd.read_csv(uploaded_file)
    raw = normalize_columns(raw)
    source_label = uploaded_file.name
else:
    if uploaded_file is not None and not _is_streamlit_upload(uploaded_file):
        st.warning("Upload control returned an unexpected value; using prototype data instead.")
    raw = make_dummy_orders()
    raw = normalize_columns(raw)
    source_label = "orders.csv (prototype)"


col_options = list(raw.columns)
default_map = {
    "order_id": "order_id" if "order_id" in raw.columns else (col_options[0] if col_options else ""),
    "product_name": "product_name" if "product_name" in raw.columns else (col_options[1] if len(col_options) > 1 else ""),
    "revenue": "revenue" if "revenue" in raw.columns else "",
    "marketplace_fees": "marketplace_fees" if "marketplace_fees" in raw.columns else "",
    "taxes": "taxes" if "taxes" in raw.columns else "",
}

with st.sidebar:
    m_order_id = st.selectbox("Order ID", options=col_options, index=col_options.index(default_map["order_id"]) if default_map["order_id"] in col_options else 0)
    m_product = st.selectbox("Product Name", options=col_options, index=col_options.index(default_map["product_name"]) if default_map["product_name"] in col_options else 0)
    m_revenue = st.selectbox("Revenue", options=col_options, index=col_options.index(default_map["revenue"]) if default_map["revenue"] in col_options else 0)
    m_fees = st.selectbox("Marketplace Fees", options=col_options, index=col_options.index(default_map["marketplace_fees"]) if default_map["marketplace_fees"] in col_options else 0)
    m_taxes = st.selectbox("Taxes", options=col_options, index=col_options.index(default_map["taxes"]) if default_map["taxes"] in col_options else 0)


df = raw.rename(
    columns={
        m_order_id: "order_id",
        m_product: "product_name",
        m_revenue: "revenue",
        m_fees: "marketplace_fees",
        m_taxes: "taxes",
    }
)

required = {"order_id", "product_name", "revenue", "marketplace_fees", "taxes"}
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Missing required columns after mapping: {missing}")
    st.stop()

df = compute_metrics(df)


# --- Header ---
st.markdown(
    f"""
    <div class="pa-header">
      <div>
        <div class="pa-title">Profit Analysis Dashboard</div>
        <div class="pa-subtitle">Where am I losing money? Flag orders with low net profit, high taxes, and excessive marketplace fees.</div>
      </div>
      <div class="pa-pill">Data Source: <b>{source_label}</b></div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --- KPI row ---
total_orders = int(df.shape[0])
revenue_sum = float(df["revenue"].fillna(0).sum())
fees_taxes_sum = float(df["total_costs"].fillna(0).sum())
net_profit_sum = float(df["net_profit"].fillna(0).sum())
fees_rate = (fees_taxes_sum / revenue_sum) if revenue_sum else float("nan")
profit_margin = (net_profit_sum / revenue_sum) if revenue_sum else float("nan")

kpi_cards(
    total_orders=total_orders,
    revenue_sum=revenue_sum,
    fees_taxes_sum=fees_taxes_sum,
    net_profit_sum=net_profit_sum,
    fees_rate=fees_rate,
    profit_margin=profit_margin,
    fees_alert_threshold=fees_alert_threshold,
    margin_alert_threshold=low_margin_threshold,
)


# --- Alerts table (main visual weight) ---
st.markdown(
    """
    <div class="section-card">
      <div class="section-title">Low Profit Alerts</div>
      <div class="section-caption">
        Rows are flagged when Net Profit is negative or Profit Margin is below your threshold.
        Sort by <b>Net Profit</b> or <b>Profit Margin</b> to find the worst offenders first.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

display = df.copy()
display["Profit Margin"] = display["profit_margin"]
display = display.rename(
    columns={
        "order_id": "Order ID",
        "product_name": "Product Name",
        "revenue": "Revenue",
        "marketplace_fees": "Marketplace Fees",
        "taxes": "Taxes",
        "net_profit": "Net Profit",
    }
)

display = display[["Order ID", "Product Name", "Revenue", "Marketplace Fees", "Taxes", "Net Profit", "Profit Margin"]]
display = display.sort_values(by=["Net Profit", "Profit Margin"], ascending=[True, True], na_position="last")

st.dataframe(
    style_alert_table(display, low_margin_threshold=low_margin_threshold),
    width="stretch",
    height=360,
)


# --- Cost breakdown (optional, preferred) ---
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-card">
      <div class="section-title">Cost Breakdown (Selected Product)</div>
      <div class="section-caption">
        Visualize how much of each sale is consumed by marketplace fees + taxes.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

products = sorted([p for p in df["product_name"].dropna().unique().tolist()])
if not products:
    st.info("No products found to chart.")
else:
    left, right = st.columns([1, 2], vertical_alignment="top")
    with left:
        selected_product = st.selectbox("Product", options=products, index=0)
        subset = df[df["product_name"] == selected_product].copy()
        subset = subset.sort_values(by="profit_margin", ascending=True)

        st.markdown("**Key stats**")
        # Keep all values as strings to avoid Arrow serialization issues
        # (e.g., mixing ints with "$12.34" in the same column).
        key_stats = pd.DataFrame(
            {
                "Metric": ["Orders", "Avg Revenue", "Avg Fees+Taxes", "Avg Net Profit", "Avg Margin"],
                "Value": [
                    f"{int(subset.shape[0])}",
                    _currency(float(subset["revenue"].mean())),
                    _currency(float(subset["total_costs"].mean())),
                    _currency(float(subset["net_profit"].mean())),
                    _pct(float(subset["profit_margin"].mean())),
                ],
            }
        )
        st.dataframe(
            key_stats,
            width="stretch",
        )

    with right:
        chart_df = subset[["order_id", "marketplace_fees", "taxes", "net_profit"]].copy()
        chart_df = chart_df.rename(
            columns={
                "order_id": "Order",
                "marketplace_fees": "Marketplace Fees",
                "taxes": "Taxes",
                "net_profit": "Net Profit",
            }
        ).set_index("Order")

        st.caption("Each bar shows the composition of the transaction outcome (costs vs profit).")
        st.bar_chart(chart_df, height=240, stack=False)

