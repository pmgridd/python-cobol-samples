from flask import Flask, request, jsonify

app = Flask(__name__)

# Helper function to get length before the first space, simulating COBOL's INSPECT
def get_length_before_space(input_string):
    if not input_string:
        return 0
    space_index = input_string.find(' ')
    if space_index == -1:
        return len(input_string) # No space found, take full length
    return space_index

@app.route('/format_name', methods=['POST'])
def format_name():
    data = request.get_json()

    given_name = data.get('given_name', '').strip()
    middle_name = data.get('middle_name', '').strip()
    family_name = data.get('family_name', '').strip()

    results = {}

    # Example 1: Formatting a person's name using MOVE statements (direct concatenation)
    # COBOL would move to fixed-length fields, then display those. Python uses dynamic strings.
    # Output will naturally handle spaces between names.
    example1_name = f"{given_name} {middle_name} {family_name}".strip()
    results["example_1_move_statements"] = example1_name

    # Example 2: Formatting a person's name using INSPECT and reference modification
    # Calculate lengths up to the first space, then concatenate.
    given_name_length = get_length_before_space(given_name)
    middle_name_length = get_length_before_space(middle_name)
    family_name_length = get_length_before_space(family_name)

    example2_name_parts = []
    if given_name_length > 0:
        example2_name_parts.append(given_name[:given_name_length])
    if middle_name_length > 0:
        example2_name_parts.append(middle_name[:middle_name_length])
    if family_name_length > 0:
        example2_name_parts.append(family_name[:family_name_length])
    
    example2_name = ' '.join(example2_name_parts)
    results["example_2_inspect_ref_mod"] = example2_name

    # Example 3: Formatting a person's name using STRING (delimited by space)
    # This is equivalent to stripping each part and joining with a single space.
    example3_name = ' '.join(filter(None, [given_name, middle_name, family_name]))
    results["example_3_string_delimited_by_space"] = example3_name

    # Example 4: Combining INSPECT, STRING, and reference modification
    # This is very similar to example 2, explicitly using the calculated lengths.
    example4_name_parts = []
    if given_name_length > 0:
        example4_name_parts.append(given_name[:given_name_length])
    if middle_name_length > 0:
        example4_name_parts.append(middle_name[:middle_name_length])
    if family_name_length > 0:
        example4_name_parts.append(family_name[:family_name_length])

    example4_name = ' '.join(example4_name_parts)
    # The COBOL example calculates WS-OUTPUT-LENGTH based on sum of lengths + 2 (for 2 spaces)
    # Python's join inherently handles the length correctly.
    results["example_4_combined_inspect_string_ref_mod"] = example4_name

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)