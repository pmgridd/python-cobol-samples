from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate_brakes_temperature', methods=['POST'])
def calculate_brakes_temperature():
    data = request.get_json()

    # Default values based on COBOL program
    m = data.get('m', 100.0)  # Mass of brake material in KG
    sh = data.get('sh', 800.0) # Specific heat of brake material in Joules per KG x Temp Celsius
    w = data.get('w', 10000.0) # Weight of the truck in KG
    d = data.get('d', 75.0)   # Vertical displacement on the downhill run in meters
    a = data.get('a', 9.8)    # a: 9.8 meters per second squared

    # Ensure all inputs are floats
    try:
        m = float(m)
        sh = float(sh)
        w = float(w)
        d = float(d)
        a = float(a)
    except ValueError:
        return jsonify({"error": "Invalid input type. All parameters must be numbers."}), 400

    # Calculate Mgh (loss of potential energy of the truck)
    # Mgh = (10,000 kg)(9.80 m/s2)(75.0 m) = 7.35 × 10^6 J.
    Mgh = w * a * d

    # Calculate the temperature change Mgh / m * c
    # where m is the mass of the brake material
    # and c is the specific heat given in the problem setup.
    mc = m * sh

    if mc == 0:
        return jsonify({"error": "Mass of brake material or specific heat cannot be zero."}), 400

    deltaT_Celsius = Mgh / mc

    results = {
        "Mgh": Mgh,
        "mc": mc,
        "deltaT_Celsius": deltaT_Celsius
    }

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)