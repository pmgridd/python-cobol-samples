from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/greet', methods=['POST'])
def greet_user():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Please provide a 'name' in the request body."}), 400

    name = data['name']
    
    # In COBOL, INSPECT FUNCTION REVERSE(WS-FRIEND) TALLYING WS-TRAILING-SPACES FOR LEADING SPACES
    # was used to count trailing spaces. Python's strip() handles this more elegantly.
    cleaned_name = str(name).strip()

    if not cleaned_name:
        return jsonify({"error": "Name cannot be empty or just spaces."}), 400
        
    greeting = f"Hello, {cleaned_name}!"
    
    return jsonify({"greeting": greeting}), 200

if __name__ == '__main__':
    app.run(debug=True)