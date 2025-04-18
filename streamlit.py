import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

connection = mysql.connector.connect(
    host="gateway01.us-west-2.prod.aws.tidbcloud.com",
    port=4000,
    user="P4iQSrjmBT5xcHr.root",
    password="g9nGrYZlFi6tEsWt",
    database="stock",
    ssl_ca=r"C:\Users\velut\Downloads\isrgrootx1 (1).pem",  
    ssl_verify_cert=True,
    ssl_verify_identity=True
)



choice = st.sidebar.selectbox('Navigation',['Home','Visualization'])

if choice == 'Home':
    st.title('Welcome to Streamlit!')

if choice == 'Visualization':
    st.title("1. Volatility Analysis")

    # Load data from TiDB
    query = "SELECT * FROM Project_stock_analysis.Volatility_Analysis"
    df = pd.read_sql(query, connection)

    # Show data
    st.subheader("Top 10 Most Volatile Stocks")
    st.dataframe(df)

    # Plot bar chart
    st.subheader("Volatility Bar Chart")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='ticker', y='volatility', data=df, palette='viridis')
    plt.title('Top 10 Most Volatile Stocks')
    plt.ylabel('Volatility (Standard Deviation of Daily Returns)')
    plt.xlabel('Stock')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    #####################################################
    st.title("2. Cumulative Return Over Time")

    # Load data from TiDB
    query = "SELECT * FROM Project_stock_analysis.Cumulative_Return"
    df = pd.read_sql(query, connection)

    # Fix data types
    df['date'] = pd.to_datetime(df['date'])
    df['cumulative_return'] = pd.to_numeric(df['cumulative_return'], errors='coerce')

    # Show data
    st.subheader("Cumulative Return for Top 5 Performing Stocks")
    st.dataframe(df)

    # Plot
    import matplotlib.pyplot as plt
    import seaborn as sns

    st.subheader("Cumulative Return Line Chart")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='date', y='cumulative_return', hue='ticker', ax=ax)
    ax.set_title('Cumulative Return Over Time (Top 5 Performing Stocks)')
    ax.set_ylabel('Cumulative Return')
    ax.set_xlabel('Date')
    ax.legend(title='Ticker')
    fig.tight_layout()

    st.pyplot(fig)

    #####################################################
    st.title("3. Sector-wise Performance")

    # Load data from TiDB
    query = "SELECT * FROM Project_stock_analysis.Sector_wise_Performance"
    df = pd.read_sql(query, connection)

    # Convert data types if needed
    df['avg_yearly_return'] = pd.to_numeric(df['avg_yearly_return'], errors='coerce')

    # Sort for better visuals
    df = df.sort_values(by='avg_yearly_return', ascending=False)

    # Show table
    st.subheader("Average Yearly Return by Sector")
    st.dataframe(df)

    # Plotting
    import matplotlib.pyplot as plt

    st.subheader("Sector-wise Average Yearly Return Bar Chart")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df['sector'], df['avg_yearly_return'], color='steelblue')
    ax.set_xlabel('Sector')
    ax.set_ylabel('Average Yearly Return (%)')
    ax.set_title('Sector-wise Average Yearly Return')
    plt.xticks(rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    fig.tight_layout()

    # Show plot in Streamlit
    st.pyplot(fig)

    #####################################################
    st.title("4. Stock Price Correlation")

    # Load data from TiDB
    query = "SELECT * FROM Project_stock_analysis.Stock_Price_Correlation"
    df = pd.read_sql(query, connection)
    
    # Convert to pivot table to get back original correlation matrix format
    corr_matrix = df.pivot(index='ticker', columns='ticker2', values='correlation')

    # Display data
    st.subheader("Correlation Data (Melted Format)")
    st.dataframe(df)

    # Plot heatmap
    st.subheader("Stock Price Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(20, 16))
    sns.heatmap(corr_matrix,
            annot=False,         # Set to True if you want to see the numbers
            cmap='coolwarm',
            linewidths=0.5,
            cbar=True,
            square=True)
    ax.set_title('Stock Price Correlation Heatmap', fontsize=20)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    st.pyplot(fig)

    #####################################################
    st.title("5. Top 5 Gainers and Losers (Month-wise)")

    # Load data from TiDB
    query = "SELECT * FROM Project_stock_analysis.Top_5_Gainers_and_Losers"
    df = pd.read_sql(query, connection)

    # Ensure column names are clean
    df.columns = df.columns.str.strip()

    # Show raw data (optional)
    st.dataframe(df)

    # Sidebar to select a month
    months = df['monthyear'].unique()
    selected_month = st.selectbox("Select Month:", sorted(months))

    # Filter data for the selected month
    month_df = df[df['monthyear'] == selected_month]

    # Calculate top gainers and losers
    top_gainers = month_df.nlargest(5, 'daily_return')
    top_losers = month_df.nsmallest(5, 'daily_return')

    # Layout columns
    col1, col2 = st.columns(2)

    # Top Gainers
    with col1:
      st.subheader(f"Top 5 Gainers - {selected_month}")
      fig1, ax1 = plt.subplots()
      sns.barplot(x='daily_return', y='ticker', data=top_gainers, palette='Greens', ax=ax1)
      ax1.set_xlabel("Monthly Return (%)")
      st.pyplot(fig1)

      # Top Losers
    with col2:
     st.subheader(f"Top 5 Losers - {selected_month}")
     fig2, ax2 = plt.subplots()
     sns.barplot(x='daily_return', y='ticker', data=top_losers, palette='Reds', ax=ax2)
     ax2.set_xlabel("Monthly Return (%)")  # Use ax2
     st.pyplot(fig2)
