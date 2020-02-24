from flask import Flask, render_template, request, jsonify
import pandas as pd


app = Flask(__name__)

# reading in the first 5 columns of the data set
df = pd.read_csv(r'C:\Users\Holly Birch\PycharmProjects\Nested\UK-HPI-full-file-2019-05.csv', usecols=[0, 1, 2, 3, 4])
df['RegionName'] = df['RegionName'].str.lower()


@app.route("/", methods=["POST", "GET"])
def input_form():
    try:
        if request.method == "POST":
            # variables created and given the value that is entered into the "name" box
            borough_input = request.form["borough"]
            borough_input = borough_input.lower()
            date_from_input = request.form["date_from"]
            date_to_input = request.form["date_to"]
            price_input = request.form["price"]

            punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            # loop over the given string and if any punctuation replace with nothing
            for x in price_input.lower():
                if x in punctuation:
                    price_input = price_input.replace(x, "")

            # filtering the df on the borough and creating a new df
            borough_df = df.query('RegionName == @borough_input')

            print(borough_df)

            full_from_date_calculation = date_calculation(date_from_input)
            splitting_date_from = full_from_date_calculation.split('/', 1)[1]

            # making a new df that contains the month and year for the borough
            from_date_df = borough_df[borough_df['Date'].str.contains(splitting_date_from)]

            # splitting the to date input to get the month and the year to filter the borough df
            full_to_date_calculation = date_calculation(date_to_input)
            split_date_to_input = full_to_date_calculation.split('/', 1)[1]

            # making a new df that contains the month and year for the borough
            to_date_df = borough_df[borough_df['Date'].str.contains(split_date_to_input)]

            # rounding the from date index to 2 decimal places
            from_date_index_value = round(from_date_df['Index'].values[0], 2)

            # rounding the to date index value to 2 decimal places
            to_date_index_value = round(to_date_df['Index'].values[0], 2)

            return calculation(price_input, to_date_index_value, from_date_index_value)

    # catching if an incorrect input has been entered or if the information does not exist in the data set
    except (ValueError, KeyError, TypeError, IndexError):
        # redirecting to a different page to outline there is an error
        return render_template("incorrectentry.html")

    else:

        return render_template("inputform.html")


def calculation(price_input, to_date_index_value, from_date_index_value):
    # dividing the to date index value by the from date and multiplying it by the input price
    calculating = round(int(price_input) * (to_date_index_value / from_date_index_value))
    # returning the calculation

    return jsonify(calculating)
    # print("Price given ", "£",calculation)


def date_calculation(date_input):
    # splitting day month and year and making them int to deal with adding/subtracting will format date at end
    day = int(date_input.split('/', 1)[0])
    print(day)
    month = int(date_input.split('/', 2)[1])

    # calculating half of the days of the month returning n and rounding up
    if month == 2:
        n = 28/2
    else:
        n = 15
    print(n)

    if day >= n:
        end_date = pd.to_datetime(date_input) + pd.DateOffset(months=1) + pd.offsets.DateOffset(day=1)

        if month == 13:
            end_date = pd.to_datetime(date_input) + pd.DateOffset(year=1) & pd.to_datetime(date_input) + \
                       pd.DateOffset(months=-12)

    else:
        end_date = pd.to_datetime(date_input) + pd.DateOffset(day=0)

    return end_date.strftime("%d/%m/%Y")


if __name__ == '__main__':
    app.run(debug=True)

# makes the code not execute when the file is imported from another script.






