from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# reading in the first 5 columns of the data set
df = pd.read_csv('UK-HPI-full-file-2019-05.csv', usecols=[0, 1, 2, 3, 4])


@app.route("/", methods=["POST", "GET"])
def input_form():
    try:
        if request.method == "POST":
            # variables created and given the value that is entered into the "name" box
            borough_input = request.form["borough"]
            # print(borough_input)
            date_from_input = request.form["date_from"]
            # print(date_from_input)
            date_to_input = request.form["date_to"]
            # print(date_to_input)
            price_input = request.form["price"]
            # print(price_input)

            # filtering the df on the borough and creating a new df
            borough_df = df.query('RegionName == @borough_input')
            # print(borough_df)

            # splitting the from date input to get the month and the year to filter the borough df
            split_date_from_input = date_from_input.split('/', 1)[1]
            # print(split_date_from_input)

            # making a new df that contains the month and year for the borough
            from_date_df = borough_df[borough_df['Date'].str.contains(split_date_from_input)]
            # print("FROM DATE DF")
            # print(from_date_df)

            # splitting the to date input to get the month and the year to filter the borough df
            split_date_to_input = date_to_input.split('/', 1)[1]
            # print(split_date_to_input)

            # making a new df that contains the month and year for the borough
            to_date_df = borough_df[borough_df['Date'].str.contains(split_date_to_input)]
            # print("TO DATE DF")
            # print(to_date_df)

            # rounding the from date index to 2 decimal places
            from_date_index_value = round(from_date_df['Index'].values[0], 2)
            # print("from")
            # print(from_date_index_value)

            # rounding the to date index value to 2 decimal places
            to_date_index_value = round(to_date_df['Index'].values[0], 2)
            # print("To")
            # print(to_date_index_value)

            # dividing the to date index value by the from date and multiplying it by the input price
            calculation = round(int(price_input) * (to_date_index_value / from_date_index_value))
            # returning the calculation
            return jsonify(calculation)
            # print("Price given ", "£",calculation)
            return render_template("inputform.html")
    # catching if an incorrect input has been entered or if the information does not exist in the data set
    except (ValueError, KeyError, TypeError, IndexError):
        # redirecting to a different page to outline there is an error
        return render_template("incorrectentry.html")

    else:

        return render_template("inputform.html")


if __name__ == '__main__':
    app.run(debug=True)



