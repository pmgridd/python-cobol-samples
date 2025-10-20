from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/compare_alphanumeric', methods=['POST'])
def compare_alphanumeric():
    data = request.get_json()
    alpha1 = data.get('alpha1')
    alpha2 = data.get('alpha2')

    if alpha1 is None or alpha2 is None:
        return jsonify({"error": "Please provide 'alpha1' and 'alpha2' values."}), 400

    result = ""
    if alpha1 == alpha2:
        result = "equal"
    else:
        result = "different"
    
    return jsonify({"result_of_compare": result}), 200

@app.route('/compare_with_literal', methods=['POST'])
def compare_with_literal():
    data = request.get_json()
    alpha1 = data.get('alpha1')

    if alpha1 is None:
        return jsonify({"error": "Please provide an 'alpha1' value."}), 400

    result = ""
    if alpha1 == 'foobar':
        result = "equal"
    else:
        result = "different"
    
    return jsonify({"result_of_compare": result}), 200

@app.route('/validate_numeric', methods=['POST'])
def validate_numeric():
    data = request.get_json()
    numeric_val = data.get('numeric_val')

    if numeric_val is None:
        return jsonify({"error": "Please provide a 'numeric_val'."}), 400

    try:
        # Attempt to convert to float (or int if preferred)
        num = float(numeric_val)
        # Simulate ADD 1 TO NUMERIC-2
        num += 1
        message = f"Value is numeric. Incremented to {num}"
    except ValueError:
        # Simulate MOVE 1 TO NUMERIC-2
        num = 1
        message = f"Value is not numeric. Set to {num}"
    
    return jsonify({"processed_value": num, "message": message}), 200

@app.route('/numeric_division_check', methods=['POST'])
def numeric_division_check():
    data = request.get_json()
    numeric1 = data.get('numeric1')
    numeric2 = data.get('numeric2')

    if numeric1 is None or numeric2 is None:
        return jsonify({"error": "Please provide 'numeric1' and 'numeric2' values."}), 400

    try:
        numeric1 = float(numeric1)
        numeric2 = float(numeric2)
    except ValueError:
        return jsonify({"error": "'numeric1' and 'numeric2' must be numbers."}), 400

    if numeric1 > 0:
        if numeric1 == 0:
            # This case would be handled by the outer if, but added for clarity
            return jsonify({"error": "Division by zero averted. numeric1 is zero."}), 400
        numeric2 = numeric2 / numeric1
        message = f"numeric1 is greater than zero. numeric2 divided by numeric1: {numeric2}"
    else:
        numeric2 = numeric2 - 1
        message = f"numeric1 is not greater than zero. numeric2 decremented by 1: {numeric2}"
    
    return jsonify({"processed_numeric2": numeric2, "message": message}), 200

@app.route('/compare_two_numerics', methods=['POST'])
def compare_two_numerics():
    data = request.get_json()
    numeric1 = data.get('numeric1')
    numeric2 = data.get('numeric2')

    if numeric1 is None or numeric2 is None:
        return jsonify({"error": "Please provide 'numeric1' and 'numeric2' values."}), 400

    try:
        numeric1 = float(numeric1)
        numeric2 = float(numeric2)
    except ValueError:
        return jsonify({"error": "'numeric1' and 'numeric2' must be numbers."}), 400

    result = ""
    if numeric1 > numeric2:
        result = "numeric-1"
    else:
        result = "numeric-2"
    
    return jsonify({"result_of_compare": result}), 200

@app.route('/evaluate_numerics', methods=['POST'])
def evaluate_numerics():
    data = request.get_json()
    numeric1 = data.get('numeric1')
    numeric2 = data.get('numeric2')

    if numeric1 is None or numeric2 is None:
        return jsonify({"error": "Please provide 'numeric1' and 'numeric2' values."}), 400

    try:
        numeric1 = float(numeric1)
        numeric2 = float(numeric2)
    except ValueError:
        return jsonify({"error": "'numeric1' and 'numeric2' must be numbers."}), 400

    result = ""
    if numeric1 > numeric2:
        result = "numeric-1"
    elif numeric1 < numeric2:
        result = "numeric-2"
    else:
        result = "equal"
    
    return jsonify({"result_of_compare": result}), 200

@app.route('/evaluate_multiple_conditions', methods=['POST'])
def evaluate_multiple_conditions():
    data = request.get_json()
    numeric1 = data.get('numeric1')
    numeric2 = data.get('numeric2')
    alpha1 = data.get('alpha1')
    alpha2 = data.get('alpha2')

    if any(val is None for val in [numeric1, numeric2, alpha1, alpha2]):
        return jsonify({"error": "Please provide 'numeric1', 'numeric2', 'alpha1', and 'alpha2' values."}), 400

    try:
        numeric1 = float(numeric1)
        numeric2 = float(numeric2)
    except ValueError:
        return jsonify({"error": "'numeric1' and 'numeric2' must be numbers."}), 400

    result = "undefined"

    if numeric1 > numeric2 and alpha1[0:3] == 'THX':
        result = "THX and numeric-1"
    elif numeric1 < numeric2 and alpha1[0:3] == 'THX':
        result = "THX and numeric-2"
    elif numeric1 == numeric1 and alpha2 == 'Terminator': # numeric1 == numeric1 is always true
        result = "Terminator and equal numbers"
    
    return jsonify({"result_of_compare": result}), 200

if __name__ == '__main__':
    app.run(debug=True)