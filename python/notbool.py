from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Helper functions for COBOL-like boolean simulations ---

# Example 2: PIC X where 'T' = true and SPACE = false
def ex2_is_true(flag_value):
    return flag_value == 'T'

def ex2_toggle_flag(flag_value):
    return ' ' if flag_value == 'T' else 'T'

# Example 3: PIC X where 'Y' = yes and 'N' = no
def ex3_is_yes(flag_value):
    return flag_value == 'Y'

def ex3_toggle_flag(flag_value):
    return 'N' if flag_value == 'Y' else 'Y'

# Example 4: PIC X where '1' = true and '0' = false
def ex4_is_true(flag_value):
    return flag_value == '1'

def ex4_toggle_flag(flag_value):
    return '0' if flag_value == '1' else '1'

# Example 5: Pseudo-boolean using 88-level items without FALSE clause
# Here, the field itself determines the boolean state (e.g., 'T' for true, others for false)
def ex5_is_flag_set(field_value):
    return field_value == 'T'

def ex5_toggle_flag(field_value):
    # If set ('T'), move space; else, set to 'T'
    return ' ' if field_value == 'T' else 'T'

# Example 6: Pseudo-boolean using 88-level items with FALSE clause
# Here, 'T' is true, 'F' is false.
def ex6_is_flag_set(field_value):
    return field_value == 'T'

def ex6_toggle_flag(field_value):
    # If true ('T'), set to false ('F'); else, set to true ('T')
    return 'F' if field_value == 'T' else 'T'

# Example 7: Pseudo-boolean using numeric values (COMP-3)
# Here, 1 is true, -1 is false.
def ex7_is_true(flag_value):
    return flag_value == 1

def ex7_toggle_flag(flag_value):
    # COBOL: COMPUTE EX7-FLAG = EX7-FLAG * -EX7-FLAG
    # This toggles 1 to -1, and -1 to 1. (1 * -1 = -1, -1 * -(-1) = -1 * 1 = -1)
    # The original COBOL toggle logic:
    # IF EX7-FLAG EQUAL EX7-TRUE THEN
    #    MOVE EX7-FALSE TO EX7-FLAG
    # ELSE
    #    MOVE EX7-TRUE TO EX7-FLAG
    # END-IF
    # Given the COBOL comment `COMPUTE EX7-FLAG = EX7-FLAG * -EX7-FLAG` might be misleading
    # if -EX7-FLAG is interpreted as its numeric negative. Let's follow the clear IF/ELSE logic.
    return -1 if flag_value == 1 else 1

# --- Flask API Endpoints ---

@app.route('/ex2_boolean_logic', methods=['POST'])
def ex2_boolean_logic():
    data = request.get_json()
    flag = data.get('flag')

    if flag not in ['T', ' ']:
        return jsonify({"error": "Invalid flag for EX2. Expected 'T' or ' '."}), 400

    result = "true" if ex2_is_true(flag) else "false"
    toggled_flag = ex2_toggle_flag(flag)

    return jsonify({
        "input_flag": flag,
        "is_true": result,
        "toggled_flag": toggled_flag
    }), 200

@app.route('/ex3_boolean_logic', methods=['POST'])
def ex3_boolean_logic():
    data = request.get_json()
    flag = data.get('flag')

    if flag not in ['Y', 'N']:
        return jsonify({"error": "Invalid flag for EX3. Expected 'Y' or 'N'."}), 400

    result = "yes" if ex3_is_yes(flag) else "no"
    toggled_flag = ex3_toggle_flag(flag)

    return jsonify({
        "input_flag": flag,
        "is_yes": result,
        "toggled_flag": toggled_flag
    }), 200

@app.route('/ex4_boolean_logic', methods=['POST'])
def ex4_boolean_logic():
    data = request.get_json()
    flag = data.get('flag')

    if flag not in ['1', '0']:
        return jsonify({"error": "Invalid flag for EX4. Expected '1' or '0'."}), 400

    result = ""
    if ex4_is_true(flag):
        result = "true"
    elif flag == '0': # Explicitly check for '0' as false
        result = "false"
    else:
        result = "not set" # This case should ideally not be hit with '1' or '0' input

    toggled_flag = ex4_toggle_flag(flag)

    return jsonify({
        "input_flag": flag,
        "evaluation": result,
        "toggled_flag": toggled_flag
    }), 200

@app.route('/ex5_88_level_logic', methods=['POST'])
def ex5_88_level_logic():
    data = request.get_json()
    field_value = data.get('field')

    if field_value is None or not isinstance(field_value, str) or len(field_value) != 1:
        return jsonify({"error": "Invalid field for EX5. Expected a single character string (e.g., 'T', ' ')."}), 400

    is_set = ex5_is_flag_set(field_value)
    toggled_field = ex5_toggle_flag(field_value)

    return jsonify({
        "input_field": field_value,
        "is_flag_set": is_set,
        "toggled_field": toggled_field
    }), 200

@app.route('/ex6_88_level_logic', methods=['POST'])
def ex6_88_level_logic():
    data = request.get_json()
    field_value = data.get('field')

    if field_value not in ['T', 'F']:
        return jsonify({"error": "Invalid field for EX6. Expected 'T' or 'F'."}), 400

    is_set = ex6_is_flag_set(field_value)
    toggled_field = ex6_toggle_flag(field_value)

    return jsonify({
        "input_field": field_value,
        "is_flag_set": is_set,
        "toggled_field": toggled_field
    }), 200

@app.route('/ex7_numeric_boolean_logic', methods=['POST'])
def ex7_numeric_boolean_logic():
    data = request.get_json()
    flag = data.get('flag')

    if not isinstance(flag, (int, float)):
        return jsonify({"error": "Invalid flag for EX7. Expected a number (1 or -1)."}), 400

    # Ensure it's explicitly 1 or -1 as per COBOL example
    if flag not in [1, -1]:
        return jsonify({"error": "Invalid flag for EX7. Expected 1 (true) or -1 (false)."}), 400

    is_true = ex7_is_true(flag)
    toggled_flag = ex7_toggle_flag(flag)

    return jsonify({
        "input_flag": flag,
        "is_true": is_true,
        "toggled_flag": toggled_flag
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
