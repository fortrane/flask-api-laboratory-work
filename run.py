from app import app, db
from app.models import RequestHistory
from flask import request, jsonify
from app.services import convert_to_base13, multiply_matrix_scalar, solve_quadratic_equation, remove_vowels
from app.validation import validate_remove_vowels, validate_solve_quadratic, validate_multiply_matrix_scalar, validate_convert_to_base13
from werkzeug.exceptions import BadRequest


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    if e.description.startswith("Failed to decode JSON object"):
        return jsonify({'error': 'Invalid JSON format'}), 400
    return e.get_response()


@app.route('/api/history', methods=['GET'])
def get_history():
    limit = request.args.get('limit', default=20, type=int)

    history = RequestHistory.query.order_by(RequestHistory.id.desc()).limit(limit)

    return jsonify([{'id': h.id, 'endpoint': h.endpoint, 'input': h.input_data, 'result': h.result, 'timestamp': h.timestamp} for h in history])


@app.route('/api/convert_to_base13', methods=['POST'])
@validate_convert_to_base13
def api_convert_to_base13():
    data = request.json
    try:
        result = convert_to_base13(data.get('inputdata'))
        new_request = RequestHistory(endpoint='/api/convert_to_base13', input_data=str(data['inputdata']), result=str(result))
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/multiply_matrix_scalar', methods=['POST'])
@validate_multiply_matrix_scalar
def api_multiply_matrix_scalar():
    data = request.json
    matrix = data.get('inputdata', {}).get('matrix')
    scalar = data.get('inputdata', {}).get('scalar')

    if matrix is None or scalar is None:
        return jsonify({'error': 'Missing matrix or scalar in input data'}), 400

    result = multiply_matrix_scalar(matrix, scalar)
    return jsonify({'result': result})


@app.route('/api/solve_quadratic', methods=['POST'])
@validate_solve_quadratic
def api_solve_quadratic():
    data = request.json
    coefficients = data.get('inputdata')

    if len(coefficients) != 3:
        return jsonify({'error': 'Incorrect number of coefficients'}), 400

    a, b, c = coefficients
    result = solve_quadratic_equation(a, b, c)
    new_request = RequestHistory(endpoint='/api/solve_quadratic', input_data=str(coefficients), result=str(result))
    db.session.add(new_request)
    db.session.commit()
    return jsonify({'result': result})


@app.route('/api/remove_vowels', methods=['POST'])
@validate_remove_vowels
def api_remove_vowels():
    data = request.json

    if data is None or 'inputdata' not in data:
        return jsonify({'error': 'No input data'}), 400

    text = data.get('inputdata')
    if not isinstance(text, str):
        return jsonify({'error': 'The input data must be a string'}), 400

    result = remove_vowels(text)
    new_request = RequestHistory(endpoint='/api/remove_vowels', input_data=text, result=result)
    db.session.add(new_request)
    db.session.commit()
    return jsonify({'result': result})


@app.route('/api/history/<int:id>', methods=['DELETE'])
def delete_history(id):
    history_item = RequestHistory.query.get_or_404(id)
    db.session.delete(history_item)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200


@app.route('/api/history/<int:id>', methods=['GET'])
def get_specific_history(id):
    history_item = RequestHistory.query.get_or_404(id)
    return jsonify({'id': history_item.id, 'endpoint': history_item.endpoint, 'input': history_item.input_data, 'result': history_item.result, 'timestamp': history_item.timestamp})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
