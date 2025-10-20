from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_records', methods=['POST'])
def process_records():
    data = request.get_json()
    if not data or 'records' not in data or not isinstance(data['records'], list):
        return jsonify({"error": "Invalid input. Please provide a JSON object with a 'records' key containing a list of strings."}), 400

    input_records = data['records']
    processed_records = []
    record_count = 0

    for record in input_records:
        if not isinstance(record, str) or len(record) != 40:
            return jsonify({"error": f"Invalid record '{record}'. Each record must be a 40-character string."}), 400

        # Simulate COBOL's fixed-length record fields and their reversal
        input_first_10 = record[0:10]
        input_last_30 = record[10:40]

        output_record = input_last_30 + input_first_10
        processed_records.append(output_record)
        record_count += 1
    
    response = {
        "processed_records": processed_records,
        "record_count": record_count
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
