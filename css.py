import streamlit as st 
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def show_charts(expenses):
    PALETTE = [
        "#6366F1", "#8B5CF6", "#EC4899", "#F59E0B",
        "#10B981", "#3B82F6", "#EF4444", "#14B8A6",
    ]
    
    BG_CARD  = "#1E1F2E"
    TEXT_PRI = "#F1F5F9"
    TEXT_SEC = "#94A3B8"
    
    PLOTLY_LAYOUT = dict(
        paper_bgcolor="#000000",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_PRI),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    
    # ── Page Config ───────────────────────────────────────────────────────────────
    st.set_page_config(
        page_title="Expense Manager",
        page_icon="💸",
        layout="wide",
    )
    
    # ── Scoped CSS — only metric cards and chart wrappers, sidebar untouched ──────
    st.markdown(f"""
    <style>
    /* Metric cards */
    [data-testid="metric-container"] {{
        background: {BG_CARD};
        border: 1px solid rgba(99,102,241,.25);
        border-radius: 16px;
        padding: 20px 24px;
    }}
    [data-testid="metric-container"] label {{
        color: {TEXT_SEC} !important;
        font-size: .78rem;
        letter-spacing: .08em;
        text-transform: uppercase;
    }}
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        font-weight: 700;
        color: {TEXT_PRI} !important;
    }}
    
    /* Chart card wrapper */
    .chart-card {{
        background: {BG_CARD};
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 8px;
    }}
    .chart-card .ct {{
        font-size: 1rem;
        font-weight: 600;
        color: {TEXT_PRI};
        margin: 0 0 2px;
    }}
    .chart-card .cs {{
        font-size: .8rem;
        color: {TEXT_SEC};
        margin: 0 0 12px;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # ═════════════════════════════════════════════════════════════════════════════
    #  `expenses` DataFrame must already exist in scope before this file runs.
    # ═════════════════════════════════════════════════════════════════════════════
    if "expenses" not in dir():
        raise NameError("`expenses` DataFrame not found.")
    
    # ── Data Preparation ──────────────────────────────────────────────────────────
    expenses["amount"] = pd.to_numeric(expenses["amount"], errors="coerce").fillna(0)
    
    category_df = (
        expenses.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )
    
    total_expense    = expenses["amount"].sum()
    num_transactions = len(expenses)
    top_category     = category_df.iloc[0]["category"] if not category_df.empty else "N/A"
    
    # ── Page Title ────────────────────────────────────────────────────────────────
    st.title("💸 Spending Overview")
    st.caption("A clear picture of where your money goes")
    st.markdown("---")
    
    # ── KPI Metrics ───────────────────────────────────────────────────────────────
    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Total Expenses", f"NPR {total_expense:,.2f}")
    with k2:
        st.metric("No of Expenses", f"{num_transactions:,}")
    with k3:
        st.metric("Top Category", top_category)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Charts ────────────────────────────────────────────────────────────────────
    col_bar, col_donut = st.columns([3, 2], gap="large")
    
    # ── 1. Horizontal Bar Chart ───────────────────────────────────────────────────
    with col_bar:
        st.markdown(
            '<div class="chart-card">'
            '<p class="ct">Category-wise Spending</p>'
            '<p class="cs">Ranked by total expenditure</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    
        bar_df = category_df.sort_values("amount", ascending=True)
        n = len(bar_df)
    
        fig_bar = go.Figure(go.Bar(
            x=bar_df["amount"],
            y=bar_df["category"],
            orientation="h",
            marker=dict(
                color=[PALETTE[i % len(PALETTE)] for i in range(n)],
                line=dict(width=0),
            ),
            text=[f"NPR {v:,.0f}" for v in bar_df["amount"]],
            textposition="outside",
            textfont=dict(size=14, color="#FFFFFF"),
            hovertemplate="<b>%{y}</b><br>NPR %{x:,.2f}<extra></extra>",
        ))
    
        fig_bar.update_layout(
            **PLOTLY_LAYOUT,
            height=max(300, n * 54),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=13, color=TEXT_PRI)),
            bargap=0.35,
        )
    
        st.plotly_chart(fig_bar, width="content", config={"displayModeBar": False})
    
    # ── 2. Donut Chart ────────────────────────────────────────────────────────────
    with col_donut:
        st.markdown(
            '<div class="chart-card">'
            '<p class="ct">Expense Distribution</p>'
            '<p class="cs">Share of each category</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    
        fig_donut = go.Figure(go.Pie(
            labels=category_df["category"],
            values=category_df["amount"],
            hole=0.62,
            marker=dict(
                colors=[PALETTE[i % len(PALETTE)] for i in range(len(category_df))],
                line=dict(color=BG_CARD, width=3),
            ),
            textinfo="percent",
            textfont=dict(size=12, color=TEXT_PRI),
            hovertemplate="<b>%{label}</b><br>NPR %{value:,.2f} (%{percent})<extra></extra>",
            direction="clockwise",
            sort=True,
        ))
    
        fig_donut.add_annotation(
            text=f"<b>NPR {total_expense:,.0f}</b><br><span style='font-size:11px'>Total</span>",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=15, color=TEXT_PRI),
            align="center",
        )
    
        fig_donut.update_layout(
            **PLOTLY_LAYOUT,
            height=360,
            showlegend=True,
            legend=dict(
                orientation="v",
                x=1.02, y=0.5,
                font=dict(size=11, color=TEXT_SEC),
                bgcolor="rgba(0,0,0,0)",
            ),
        )
    
        st.plotly_chart(fig_donut, width="content", config={"displayModeBar": False})


def css_add_expense():
    st.markdown("""
    <style>
 
      /* Center the form */
      [data-testid="stForm"] {
          background: #1a1a1a;
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 16px;
          padding: 32px 36px;
          max-width: 620px;
          margin: 60px auto;
      }
 
      /* Form subheader */
      [data-testid="stForm"] h3 {
          color: #ffffff;
          font-size: 1.2rem;
          font-weight: 600;
          margin-bottom: 20px;
      }
 
      /* Input labels */
      [data-testid="stForm"] label {
          color: #aaaaaa !important;
          font-size: 0.82rem !important;
      }
 
      /* Submit button */
      [data-testid="stForm"] button[kind="primaryFormSubmit"] {
          width: 100%;
          background-color: #ffffff;
          color: #000000;
          border: none;
          border-radius: 10px;
          padding: 10px;
          font-weight: 600;
          font-size: 0.9rem;
          margin-top: 8px;
          cursor: pointer;
      }
 
      [data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
          background-color: #e0e0e0;
      }
 
    </style>
    """, unsafe_allow_html=True)


def css_webapp():
    st.markdown("""
    <style>
 
      /* Page background */
      .st-emotion-cache-13k62yr {
          background: #000000;
          color-scheme: dark;
      }
 
      /* Main content padding */
      .st-emotion-cache-zy6yx3 {
          width: 100%;
          padding: 60px;
          max-width: initial;
          min-width: auto;
      }
 
      /* Top header bar */
      .st-emotion-cache-wyoiad {
          background: #000000;
      }
 
      /* Sidebar background */
      [data-testid="stSidebar"] {
          background-color: #1a1a1a;
      }
 
      /* Sidebar all text white */
      [data-testid="stSidebar"] * {
          color: #ffffff !important;
      }
 
    </style>
    """, unsafe_allow_html=True)