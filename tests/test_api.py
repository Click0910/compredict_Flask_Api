import json
from flask_jwt_extended import create_access_token
from api.serializers import StandardizationRequestSchema


def test_standardization_api(client):
    # create access token
    access_token = create_access_token(identity='user')

    # define request data
    request_data = {
        'signals': [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
            [10.0, 11.0, 12.0]
        ]
    }

    # define expected response data
    expected_response_data = {
        'signals': [
            [-1.3416407864998738, -1.3416407864998738, -1.3416407864998738],
            [-0.4472135954999579, -0.4472135954999579, -0.4472135954999579],
            [0.4472135954999579, 0.4472135954999579, 0.4472135954999579],
            [1.3416407864998738, 1.3416407864998738, 1.3416407864998738]
        ]
    }

    # convert request data to JSON
    request_data_json = json.dumps(request_data)

    # send POST request to API
    response = client.post('/api/standardize',
                           headers={'Authorization': 'Bearer {}'.format(access_token),
                                    'Content-Type': 'application/json'},
                           data=request_data_json)

    # check response status code
    assert response.status_code == 200

    # deserialize response data
    response_data, errors = StandardizationRequestSchema().load(response.json)

    # check for serialization errors
    assert not errors

    # check response data
    assert response_data == expected_response_data
