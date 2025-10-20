from flask import Flask, request, jsonify

app = Flask(__name__)

# Constants
SALES_TAX_RATE = 0.065

@app.route('/calculate_invoice_total', methods=['POST'])
def calculate_invoice_total():
    invoice_data = request.get_json()

    if not invoice_data:
        return jsonify({"error": "No invoice data provided."}), 400

    # Initialize totals
    cumulative_price_before_tax = 0.0
    cumulative_price_with_tax = 0.0
    cumulative_sales_tax = 0.0

    # Extract invoice details (with default/validation)
    inv_number = invoice_data.get('inv_number', 'N/A')
    inv_date = invoice_data.get('inv_date', 'N/A') # YYYYMMDD format expected for COBOL original
    inv_line_items = invoice_data.get('inv_line_items', [])
    is_return = invoice_data.get('is_return', 'N') == 'R'

    if not isinstance(inv_line_items, list):
        return jsonify({"error": "Invoice line items must be a list."}), 400

    for i, line_item in enumerate(inv_line_items):
        try:
            unit_price = float(line_item.get('unit_price'))
            quantity = int(line_item.get('quantity'))
            taxable = line_item.get('taxable', 'T') == 'T' # Default to taxable if not specified
            sku = line_item.get('sku', 'UNKNOWN')

            if quantity < 0 or unit_price < 0:
                return jsonify({"error": f"Line item {i+1}: Quantity and unit price cannot be negative."}), 400

            line_working_total = unit_price * quantity
            line_working_tax = 0.0

            if taxable:
                line_working_tax = line_working_total * SALES_TAX_RATE
                line_working_total += line_working_tax

            cumulative_price_before_tax += (unit_price * quantity) # Original before tax for this line
            cumulative_price_with_tax += line_working_total
            cumulative_sales_tax += line_working_tax

        except (ValueError, TypeError) as e:
            return jsonify({"error": f"Invalid data in line item {i+1}: {e}"}), 400

    # Final invoice totals
    inv_total_amount = cumulative_price_with_tax
    inv_total_before_tax = cumulative_price_before_tax
    inv_total_sales_tax = cumulative_sales_tax

    # Format output similar to COBOL display
    # Assuming inv_date is 'YYYYMMDD' for formatting
    formatted_inv_date = inv_date
    if len(inv_date) == 8 and inv_date.isdigit():
        formatted_inv_date = f"{inv_date[0:4]}/{inv_date[4:6]}/{inv_date[6:8]}"
    
    # Generate detailed line item report
    formatted_line_items = []
    for i, line_item in enumerate(inv_line_items):
        formatted_line_items.append({
            "line_number": i + 1,
            "sku": line_item.get('sku', 'UNKNOWN'),
            "quantity": int(line_item.get('quantity', 0)),
            "unit_price": float(line_item.get('unit_price', 0.0)),
            "taxable_item": line_item.get('taxable', 'T') == 'T'
        })


    response = {
        "invoice_number": inv_number,
        "invoice_date": formatted_inv_date,
        "total_amount": round(inv_total_amount, 2),
        "total_before_tax": round(inv_total_before_tax, 2),
        "total_sales_tax": round(inv_total_sales_tax, 3), # COBOL had 3 decimal places for tax
        "sales_tax_rate": SALES_TAX_RATE,
        "is_return": is_return,
        "line_items_summary": formatted_line_items
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
