import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='ME', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_purchase_timestamp": "order_date", 
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    
    return monthly_orders_df

def create_order_status_df(df):
    order_status_df = df.groupby(by="order_status").agg({
        "order_id": "nunique"
    })
    order_status_df = order_status_df.reset_index()
    order_status_df["total_order"] = df["order_id"].count()
    order_status_df["percentage"] = order_status_df["order_id"] / order_status_df["total_order"] * 100

    order_status_df.rename(columns={
        "order_id": "order_count",
    }, inplace=True)
    
    return order_status_df

def create_rfm_customer_df(df):
    rfm_customer_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max", 
        "order_item_id": "nunique",
        "payment_value": "sum"
    })
    rfm_customer_df = rfm_customer_df.rename(columns={
        "order_purchase_timestamp": "max_order_timestamp", 
        "order_item_id": "frequency", 
        "payment_value": "monetary"
    })

    rfm_customer_df["max_order_timestamp"] = rfm_customer_df["max_order_timestamp"].dt.date
    recent_date = all_df["order_purchase_timestamp"].dt.date.max()
    rfm_customer_df["recency"] = rfm_customer_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    
    
    return rfm_customer_df

def create_rfm_seller_df(df):
    rfm_seller_df = df.groupby(by="seller_id", as_index=False).agg({
        "order_purchase_timestamp": "max", 
        "order_id": "nunique", 
        "payment_value": "sum", 
        "review_score": "mean"
    })

    rfm_seller_df = rfm_seller_df.rename(columns={
        "order_purchase_timestamp": "max_order_timestamp", 
        "order_id": "frequency", 
        "payment_value": "monetary", 
        "review_score": "avg_score"
    }).sort_values(by="frequency", ascending=False)

    rfm_seller_df["avg_score"] = rfm_seller_df["avg_score"].apply(lambda x: round(x, 1)) 
    rfm_seller_df["max_order_timestamp"] = rfm_seller_df["max_order_timestamp"].dt.date
    recent_date = all_df["order_purchase_timestamp"].dt.date.max()
    rfm_seller_df["recency"] = rfm_seller_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

    return rfm_seller_df

all_df = pd.read_csv("Olist_data.csv")

datetime_columns = ["order_purchase_timestamp"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    
    st.image("Olist logo.png")

    st.subheader("By : FAKHRIAKMAL")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

monthly_orders_df = create_monthly_orders_df(main_df)
order_status_df = create_order_status_df(main_df)
rfm_customer_df = create_rfm_customer_df(main_df)
rfm_seller_df = create_rfm_seller_df(main_df)

st.header('Olist Brazillian E-Commerce')

st.markdown("[Datasets](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/code)")

st.subheader('Monthly Orders')

col1, col2 = st.columns(2)
 
with col1:
    total_orders = monthly_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(monthly_orders_df.revenue.sum(), "EUR", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df["order_date"],
    monthly_orders_df["order_count"],
    marker='o', 
    linewidth=5,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader('Orders Performance')
 
col1, col2 = st.columns(2)
 
with col1:
    delivered_df = order_status_df[order_status_df["order_status"] == 'delivered']
    undelivered_df = order_status_df[order_status_df["order_status"] != "delivered"]
    delivered = delivered_df['order_count'].sum()
    undelivered = undelivered_df['order_count'].sum()
    st.metric("Undelivered Order", value=undelivered)
 
with col2:
    avg_score = main_df['review_score'].mean()
    avg_score = round(avg_score, 2)
    st.metric("Average Score", value=avg_score)

#

col1, col2 = st.columns(2)
 
with col1:
    percent_delivered_df = delivered_df["percentage"]
    percent_undelivered_df = 100 - percent_delivered_df

    percent_delivered = percent_delivered_df.sum()
    percent_undelivered = percent_undelivered_df.iloc[0]

    sizes = [percent_delivered, percent_undelivered]
    labels = ['Delivered', 'Undelivered']
    colors = ['#66b3ff', 'red']

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        sizes, 
        labels=labels, 
        colors=colors, 
        autopct='%1.1f%%', 
        startangle=90, 
        wedgeprops={'edgecolor': 'black'}
    )
    ax.set_title("Order Status Distribution (Delivered vs. Undelivered)")
    st.pyplot(fig)

with col2:
    review_score_counts = main_df["review_score"].value_counts().reset_index()
    review_score_counts.columns = ['review_score', 'total_orders']
    review_score_counts = review_score_counts.sort_values(by='review_score', ascending=True).reset_index(drop=True)
    review_score_counts["all_order"] = main_df["order_id"].count()
    review_score_counts["percentage"] = review_score_counts["total_orders"] / review_score_counts["all_order"] * 100

    score_1 = review_score_counts["percentage"].iloc[0]
    score_2 = review_score_counts["percentage"].iloc[1]
    score_3 = review_score_counts["percentage"].iloc[2]
    score_4 = review_score_counts["percentage"].iloc[3]
    score_5 = review_score_counts["percentage"].iloc[4]

    size = [score_1, score_2, score_3, score_4, score_5]
    label = ["1 Star", "2 Star", "3 Star", "4 Star", "5 Star"]
    cmap = plt.get_cmap("Blues")  
    color = [cmap(i / len(size)) for i in range(len(size))]

    highlight_index = 0
    color[highlight_index] = 'red'

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        size, 
        labels=label, 
        colors=color, 
        autopct='%1.1f%%', 
        startangle=90, 
        wedgeprops={'edgecolor': 'black'}
    )
    ax.set_title("Order Performance by Star Score")
    st.pyplot(fig)

#

st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_customer_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_customer_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_monetary = format_currency(rfm_customer_df.monetary.mean(), "EUR", locale='es_CO') 
    st.metric("Average Monetary", value=avg_monetary)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(40, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(
    y="recency", 
    x="customer_id", 
    data=rfm_customer_df.sort_values(by="recency", ascending=True).head(5), 
    palette=colors, 
    ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35, rotation=90)
 
sns.barplot(
    y="frequency", 
    x="customer_id", 
    data=rfm_customer_df.sort_values(by="frequency", ascending=False).head(5), 
    palette=colors, 
    ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35, rotation=90)
 
sns.barplot(
    y="monetary", 
    x="customer_id", 
    data=rfm_customer_df.sort_values(by="monetary", ascending=False).head(5), 
    palette=colors, 
    ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35, rotation=90)
 
st.pyplot(fig)
 