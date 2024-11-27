# Financial-dashboard
Describes the financial health based on income, savings, credit card spending and loan payments through a small dataset

## Setup

### 1. clone the repository

```bash
git clone https://github.com/harshapeteti/financial-health-dashboard.git
```
### 2. install dependencies
```bash
cd financial-health-dashboard
cd streamlit
pip install -r requirements.txt
```

### 3. running the app
```bash
streamlit run app.py
```
### Financial score calculation 
this gives the logic of the model that has been used
1. savings to income ratio, calculated if you save less than 20% of income, it lowers the score
2. monthly expenses as a percentage of income, if spending is more than 50% of income, it should lower the score
3. loan payments as percentage of income, if the loan payments are more than 30% of income, it lowers the score
4. credit card spending, if there is too much expenditure on credit card which is more than 30% of monthly expenses, it will lower the score
5. financial goals that are met will increase the score
