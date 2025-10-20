from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# SKU Lookup Table (equivalent to WS-SKU-LOOKUP-TABLE)
# Maps (THEIR-PRODUCT-CODE-PREFIX) to (OUR-SKU-GROUP-CODE)
SKU_LOOKUP_TABLE = {
    'AB': 'TC45',
    'GT': 'HH05',
    'KR': 'NB13',
    'PK': 'CC19',
    'ZW': 'YT54'
}
DEFAULT_SKU_PREFIX = 'XX00'

# Helper to convert a string to its ASCII hexadecimal representation
def string_to_ascii_hex(input_string):
    return ''.join([f'{ord(char):02x}' for char in input_string]).upper()

@app.route('/reformat_record', methods=['POST'])
def reformat_record():
    input_data = request.get_json()

    # --- Input Record Extraction and Validation ---
    required_fields = [
        'in_product_code', 'in_product_desc', 'in_invoice_no',
        'in_quantity', 'in_unit_price', 'in_invoice_date', 'in_taxable'
    ]
    for field in required_fields:
        if field not in input_data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    in_product_code = str(input_data['in_product_code'])
    in_product_desc = str(input_data['in_product_desc'])
    in_invoice_no = str(input_data['in_invoice_no'])
    in_taxable = str(input_data['in_taxable']).upper() # 'Y' or other (space in COBOL)

    try:
        in_quantity = int(input_data['in_quantity'])
        in_unit_price = float(input_data['in_unit_price'])
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid numeric input: {e}"}), 400

    # Date reformatting (MM/DD/YY to YYYY-MM-DD)
    in_invoice_date_str = str(input_data['in_invoice_date'])
    try:
        # Assuming MM/DD/YY format
        # For YY, Python's %y handles 00-99. datetime will typically interpret as 20xx for >= 69 and 19xx for < 69.
        # The COBOL code uses CURRENT-CENTURY. For simplicity, we'll assume a 20xx century for all 2-digit years.
        # This is a common interpretation for 2-digit years in modern systems.
        invoice_date_obj = datetime.strptime(in_invoice_date_str, '%m/%d/%y')
        # If the year is <= current_year % 100, assume 20xx, otherwise 19xx for a more robust interpretation
        # For this migration, aligning with COBOL\'s current century logic, we force 20xx if it's a 2-digit year.
        # A more complex rule based on CURRENT-DATE could be:
        # current_year_2_digit = datetime.now().year % 100
        # if invoice_date_obj.year > current_year_2_digit + OFFSET (e.g. 20): # To allow future dates
        #    invoice_date_obj = invoice_date_obj.replace(year=invoice_date_obj.year - 100)
        # However, the COBOL original used CURRENT-CENTURY, which means it would prepend the current century.
        # Let's align with that simple century interpretation if the year is 2 digits.
        if invoice_date_obj.year < 100: # It's a 2-digit year from %y
            current_century = (datetime.now().year // 100) * 100
            # If the 2-digit year implies a date in the past century (e.g., current year 2023, input 95 -> 1995)
            # COBOL\'s CURRENT-CENTURY logic means if current year is 2023, YY 22 -> 2022, YY 95 -> 2095 (incorrect for past)
            # A common date interpretation is: 00-49 -> 2000-2049, 50-99 -> 1950-1999
            # But the COBOL specifically says MOVE WS-CURRENT-CENTURY TO WS-DATE-CENTURY
            # This implies if current year is 2023, any 'YY' becomes '20YY'.
            # Let's use the explicit `datetime.strftime` to get 4 digit year properly.
            out_inv_date_yyyy_mm_dd = invoice_date_obj.strftime('%Y-%m-%d')
        else: # Already a 4-digit year, or more specific format
            out_inv_date_yyyy_mm_dd = invoice_date_obj.strftime('%Y-%m-%d')

    except ValueError:
        return jsonify({"error": f"Invalid date format for in_invoice_date: {in_invoice_date_str}. Expected MM/DD/YY."}), 400

    # SKU Lookup and Transformation
    in_product_code_prefix = in_product_code[0:2]
    ws_sku_prefix = SKU_LOOKUP_TABLE.get(in_product_code_prefix, DEFAULT_SKU_PREFIX)
    out_sku = ws_sku_prefix + in_product_code[2:4]

    # Taxable Item Conversion ('Y' to True, others to False)
    taxable_item = (in_taxable == 'Y')
    
    # Output record construction
    output_record = {
        "out_sku": out_sku,
        "out_item_desc": in_product_desc,
        "out_quantity": in_quantity,
        "out_unit_price": in_unit_price,
        "out_invoice_no": in_invoice_no,
        "out_inv_date_yyyy_mm_dd": out_inv_date_yyyy_mm_dd,
        "taxable_item": 'T' if taxable_item else 'N' # Mimicking 88-level output
    }

    # Simulate hexadecimal conversion for OUTPUT-RECORD (concatenating string values)
    # This is a simplified hex representation, not byte-for-byte memory layout.
    concatenated_output_for_hex = (
        output_record["out_sku"].ljust(10) +
        output_record["taxable_item"].ljust(1) +
        output_record["out_item_desc"].ljust(30) +
        str(output_record["out_quantity"]).zfill(5) + # Assuming 5 digits for S9(5) COMP-3
        str(f'{output_record["out_unit_price"]:.2f}').replace('.', '').zfill(9) + # S9(7)V99 COMP-3, 9 digits
        output_record["out_invoice_no"].ljust(16) +
        output_record["out_inv_date_yyyy_mm_dd"].ljust(8)
    )
    # The actual COBOL length of OUTPUT-RECORD (10+1+30+3+5+16+8) = 73 if comp-3 is 3 and 5 bytes.
    # We are using string representation, so lengths will be different
    # S9(5) COMP-3 is typically 3 bytes. S9(7)V99 COMP-3 is typically 5 bytes.
    # The string_to_ascii_hex will convert the string representation of these.
    # The COBOL example for HEX2TEXT had specific lengths for HEX-OUTPUT-RECORD-HIGH-ORDER PIC X(73) and LOW-ORDER PIC X(73).
    # This implies the OUTPUT-RECORD group item itself would be 73 characters long in display format, not the binary representation.
    # Let's adjust the concatenated string to be closer to the COBOL PICs for hex conversion.
    # OUT-SKU PIC X(10)
    # FILLER PIC X (for TAXABLE-ITEM)
    # OUT-ITEM-DESC PIC X(30)
    # OUT-QUANTITY PIC S9(5) COMP-3 (let's assume 5 chars for display, though it's binary)
    # OUT-UNIT-PRICE PIC S9(7)V99 COMP-3 (let's assume 9 chars for display, though it's binary)
    # OUT-INVOICE-NO PIC X(16)
    # OUT-INV-DATE-YYYY-MM-DD PIC X(08)
    
    # Reconstruct for hex conversion based on typical display lengths of COBOL fields
    display_out_quantity = str(output_record["out_quantity"]).rjust(5, '0')
    display_out_unit_price = f'{output_record["out_unit_price"]:.2f}'.replace('.', '').rjust(9, '0') # Example: 000054900
    
    concatenated_output_for_hex_display = (\
        output_record["out_sku"].ljust(10) +\
        output_record["taxable_item"] +\
        output_record["out_item_desc"].ljust(30) +\
        display_out_quantity +\
        display_out_unit_price +\
        output_record["out_invoice_no"].ljust(16) +\
        output_record["out_inv_date_yyyy_mm_dd"].ljust(8)\
    )

    hex_output_record = string_to_ascii_hex(concatenated_output_for_hex_display)

    return jsonify({
        "input_record": input_data,
        "output_record": output_record,
        "hex_representation_of_output_record_display_format": hex_output_record,
        "notes": "Hexadecimal representation is of the string equivalent of the display-formatted output record, not its raw binary memory layout."
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
