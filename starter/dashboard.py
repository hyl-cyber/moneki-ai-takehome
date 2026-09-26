import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="门店经营看板", layout="wide")
st.title("🏪 门店经营数据看板")

# 侧边栏筛选
with st.sidebar:
    st.header("筛选条件")
    start_date = st.date_input("起始日期")
    end_date = st.date_input("结束日期")
    store_str = st.text_input("门店ID，逗号分隔", value="1,2")

# 1. 汇总指标卡片
try:
    resp_summary = requests.get(
        f"{API_BASE}/api/metrics/summary",
        params={
            "start": str(start_date),
            "end": str(end_date),
            "store_id": store_str
        },
        timeout=10
    )
    summary_data = resp_summary.json()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("净营业额", summary_data["net_revenue"])
    col2.metric("订单总数", summary_data["orders"])
    col3.metric("退款金额", summary_data["refund_amount"])
    col4.metric("平均客单价", summary_data["aov"])

except Exception as e:
    st.error(f"汇总指标接口失败：{e}")

st.divider()

# 2. 每日数据
try:
    resp_daily = requests.get(
        f"{API_BASE}/api/metrics/daily",
        params={
            "start": str(start_date),
            "end": str(end_date),
            "store_id": store_str
        },
        timeout=10
    )
    daily_data = resp_daily.json()
    daily_list = daily_data["days"]

    # 清洗脏数据
    clean_daily = []
    for item in daily_list:
        if isinstance(item, dict) and "date" in item and item["date"] is not None:
            clean_daily.append(item)

    if len(clean_daily) > 0:
        df_daily = pd.DataFrame(clean_daily)
        df_daily["date"] = pd.to_datetime(df_daily["date"])
        df_daily = df_daily.sort_values("date")

        # 图1：每日净营业额
        fig_revenue = px.line(
            df_daily,
            x="date",
            y="net_revenue",
            title="📈 每日净营业额趋势"
        )
        fig_revenue.update_layout(
            xaxis_title="日期",
            yaxis_title="净营收",
            showlegend=False
        )
        fig_revenue.update_traces(line_width=2)
        st.plotly_chart(fig_revenue, use_container_width=True)

        # 图2：每日订单数
        fig_order = px.line(
            df_daily,
            x="date",
            y="orders",
            title="📊 每日订单数量趋势"
        )
        fig_order.update_layout(
            xaxis_title="日期",
            yaxis_title="订单数",
            showlegend=False
        )
        fig_order.update_traces(line_width=2)
        st.plotly_chart(fig_order, use_container_width=True)

        # 图3：每日客单价
        fig_aov = px.line(
            df_daily,
            x="date",
            y="aov",
            title="💵 每日客单价趋势"
        )
        fig_aov.update_layout(
            xaxis_title="日期",
            yaxis_title="客单价",
            showlegend=False
        )
        fig_aov.update_traces(line_width=2, line_color="#2ca02c")
        st.plotly_chart(fig_aov, use_container_width=True)

    else:
        st.warning("暂无有效每日数据")

except Exception as e:
    st.error(f"每日指标接口失败：{e}")