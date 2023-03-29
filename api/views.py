from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, create_access_token
from api.serializers import StandardizationRequestSchema, StandardizationResponseSchema
from sklearn.preprocessing import StandardScaler
import numpy as np


api_bp = Blueprint('api', __name__)


class StandardizationAPI(MethodView):
    @jwt_required()
    def post(self):
        # deserialize request data
        data, errors = StandardizationRequestSchema().load(request.get_json())

        # check for validation errors
        if errors:
            return jsonify(errors), 400

        # check for uniformity of list lengths
        if len(set(map(len, data['signals']))) != 1:
            return jsonify({'message': 'All signals must have the same length.'}), 400

        # standardize the input data
        scaler = StandardScaler()
        signals = np.array(data['signals'])
        standardized_signals = scaler.fit_transform(signals)

        # serialize response data
        response_data, errors = StandardizationResponseSchema().dump({
            'signals': standardized_signals.tolist()
        })

        # check for serialization errors
        if errors:
            return jsonify(errors), 500

        return jsonify(response_data), 200


class TokenAPI(MethodView):
    def post(self):
        # check if request has valid credentials
        if not request.is_json:
            return jsonify({'message': 'Missing JSON in request'}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return jsonify({'message': 'Missing username parameter'}), 400
        if not password:
            return jsonify({'message': 'Missing password parameter'}), 400

        # check if credentials are valid
        if username != 'user' or password != 'password':
            return jsonify({'message': 'Invalid username or password'}), 401

        # create and return access token
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200


class RefreshTokenAPI(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        # create and return new access token
        identity = {'username': request.jwt_identity}
        access_token = create_access_token(identity=identity)
        return jsonify({'access_token': access_token}), 200


# register API views as routes
api_bp.add_url_rule('/standardize', view_func=StandardizationAPI.as_view('standardize'))
api_bp.add_url_rule('/auth/token', view_func=TokenAPI.as_view('token'))
api_bp.add_url_rule('/auth/token/refresh', view_func=RefreshTokenAPI.as_view('refresh_token'))

