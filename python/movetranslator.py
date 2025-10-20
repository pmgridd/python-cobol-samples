from flask import Flask, request, jsonify
import struct # For simulating binary data representation for hex conversion

app = Flask(__name__)

# Helper to convert a string to its ASCII hexadecimal representation
def string_to_ascii_hex(input_string):
    return ''.join([f'{ord(char):02x}' for char in input_string]).upper()

# Helper to convert a float to its IEEE 754 single-precision hex representation
# This is a simplification, COBOL's COMP-1 might be different on some systems.
def float_to_comp1_hex(f_value):
    try:
        # Pack float as single-precision (4 bytes)
        packed = struct.pack('!f', f_value) # ! for network (big-endian), f for float
        return packed.hex().upper()
    except OverflowError:
        return "OVERFLOW"
    except Exception as e:
        return f"ERROR: {e}"

# Helper to convert a float to its IEEE 754 double-precision hex representation
# This is a simplification, COBOL's COMP-2 might be different on some systems.
def float_to_comp2_hex(f_value):
    try:
        # Pack float as double-precision (8 bytes)
        packed = struct.pack('!d', f_value) # ! for network (big-endian), d for double
        return packed.hex().upper()
    except OverflowError:
        return "OVERFLOW"
    except Exception as e:
        return f"ERROR: {e}"

# Helper to simulate COBOL PIC S9(04)V9(03) COMP-3 (packed decimal) to hex
# This is a highly simplified representation and does not fully emulate COMP-3.
# It converts the string representation of the number to hex.
def packed_decimal_to_simplified_hex(decimal_value, total_digits=7, decimal_places=3):
    # For a true COMP-3, we'd need to convert to BCD. For this demo,
    # we'll represent the string of the number as hex.
    # COBOL S9(04)V9(03) means 4 integer digits, 3 decimal digits, total 7 digits + sign.
    # Typically 4 bytes (7 digits + sign nibble = 8 nibbles = 4 bytes)
    # E.g., -256.095 -> 02 56 09 5D (if negative)
    # This is a very rough simulation.
    try:
        # Format to ensure proper decimal places
        s_value = f'{decimal_value:0{total_digits-decimal_places+1}.{decimal_places}f}'.replace('.', '')
        # Handle sign for display purposes (not true COMP-3 encoding)
        if decimal_value < 0:
            s_value = s_value.replace('-', '') + 'D' # D for negative
        else:
            s_value = s_value + 'C' # C for positive
        
        # Convert each character (digit + sign nibble) to its hex representation
        return string_to_ascii_hex(s_value) # This is a placeholder, not true COMP-3 hex
    except Exception as e:
        return f"ERROR: {e}"


# Example 1: Alphanumeric MOVE
@app.route('/move_alphanumeric', methods=['POST'])
def move_alphanumeric():
    data = request.get_json()
    input_string = data.get('input_string', 'Repent, Harlequin!')
    
    ws_original_value = input_string
    ws_original_length = len(ws_original_value)
    hex_value = string_to_ascii_hex(ws_original_value)

    return jsonify({
        "example": "Alphanumeric MOVE",
        "moved_value": ws_original_value,
        "length": ws_original_length,
        "hex_value": hex_value
    }), 200

# Example 2: 32-bit binary value (PIC S9(09) COMP)
@app.route('/move_binary_32bit', methods=['POST'])
def move_binary_32bit():
    data = request.get_json()
    input_value = data.get('input_value', 375502) # Default as per COBOL
    
    try:
        ws_binary_item_4 = int(input_value)
        # To get a hex representation of the *binary data* (4 bytes for S9(9) COMP)
        # This is a simplification: Python's int.to_bytes() for hex representation
        hex_value = ws_binary_item_4.to_bytes(4, byteorder='big', signed=True).hex().upper()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input for 32-bit binary, expected integer."}), 400
    
    return jsonify({
        "example": "32-bit Binary MOVE",
        "moved_value": ws_binary_item_4,
        "hex_value_binary_repr": hex_value # Hex representation of the binary data
    }), 200

# Example 3: 64-bit binary value (PIC S9(16) COMP)
@app.route('/move_binary_64bit', methods=['POST'])
def move_binary_64bit():
    data = request.get_json()
    input_value = data.get('input_value', -281064762375502) # Default as per COBOL

    try:
        ws_binary_item_8 = int(input_value)
        # To get a hex representation of the *binary data* (8 bytes for S9(16) COMP)
        hex_value = ws_binary_item_8.to_bytes(8, byteorder='big', signed=True).hex().upper()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input for 64-bit binary, expected integer."}), 400

    return jsonify({
        "example": "64-bit Binary MOVE",
        "moved_value": ws_binary_item_8,
        "hex_value_binary_repr": hex_value # Hex representation of the binary data
    }), 200

