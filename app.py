from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def finance():

    report = None

    if request.method == "POST":

        income = float(request.form["income"])
        rent = float(request.form["rent"])
        grocery = float(request.form["grocery"])
        desires = float(request.form["desires"])
        edu = float(request.form["edu"])

        # SUGGESTED AMOUNTS

        suggested_rent = (25 / 100) * income
        suggested_grocery = (10 / 100) * income
        suggested_desires = (5 / 100) * income
        suggested_education = (10 / 100) * income

        # TOTAL EXPENSE

        total_expense = rent + grocery + desires + edu

        # SAVINGS

        net_savings = income - total_expense

        # EXPECTED EXPENSE

        expected_expense = (
            suggested_rent
            + suggested_grocery
            + suggested_desires
            + suggested_education
        )

        # EXPECTED SAVINGS

        expected_savings = income - expected_expense

        # EMERGENCY FUND

        emergency_fund = (47 / 100) * net_savings

        # PERCENTAGES

        if income != 0:
            p_savings = (net_savings / income) * 100
            p_expense = (total_expense / income) * 100
        else:
            p_savings = 0
            p_expense = 0

        # RENT ANALYSIS

        if suggested_rent == rent:
            rent_message = "Your essentials cost matches the suggested amount."

        elif suggested_rent < rent:
            rent_message = (
                "Your essential cost exceeds the suggested amount by Rs. "
                + str(round(rent - suggested_rent, 2))
            )

        else:
            rent_message = (
                "You are spending less on essentials than the suggested amount by Rs. "
                + str(round(suggested_rent - rent, 2))
            )

        # GROCERY ANALYSIS

        if suggested_grocery == grocery:
            grocery_message = "Your grocery spending matches the suggested amount."

        elif suggested_grocery < grocery:
            grocery_message = (
                "Your grocery cost exceeds the suggested amount by Rs. "
                + str(round(grocery - suggested_grocery, 2))
            )

        else:
            grocery_message = (
                "You are spending less on groceries than the suggested amount by Rs. "
                + str(round(suggested_grocery - grocery, 2))
            )

        # DESIRES ANALYSIS

        if suggested_desires == desires:
            desires_message = "Your desire spending matches the suggested amount."

        elif suggested_desires < desires:
            desires_message = (
                "ALERT! You are spending more on desires than prescribed by Rs. "
                + str(round(desires - suggested_desires, 2))
            )

        else:
            desires_message = (
                "You are spending less on desires than prescribed by Rs. "
                + str(round(suggested_desires - desires, 2))
            )

        # EDUCATION ANALYSIS

        if suggested_education == edu:
            education_message = "Your education spending matches the suggested amount."

        elif suggested_education > edu:
            education_message = (
                "You spend less on education than prescribed by Rs. "
                + str(round(suggested_education - edu, 2))
            )

        else:
            education_message = (
                "You spend more on education than prescribed by Rs. "
                + str(round(edu - suggested_education, 2))
            )

        # FINANCIAL ADVICE

        advice = []

        if p_expense > 60:

            advice.append(
                "ALERT! You are crossing the boundary of expenses. "
                "Consider reducing unnecessary spending."
            )

            advice.append(
                "Wait 48 hours before buying something under desires "
                "to check whether it is a true need or an urge."
            )

            advice.append(
                "Keep an emergency fund for serious emergencies."
            )

            advice.append(
                "Track leakage expenses."
            )

            advice.append(
                "Review utility bills and subscriptions."
            )

            advice.append(
                "Your maximum expenditure is Rs. "
                + str(round(max(rent, grocery, desires, edu), 2))
            )

        elif 70 < p_savings < 90:

            advice.append(
                "Excellent job! Your savings percentage is very strong."
            )

            advice.append(
                "Learn about long-term investing and financial planning."
            )

            advice.append(
                "Try to maintain a balanced budget."
            )

            advice.append(
                "Build an emergency cushion."
            )

            advice.append(
                "Invest in high-value skills."
            )

        elif p_savings > 90:

            advice.append(
                "Outstanding savings performance!"
            )

            advice.append(
                "Your savings percentage is exceptionally high."
            )

        else:

            advice.append(
                "Continue monitoring your expenses and savings every month."
            )

        # HIGH INCOME MESSAGE

        income_message = ""

        if income > 10000000:

            income_message = (
                "Your income is extremely high. "
                "Remember that understanding when to exit an investment "
                "can be just as important as knowing when to enter."
            )

        # SAVE HISTORY

        with open("finance_history.csv", "a", newline="") as file:

            writer = csv.writer(file)

            if file.tell() == 0:

                writer.writerow([
                    "Date",
                    "Income",
                    "Rent/Essentials",
                    "Groceries",
                    "Desires",
                    "Education",
                    "Total Expense",
                    "Savings",
                    "Savings %",
                    "Expense %"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                income,
                rent,
                grocery,
                desires,
                edu,
                total_expense,
                net_savings,
                p_savings,
                p_expense
            ])

        # SEND DATA TO HTML

        report = {
            "income": income,
            "rent": rent,
            "grocery": grocery,
            "desires": desires,
            "edu": edu,

            "suggested_rent": suggested_rent,
            "suggested_grocery": suggested_grocery,
            "suggested_desires": suggested_desires,
            "suggested_education": suggested_education,

            "total_expense": total_expense,
            "net_savings": net_savings,
            "expected_expense": expected_expense,
            "expected_savings": expected_savings,

            "emergency_fund": emergency_fund,

            "p_savings": p_savings,
            "p_expense": p_expense,

            "rent_message": rent_message,
            "grocery_message": grocery_message,
            "desires_message": desires_message,
            "education_message": education_message,

            "advice": advice,
            "income_message": income_message
        }

    return render_template("index.html", report=report)


if __name__ == "__main__":
    app.run(debug=True)