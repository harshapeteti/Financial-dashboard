import streamlit as st
import pandas as pd
import plotly.express as px
from scoring import finance_score  #scoring function

@st.cache_data
def load_data():
    return pd.read_csv("processed_financials.csv")


#this is to make recommendations
def generate_recommendations(data, current_score):
    recommendations = []
    gain = 0

    #savings-to-income ratio
    savings_to_income = data["savings"] / data["income"] if data["income"] > 0 else 0
    if savings_to_income < 0.2:
        recommendations.append("Increase savings to at least 20% of income.")
        gain += 5  # Arbitrary points for improvement

    #monthly expenses as a percentage of income
    expenses_to_income = data["monthly_expenses"] / data["income"] if data["income"] > 0 else 0
    if expenses_to_income > 0.5:
        recommendations.append("Reduce monthly expenses to below 50% of income.")
        gain += 7

    #loan payments as a percentage of income
    loan_to_income = data["loan_payments"] / data["income"] if data["income"] > 0 else 0
    if loan_to_income > 0.3:
        recommendations.append("Reduce loan payments to below 30% of income.")
        gain += 5

    #credit card spending
    if data["credit_card_spending"] > data["monthly_expenses"] * 0.3:
        recommendations.append("Reduce discretionary spending by 10%.")
        gain += 3

    #improvement recommendation
    if len(recommendations) == 0:
        recommendations.append("You are on track! Continue maintaining healthy financial habits.")

    return recommendations, gain


st.set_page_config( 
    page_title="Family Financial Health Dashboard",
    layout="wide",
)#configuring the app here.

df = load_data() #dataset loaded as datafram

# using a sidebar to calculate inputs for financial scoring
st.sidebar.header("Input Parameters")
st.sidebar.write("Provide the following inputs to calculate the financial score.")

income = st.sidebar.number_input("Income (in $)", min_value=0, value=50000, step=1000)
savings = st.sidebar.number_input("Savings (in $)", min_value=0, value=8000, step=100)
monthly_expenses = st.sidebar.number_input("Monthly Expenses (in $)", min_value=0, value=2000, step=100)
loan_payments = st.sidebar.number_input("Loan Payments (in $)", min_value=0, value=1500, step=100)
credit_card_spending = st.sidebar.number_input("Credit Card Spending (in $)", min_value=0, value=1000, step=100)

if st.sidebar.button("Calculate Financial Score"): #here, we calculate the finance score
    input_data = {
        "income": income,
        "savings": savings,
        "monthly_expenses": monthly_expenses,
        "loan_payments": loan_payments,
        "credit_card_spending": credit_card_spending,
    } #this data we take as input

    score, insights = finance_score(input_data)

    recommendations, gain = generate_recommendations(input_data, score)

    st.markdown("## Financial Score ")
    st.metric(label="Your Financial Score", value=score)

    st.markdown("### Key Insights ")
    for insight in insights:
        st.write(f"- {insight}") #generating insights here

    st.markdown("### Recommendations for improvement ") # generating the reccomendations here based on deductions.
    for rec in recommendations:
        st.write(f"- {rec}")

    if gain > 0:
        st.info(f"Implementing these changes could improve your score by approximately {gain} points!")

# we begin the main app from here
st.title("Family Financial Health Dashboard ")
st.write("Analyze your financial data and trends to improve financial health.")

# visuals
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Spending Distribution ")
    spending_categories = df[['monthly_expenses', 'loan_payments', 'credit_card_spending']].sum()
    pie_chart = px.pie(
        names=spending_categories.index,
        values=spending_categories.values,
        title="Distribution of Spending Categories",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(pie_chart, use_container_width=True)

with col2:
    st.markdown("### Correlation Heatmap ")
    correlation_matrix = df[['income', 'savings', 'monthly_expenses', 'loan_payments', 'credit_card_spending']].corr()
    heatmap = px.imshow(
        correlation_matrix,
        color_continuous_scale='RdBu',
        title="Correlation Between Financial Metrics",
    )
    st.plotly_chart(heatmap, use_container_width=True)

st.markdown("### Bubble Chart of Income vs Financial Goals ")
bubble_chart = px.scatter(
    df,
    x="income",
    y="financial_goals_met",
    size="savings",
    color="total_spending",
    hover_name="Family ID",
    title="Income vs Financial Goals Met",
    labels={"income": "Income ($)", "financial_goals_met": "Goals Met (%)"},
    color_continuous_scale=px.colors.sequential.Viridis,
)
bubble_chart.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color="DarkSlateGrey")))
st.plotly_chart(bubble_chart, use_container_width=True)

st.markdown("### Data Preview ")
st.write("Below is a sample of the financial dataset used for analysis.")
st.dataframe(df.head(15))