# Example 4: 32-bit binary value - overwrite with spaces
@app.route('/move_binary_32bit_spaces', methods=['POST'])
def move_binary_32bit_spaces():
    # In COBOL, moving spaces to a COMP field might result in unpredictable binary data,
    # or zero if the compiler handles implicit numeric conversion.
    # Here, we'll show what '4 spaces' look like in hex ASCII.
    ws_binary_item_4_as_text = '    ' # 4 spaces for a 4-byte COMP item
    hex_value = string_to_ascii_hex(ws_binary_item_4_as_text)
    
    return jsonify({
        "example": "32-bit Binary (spaces overwrite)",
        "moved_value_as_text": ws_binary_item_4_as_text,
        "hex_value_ascii_of_spaces": hex_value
    }), 200

# Example 5: Single-precision floating-point value (COMP-1)
@app.route('/move_float_single_precision', methods=['POST'])
def move_float_single_precision():
    data = request.get_json()
    input_value = data.get('input_value', 0.0623e-24) # Default as per COBOL
    
    try:
        ws_single_precision = float(input_value)
        hex_value = float_to_comp1_hex(ws_single_precision)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input for single-precision float, expected number."}), 400

    return jsonify({
        "example": "Single-precision Float MOVE",
        "moved_value": ws_single_precision,
        "hex_value_ieee754_repr": hex_value
    }), 200

# Example 6: Double-precision floating-point value (COMP-2)
@app.route('/move_float_double_precision', methods=['POST'])
def move_float_double_precision():
    data = request.get_json()
    input_value = data.get('input_value', 3246.16e-32) # Default as per COBOL

    try:
        ws_double_precision = float(input_value)
        hex_value = float_to_comp2_hex(ws_double_precision)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input for double-precision float, expected number."}), 400

    return jsonify({
        "example": "Double-precision Float MOVE",
        "moved_value": ws_double_precision,
        "hex_value_ieee754_repr": hex_value
    }), 200

# Example 7: Packed Decimal value (PIC S9(04)V9(03) COMP-3)
@app.route('/move_packed_decimal', methods=['POST'])
def move_packed_decimal():
    data = request.get_json()
    input_value = data.get('input_value', -256.095) # Default as per COBOL

    try:
        ws_packed_decimal_item = float(input_value)
        # Simplified hex representation (not true COMP-3 encoding)
        hex_value = packed_decimal_to_simplified_hex(ws_packed_decimal_item)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input for packed decimal, expected number."}), 400

    return jsonify({
        "example": "Packed Decimal MOVE",
        "moved_value": ws_packed_decimal_item,
        "hex_value_simplified_repr": hex_value
    }), 200

# Example 8: Packed Decimal value - overwrite value with spaces
@app.route('/move_packed_decimal_spaces', methods=['POST'])
def move_packed_decimal_spaces():
    # COBOL PIC S9(04)V9(03) COMP-3 is 4 bytes.
    # Moving spaces to it might zero it out or cause issues.
    # Here, we show 4 spaces in hex ASCII.
    ws_packed_decimal_item_as_text = '    ' # 4 spaces for 4 bytes
    hex_value = string_to_ascii_hex(ws_packed_decimal_item_as_text)

    return jsonify({
        "example": "Packed Decimal (spaces overwrite)",
        "moved_value_as_text": ws_packed_decimal_item_as_text,
        "hex_value_ascii_of_spaces": hex_value
    }), 200

# Example 9: Display Numeric Signed (PIC S9(05)V9(02))
@app.route('/move_display_numeric_signed', methods=['POST'])
def move_display_numeric_signed():
    data = request.get_json()
    input_value = data.get('input_value', -4832.61) # Default as per COBOL

    try:
        ws_display_numeric_signed = float(input_value)
        # COBOL PIC S9(05)V9(02) would display something like -483261
        # or -4832.61 if edited. Assuming standard decimal display.
        # Python format specifier for 5 integer digits, 2 decimal digits, with sign
        # Adjusting width to mimic COBOL PICTURE clause might be tricky without
        # knowing exact implicit behavior. Using :.2f for 2 decimal places.
        result_str = f'{ws_display_numeric_signed:08.2f}' # Example: -04832.61
        if ws_display_numeric_signed >= 0:
            result_str = '+' + result_str # Explicit positive sign if COBOL would show it

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input for display numeric signed, expected number."}), 400

    return jsonify({
        "example": "Display Numeric Signed",
        "moved_value": ws_display_numeric_signed,
        "formatted_result": result_str
    }), 200

