from flask import Flask, request, jsonify
from scoring import finance_score  #scoring model is in scoring.py

app = Flask(__name__)

@app.route('/calculate_score', methods=['POST']) #it will be like ""localhost:port/calculate_score"""
def calculate_score():
    try:
        data = request.get_json() #using json data as input

        family_data = {
            'income': data['income'],
            'savings': data['savings'],
            'monthly_expenses': data['monthly_expenses'],
            'loan_payments': data['loan_payments'],
        }       

        #function call
        score, insights = finance_score(family_data)

        #response
        response = {
            'financial_score': score,
            'insights': insights
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
