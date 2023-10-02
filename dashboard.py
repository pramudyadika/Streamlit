import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.header('Ecommerce Dashboard :money_with_wings: ')

def create_top_state_cust(all_df):
    top_state_cust = all_df.customer_state.value_counts().head(10).sort_values(ascending=True)
    
    return top_state_cust

def create_top_payments_type(all_df):
    top_payments_type = all_df.payment_type.value_counts().head(10).sort_values(ascending=True)

    return top_payments_type

def create_top_state_sellers(all_df):
    top_state_sellers = all_df.seller_state.value_counts().head(10).sort_values(ascending=True)
    
    return top_state_sellers

def create_monthly_orders(all_df):
    all_df['order_purchase_timestamp'] = all_df['order_purchase_timestamp'].apply(pd.to_datetime)
    monthly_orders = all_df.set_index('order_purchase_timestamp')
    
    return monthly_orders

def create_top_recency_plot(all_df):
    #Define newest date
    newest_date = all_df['order_purchase_timestamp'].max()
    df_recency = all_df.groupby(['customer_unique_id'], as_index = False)['order_purchase_timestamp'].max()

    df_recency['recency'] = df_recency['order_purchase_timestamp'].apply(lambda x: (newest_date - x).days)

    top_cust_recency = df_recency.sort_values(by="recency", ascending=True).head(5)
    top_cust_recency = top_cust_recency.set_index('customer_unique_id')
    top_recency_plot = top_cust_recency.drop(['order_purchase_timestamp'], axis=1)
    
    return top_recency_plot

def create_top_frequency_plot(all_df):
    df_frequency = pd.DataFrame(all_df.groupby(["customer_unique_id"], as_index = False).agg({"order_id":"nunique"}))
    df_frequency.rename(columns={"order_id":"frequency"}, inplace=True)

    top_freq = df_frequency.sort_values(by="frequency", ascending=True).head(5)
    top_cust_freq = top_freq.set_index('customer_unique_id')

    return top_cust_freq

def create_top_monetary_plot(all_df):
    df_monetary = all_df.groupby('customer_unique_id', as_index=False)['payment_value'].sum()
    df_monetary.rename(columns={"payment_value":"monetary"}, inplace=True)

    top_monetary = df_monetary.sort_values(by="monetary", ascending=False).head(5)
    top_cust_monetary = top_monetary.set_index('customer_unique_id')

    return top_cust_monetary

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

with st.sidebar:
    
     # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

top_state_cust = create_top_state_cust(main_df)
top_state_sellers = create_top_state_sellers(main_df)
top_payments_type = create_top_payments_type(main_df)
monthly_orders = create_monthly_orders(main_df)
top_recency_plot = create_top_recency_plot(main_df)
top_frequency_plot = create_top_frequency_plot(main_df)
top_monetary_plot = create_top_monetary_plot(main_df)


st.subheader("States Demographic")
col1, col2 = st.columns(2)

with col1:
    # Plot
    plt.figure(figsize=(6, 6))
    top_state_cust.plot(kind='barh', color='teal')
    plt.title('Top 10 Customer States')
    plt.xlabel('Count')
    plt.ylabel('Customer State')
    plt.xticks(rotation=45)
    st.pyplot()

with col2:
    plt.figure(figsize=(6, 6))
    top_state_sellers.plot(kind='barh', color='darkgreen')
    plt.title('Top 10 Sellers States')
    plt.xlabel('Count')
    plt.ylabel('Sellers State')
    plt.xticks(rotation=45)
    st.pyplot()

st.subheader("Payment Type")
plt.figure(figsize=(6, 6))
top_payments_type.plot(kind='barh', color='darkblue')
plt.title('Top 5 Payments Type')
plt.xlabel('Count')
plt.ylabel('Payments Type')
plt.xticks(rotation=45)
st.pyplot()

st.subheader("Monthly Orders")
plt.figure(figsize=(6, 3))
monthly_orders.resample('M')['order_id'].count().plot()
plt.title('Monthly Orders')
plt.xlabel('Month')
plt.ylabel('Count')
plt.xticks(rotation=0)
st.pyplot()

st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    plt.figure(figsize=(3, 3))
    top_recency_plot.plot(kind='bar', color='turquoise')
    plt.title('Top 5 Customer by Recency')
    plt.xlabel('Consumers ID')
    plt.ylabel('Recency(Days)')
    plt.xticks(rotation=90)
    st.pyplot()
 
with col2:
    plt.figure(figsize=(3, 3))
    top_frequency_plot.plot(kind='bar', color='turquoise')
    plt.title('Top 5 Customer by Frequency')
    plt.xlabel('Customer ID')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    st.pyplot()
 
with col3:
    plt.figure(figsize=(3, 3))
    top_monetary_plot.plot(kind='bar', color='turquoise')
    plt.title('Top 5 Customer by Monetary')
    plt.xlabel('Customer ID')
    plt.ylabel('Monetary')
    plt.xticks(rotation=90)
    st.pyplot()