# Example 10: Display Numeric with formatting (PIC -ZZ,ZZ9.99)
@app.route('/move_display_numeric_formatted', methods=['POST'])
def move_display_numeric_formatted():
    data = request.get_json()
    input_value = data.get('input_value', -4832.61) # Default as per COBOL

    try:
        ws_display_numeric_formatted = float(input_value)
        # Python f-string for comma separator and 2 decimal places
        # COBOL PICTURE -ZZ,ZZ9.99 suppresses leading zeros, adds comma, 2 decimal places, shows negative sign
        formatted_value = f'{ws_display_numeric_formatted:,.2f}'
        # Handle the leading zero suppression if input value is between -1 and 1 (e.g., -0.50 -> -.50)
        # For positive values 0.50 -> .50
        if formatted_value.startswith('0.'):
            formatted_value = '.' + formatted_value[2:]
        elif formatted_value.startswith('-0.'):
            formatted_value = '-.' + formatted_value[3:]

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input for display numeric formatted, expected number."}), 400

    return jsonify({
        "example": "Display Numeric Formatted",
        "moved_value": ws_display_numeric_formatted,
        "formatted_result": formatted_value
    }), 200

# Example 11: Display Numeric with formatting for currency (PIC -$$,$$9.99)
@app.route('/move_display_currency_value', methods=['POST'])
def move_display_currency_value():
    data = request.get_json()
    input_value = data.get('input_value', -4832.61) # Default as per COBOL

    try:
        ws_display_currency_value = float(input_value)
        # Python f-string for currency formatting
        # COBOL PICTURE -$$,$$9.99 shows '$' sign, comma, 2 decimal places, and negative sign
        formatted_value = f'${ws_display_currency_value:,.2f}'
        # If negative, move sign before dollar sign to match COBOL display
        if ws_display_currency_value < 0 and not formatted_value.startswith('-$'):
            formatted_value = '-' + formatted_value.replace('-', '')
        elif ws_display_currency_value >= 0 and formatted_value.startswith('-$'): # Remove potential extra negative sign if somehow there
             formatted_value = formatted_value.replace('-', '')

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input for display currency value, expected number."}), 400

    return jsonify({
        "example": "Display Currency Value Formatted",
        "moved_value": ws_display_currency_value,
        "formatted_result": formatted_value
    }), 200

# Example 13: Using INITIALIZE to initialize a group item
@app.route('/initialize_group_item', methods=['POST'])
def initialize_group_item():
    # Simulate the structure of WS-GROUP-ITEM
    # 05  WS-ALPHA-FIELD-1       PIC X(05).
    # 05  WS-PACKED-FIELD-2      PIC S9(05) COMP-3. (3 bytes for 5 digits + sign)
    # 05  WS-BOOLEAN-FIELD-3     PIC X.
    # 05  WS-TABLE-4             VALUE 'ABCD'. (effectively PIC X(04))
    #    10  WS-TABLE-ENTRY OCCURS 1 TO 4 DEPENDING ON WS-TABLE-SIZE PIC X.

    # Initializing a group item: alphanumeric by spaces, numeric by zeroes
    ws_group_item = {
        'alpha_field_1': '     ',
        'packed_field_2': 0, # Numeric zero
        'boolean_field_3': ' ',
        'table_4': '    ', # Alphanumeric by spaces
        'table_size': 0 # Numeric zero
    }
    
    # To get a 'hex value' of the group item, we concatenate string representations
    # This is not a direct memory dump, but a logical representation.
    concatenated_str = (
        ws_group_item['alpha_field_1'] +
        str(ws_group_item['packed_field_2']) +
        ws_group_item['boolean_field_3'] +
        ws_group_item['table_4'] +
        str(ws_group_item['table_size'])
    )
    hex_value = string_to_ascii_hex(concatenated_str)

    return jsonify({
        "example": "INITIALIZE Group Item",
        "initialized_group_item": ws_group_item,
        "concatenated_string_for_hex": concatenated_str,
        "hex_value_ascii_of_concatenated_string": hex_value
    }), 200

# Example 14: Using MOVE SPACES to initialize a group item
@app.route('/move_spaces_to_group_item', methods=['POST'])
def move_spaces_to_group_item():
    # MOVE SPACES to a group item sets all its characters to spaces.
    # Numeric fields would conceptually become zero, but memory-wise they'd be spaces.
    ws_group_item_spaces = {
        'alpha_field_1': '     ',
        'packed_field_2': '   ', # 3 spaces for 3 bytes of COMP-3
        'boolean_field_3': ' ',
        'table_4': '    ',
        'table_size': '  ' # 2 spaces for 2 bytes of S9(3) COMP-3
    }

    concatenated_str = (
        ws_group_item_spaces['alpha_field_1'] +
        ws_group_item_spaces['packed_field_2'] +
        ws_group_item_spaces['boolean_field_3'] +
        ws_group_item_spaces['table_4'] +
        ws_group_item_spaces['table_size']
    )
    hex_value = string_to_ascii_hex(concatenated_str)

    return jsonify({
        "example": "MOVE SPACES to Group Item",
        "initialized_group_item_with_spaces": ws_group_item_spaces,
        "concatenated_string_for_hex": concatenated_str,
        "hex_value_ascii_of_concatenated_string": hex_value
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
