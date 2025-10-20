from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Helper function to get month abbreviation for NCSA format
def get_month_abbr(month_number):
    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    return month_names[month_number - 1]

# Helper function to get day ordinal (st, nd, rd, th)
def get_day_ordinal(day):
    if 10 <= day % 100 <= 20:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

@app.route('/current_datetime', methods=['GET'])
def current_datetime_endpoint():
    now = datetime.now()
    return jsonify({
        "full_year": now.year,
        "century": now.year // 100,
        "year_2_digit": now.year % 100,
        "month": now.month,
        "day_of_month": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "milliseconds": now.microsecond // 1000, # Convert microseconds to milliseconds
        "timezone_direction": "+", # Simplified, COBOL gets from system
        "timezone_offset_hours": 0, # Simplified
        "timezone_offset_minutes": 0  # Simplified
    }), 200

@app.route('/format_ncsa', methods=['GET'])
def format_ncsa_endpoint():
    now = datetime.now()
    # Example: [20/Oct/2025:14:07:52 +0000]
    timezone_str = now.astimezone().strftime('%z')
    ncsa_timestamp = now.strftime(f"[%d/{get_month_abbr(now.month)}/%Y:%H:%M:%S {timezone_str}]")
    return jsonify({"ncsa_timestamp": ncsa_timestamp}), 200

@app.route('/format_verbose', methods=['GET'])
def format_verbose_endpoint():
    now = datetime.now()
    # Example: "October 20th, 2025"
    verbose_date = now.strftime(f"%B %d{get_day_ordinal(now.day)}, %Y")
    return jsonify({"verbose_date": verbose_date}), 200

@app.route('/format_us_shorthand', methods=['GET'])
def format_us_shorthand_endpoint():
    now = datetime.now()
    # Example: "10/20/25"
    us_shorthand = now.strftime("%m/%d/%y")
    return jsonify({"us_shorthand": us_shorthand}), 200

@app.route('/format_euro_shorthand', methods=['GET'])
def format_euro_shorthand_endpoint():
    now = datetime.now()
    # Example: "20.10.25"
    euro_shorthand = now.strftime("%d.%m.%y")
    return jsonify({"euro_shorthand": euro_shorthand}), 200

if __name__ == '__main__':
    app.run(debug=True)