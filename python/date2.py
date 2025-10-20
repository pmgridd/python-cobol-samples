from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Helper function to get full month name
def get_month_name(month_number):
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return month_names[month_number - 1]

# Helper function to get day ordinal (st, nd, rd, th)
def get_day_ordinal(day):
    if 10 <= day % 100 <= 20:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

# Helper function to get full day name (COBOL's DAY-OF-WEEK is 1=Monday, 7=Sunday)
def get_day_name(day_of_week_number):
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return day_names[day_of_week_number - 1]

@app.route('/get_current_date_time', methods=['GET'])
def get_current_date_time():
    now = datetime.now()
    
    # Simulate COBOL's conceptual data items
    date_yy = now.strftime("%y")
    date_mm = now.strftime("%m")
    date_dd = now.strftime("%d")
    date_yyyy = now.strftime("%Y")
    day_ddd = now.strftime("%j") # Day of the year as a zero-padded decimal number.
    day_of_week = now.isoweekday() # Monday is 1, Sunday is 7

    time_hour = now.strftime("%H")
    time_minute = now.strftime("%M")
    time_second = now.strftime("%S")
    time_hundredths = str(now.microsecond // 10000).zfill(2) # First two digits of microseconds

    return jsonify({
        "DATE_VALUE": {
            "DATE_YY": date_yy,
            "DATE_MM": date_mm,
            "DATE_DD": date_dd
        },
        "DATE_YYYYMMDD_VALUE": {
            "DATE_YYYY": date_yyyy,
            "DATE_MM": int(date_mm),
            "DATE_DD": date_dd
        },
        "DAY_VALUE": {
            "DAY_YY": date_yy,
            "DAY_DDD": day_ddd
        },
        "DAY_YYYYDDD_VALUE": {
            "DAY_YYYY": date_yyyy,
            "DAY_DDD": day_ddd
        },
        "DAY_OF_WEEK_VALUE": day_of_week,
        "TIME_VALUE": {
            "TIME_HOUR": time_hour,
            "TIME_MINUTE": time_minute,
            "TIME_SECOND": time_second,
            "TIME_HUNDREDTHS": time_hundredths
        }
    }), 200

@app.route('/format_verbose_date', methods=['GET'])
def format_verbose_date_endpoint():
    now = datetime.now()
    
    day_name = get_day_name(now.isoweekday())
    day_of_month = now.day
    month_name = get_month_name(now.month)
    full_year = now.year
    
    verbose_date = (
        f"Today is {day_name}, the {day_of_month}{get_day_ordinal(day_of_month)} "
        f"of {month_name}, {full_year}"
    )
    return jsonify({"verbose_date": verbose_date}), 200

@app.route('/format_us_shorthand', methods=['GET'])
def format_us_shorthand_endpoint():
    now = datetime.now()
    us_shorthand = now.strftime("%m/%d/%y")
    return jsonify({"us_shorthand": us_shorthand}), 200

@app.route('/format_euro_shorthand', methods=['GET'])
def format_euro_shorthand_endpoint():
    now = datetime.now()
    euro_shorthand = now.strftime("%d.%m.%y")
    return jsonify({"euro_shorthand": euro_shorthand}), 200

@app.route('/format_time_hundredths', methods=['GET'])
def format_time_hundredths_endpoint():
    now = datetime.now()
    time_hundredths = str(now.microsecond // 10000).zfill(2)
    formatted_time = now.strftime(f"%H:%M:%S.{time_hundredths}")
    return jsonify({"formatted_time_hundredths": formatted_time}), 200

if __name__ == '__main__':
    app.run(debug=True)
