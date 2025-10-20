from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Gravitational constant G
G = 6.67428e-11

@app.route('/calculate_attraction', methods=['POST'])
def calculate_attraction():
    data = request.get_json()

    # Validate input data
    if not data or 'body1' not in data or 'body2' not in data:
        return jsonify({"error": "Invalid input. Please provide 'body1' and 'body2' data."}), 400

    body1 = data['body1']
    body2 = data['body2']

    required_fields = ['mass', 'vx', 'vy', 'px', 'py']
    for body in [body1, body2]:
        for field in required_fields:
            if field not in body:
                return jsonify({"error": f"Missing field '{field}' in body data."}), 400
            try:
                # Ensure numerical values
                body[field] = float(body[field])
            except ValueError:
                return jsonify({"error": f"Invalid value for field '{field}'. Must be a number."}), 400

    mass1, vx1, vy1, px1, py1 = body1['mass'], body1['vx'], body1['vy'], body1['px'], body1['py']
    mass2, vx2, vy2, px2, py2 = body2['mass'], body2['vx'], body2['vy'], body2['px'], body2['py']

    # Compute the distance between the two bodies
    dx = px1 - px2
    dy = py1 - py2
    d = math.sqrt((dx * dx) + (dy * dy))

    if d == 0:
        return jsonify({
            "message": "The bodies are in the same position!",
            "distance": 0,
            "force_of_attraction": 0,
            "force_along_x_axis": 0,
            "force_along_y_axis": 0
        }), 200

    # Compute the force of attraction
    f = (G * mass1 * mass2) / (d * d)

    # Compute the direction of force (using atan2 for accuracy)
    theta = math.atan2(dy, dx)
    fx = math.cos(theta) * f
    fy = math.sin(theta) * f

    results = {
        "distance": d,
        "force_of_attraction": f,
        "force_along_x_axis": fx,
        "force_along_y_axis": fy
    }

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)