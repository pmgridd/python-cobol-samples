from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 88-level equivalent implementations ---

def is_simple_88_true(value):
    return value == 'T'

def is_simple_88_with_false_true(value):
    return value == 'T'

def is_category_a(code):
    return code in ['A', '3', '7']

def is_category_b(code):
    return code in ['B', '9', 'X']

def get_person_age_category(age):
    if 0 <= age <= 12:
        return 'child'
    elif 13 <= age <= 19:
        return 'teen'
    elif 20 <= age <= 35:
        return 'young-adult'
    elif 36 <= age <= 49:
        return 'adult'
    elif 50 <= age <= 59:
        return 'middle-aged'
    elif 60 <= age <= 74:
        return 'senior'
    elif 75 <= age <= 200:
        return 'elderly'
    else:
        return 'ageless' # Covers cases outside defined ranges or invalid input

# --- Flask API Endpoints ---

@app.route('/simple_88', methods=['POST'])
def simple_88_endpoint():
    data = request.get_json()
    value = data.get('value')

    if value is None:
        return jsonify({"error": "Please provide a 'value' (e.g., 'T' or 'F')."}), 400

    result = {
        "input_value": value,
        "is_simple_88_true": is_simple_88_true(value),
        "is_simple_88_with_false_true": is_simple_88_with_false_true(value)
    }
    return jsonify(result), 200

@app.route('/category_check', methods=['POST'])
def category_check_endpoint():
    data = request.get_json()
    category_code = data.get('code')

    if category_code is None:
        return jsonify({"error": "Please provide a 'code' (e.g., 'A', 'B', '3', 'X')."}), 400

    result = {
        "input_code": category_code,
        "is_category_a": is_category_a(category_code),
        "is_category_b": is_category_b(category_code),
        "evaluated_category": 'A' if is_category_a(category_code) else ('B' if is_category_b(category_code) else '?')
    }
    return jsonify(result), 200

@app.route('/age_category', methods=['POST'])
def age_category_endpoint():
    data = request.get_json()
    age = data.get('age')

    if age is None:
        return jsonify({"error": "Please provide an 'age' (integer)."}), 400

    try:
        age = int(age)
    except ValueError:
        return jsonify({"error": "Invalid age. Must be an integer."}), 400

    result = {
        "input_age": age,
        "age_category": get_person_age_category(age)
    }
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)