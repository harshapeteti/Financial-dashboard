def finance_score(data):
    savings_to_income_ratio = data['savings'] / data['income']
    expenses_to_income_ratio = data['monthly_expenses'] / data['income']
    loan_payments_ratio = data['loan_payments'] / data['income']

    score = 100  # beginning score
    if savings_to_income_ratio < 0.2:
        score -= 20  # deducing the points if savings are low
    if expenses_to_income_ratio > 0.5:
        score -= 15  # deducing points if monthly expenses are too high
    if loan_payments_ratio > 0.3:
        score -= 10  # deducing points if loan payments are too high

    insights = []
    if savings_to_income_ratio < 0.2:
        insights.append("Savings are below recommended levels.")
    if expenses_to_income_ratio > 0.5:
        insights.append("Expenses are above recommended levels.")
    if loan_payments_ratio > 0.3:
        insights.append("Loan payments are too high relative to income.")

    return score, insights
