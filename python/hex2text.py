from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hex_to_text', methods=['POST'])
def hex_to_text_endpoint():
    data = request.get_json()
    
    if not data or 'original_value' not in data:
        return jsonify({"error": "Invalid input. Please provide 'original_value' in the request body."}), 400

    original_value = data['original_value']

    if not isinstance(original_value, str):
        return jsonify({"error": "'original_value' must be a string."}), 400

    hex_result = ""
    for char in original_value:
        # Get the ASCII/Unicode value of the character
        char_val = ord(char)
        # Convert to hexadecimal, remove '0x' prefix, and pad with leading zero if necessary
        hex_char = format(char_val, '02x')
        hex_result += hex_char
    
    return jsonify({"hex_result": hex_result.upper()}), 200 # COBOL example uses uppercase hex

if __name__ == '__main__':
    app.run(debug=True)
