from functools import wraps
from flask import request, jsonify


def validate_convert_to_base13(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.json
        if data is None or 'inputdata' not in data or not isinstance(data['inputdata'], int):
            return jsonify({'error': 'Invalid input data. Expected an integer.'}), 400
        return f(*args, **kwargs)
    return decorated_function


def validate_multiply_matrix_scalar(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.json
        if data is None or 'inputdata' not in data:
            return jsonify({'error': 'Invalid input data. Expected matrix and scalar.'}), 400

        input_data = data['inputdata']
        matrix = input_data.get('matrix')
        scalar = input_data.get('scalar')

        if matrix is None or not all(isinstance(row, list) and all(isinstance(num, int) for num in row) for row in matrix):
            return jsonify({'error': 'Matrix must be a list of lists of integers.'}), 400

        if scalar is None or not isinstance(scalar, int):
            return jsonify({'error': 'Scalar must be an integer.'}), 400

        return f(*args, **kwargs)
    return decorated_function


def validate_solve_quadratic(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.json
        if data is None or 'inputdata' not in data or not isinstance(data['inputdata'], list) or len(data['inputdata']) != 3:
            return jsonify({'error': 'Invalid input data. Expected list of three numbers.'}), 400
        return f(*args, **kwargs)
    return decorated_function


def validate_remove_vowels(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.json
        if data is None or 'inputdata' not in data or not isinstance(data['inputdata'], str):
            return jsonify({'error': 'Invalid input data. Expected a string.'}), 400
        return f(*args, **kwargs)
    return decorated_function
