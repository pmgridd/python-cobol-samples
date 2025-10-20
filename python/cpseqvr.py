from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_variable_records', methods=['POST'])
def process_variable_records():
    data = request.get_json()
    if not data or 'records' not in data or not isinstance(data['records'], list):
        return jsonify({"error": "Invalid input. Please provide a JSON object with a 'records' key containing a list of strings."}), 400

    input_records = data['records']
    processed_records = []
    record_count = 0

    for record in input_records:
        if not isinstance(record, str):
            return jsonify({"error": f"Invalid record '{record}'. Each record must be a string."}), 400

        # Simulate appending 'XXXXX' to each variable-length record
        # In COBOL, this would involve adjusting IN-RECLEN and OUT-RECLEN
        # and moving data to a larger buffer if needed. Here, we just concatenate.
        modified_record = record + 'XXXXX'
        processed_records.append(modified_record)
        record_count += 1
    
    response = {
        "processed_records": processed_records,
        "record_count": record_count
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)