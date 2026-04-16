import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Hyperliquid Analytics", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv('merged_trading_data.csv')
    df['date'] = df['TradeDate']
    return df

df = load_data()

st.sidebar.header("Filter Options")
selected_sentiment = st.sidebar.multiselect(
    "Select Market Sentiment", 
    options=df['classification'].unique(),
    default=df['classification'].unique()
)


mask = df['classification'].isin(selected_sentiment)
filtered_df = df[mask]


st.title("Trade Performance Dashboard")
st.markdown("Exploring the relationship between **Market Sentiment** and **Trader Profitability**.")


col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Trades", len(filtered_df))
with col2:
    st.metric("Avg PnL", f"${filtered_df['Closed PnL'].mean():.2f}")
with col3:
    win_rate = (filtered_df['Closed PnL'] > 0).mean()
    st.metric("Win Rate", f"{win_rate:.1%}")

st.divider()


c1, c2 = st.columns(2)

with c1:
    st.subheader("PnL Distribution by Sentiment")
    fig_pnl = px.box(filtered_df, x='classification', y='Closed PnL', 
                     color='classification', points=False)
    st.plotly_chart(fig_pnl, use_container_width=True)

with c2:
    st.subheader("Trade Frequency Heatmap")
    heat_data = filtered_df.groupby(['date', 'classification']).size().reset_index(name='Trade Count')
    fig_heat = px.density_heatmap(heat_data, x='date', y='classification', z='Trade Count',
                                  color_continuous_scale='Viridis')
    st.plotly_chart(fig_heat, use_container_width=True)


