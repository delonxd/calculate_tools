import pandas as pd
import numpy as np

for temp in np.arange(1, 0.31, -0.1):

    valuation = 300
    fixed_assets = [450]
    save_month = 1.2
    investment_rate = 0.7
    loan_rate_year = 0.049 * 1.05
    return_rate_year = 0.15
    estate_rate_year = 0.01
    inflation_rate_year = 0.035
    income_rate_year = 0.03

    # rate = 0.5
    rate = temp
    loan = [fixed_assets[0]*(1-rate)]
    # loan = [400]
    # cash = [300]
    cash = [valuation-fixed_assets[0]+loan[0]]
    print('资金:', round(valuation, 2),
          '现金:', round(cash[0], 2),
          '固资:', round(fixed_assets[0], 2),
          '贷款:', round(loan[0], 2),
          '比率:', round(rate*100, 2), '%')
    # print(valuation, cash[0], loan[0])

    # income = [0.8]
    income = [save_month]
    # expense = [0.7]
    expense = [0]

    period_years = 30
    period_months = period_years * 12

    length = period_months

    payment = []
    inflation = [1]
    for i in range(period_months):
        loan_month = loan[-1]
        principal = loan[0] / period_months

        interest_rate_year = loan_rate_year
        interest_expense = loan_month * (interest_rate_year/12)
        loan.append(loan_month-principal)

        payment.append(interest_expense + principal)

        rate_year = estate_rate_year
        rslt = fixed_assets[-1] * (1 + rate_year/12)
        fixed_assets.append(rslt)

        rate_year = return_rate_year
        rslt = cash[-1] + income[-1] - expense[-1] - payment[-1] + cash[-1] * (rate_year/12) * investment_rate
        cash.append(rslt)

        rslt = inflation[-1] * (1 + inflation_rate_year/12)
        inflation.append(rslt)

        rslt = income[-1] * (1 + income_rate_year/12)
        income.append(rslt)

    print('资产:', round(cash[-1] + fixed_assets[-1], 2),
          '现金:', round(cash[-1], 2),
          '固资:', round(fixed_assets[-1], 2),
          '月存款:', round(income[-1], 2),
          '通货膨胀:', round(inflation[-1], 2),
          '资产折算后', round(((cash[-1] + fixed_assets[-1])/inflation[-1]), 2))

    print('')
    # print(fixed_assets[-1])

pass