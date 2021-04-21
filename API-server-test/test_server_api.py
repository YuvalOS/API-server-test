import requests

# success codes
OK = 200
UNAUTHORIZED = 401
NOT_FOUND = 404
INT_SERVER_ERROR = 500

server_url = 'http://localhost:8000'
server_url_auth = f'{server_url}/api/auth'
server_url_poly = f'{server_url}/api/poly'

access_token = ''
first_obj_id = ''


def test_auth_wrong_method():
    """
        test Authentication API - wrong method.
    """
    headers = {'Content-Type': 'application/json'}
    data = {'username': 'test', 'password': '1234'}
    request = requests.get(server_url_auth, headers=headers, json=data)
    assert request.status_code == INT_SERVER_ERROR
    assert request.json()['message'] == 'Method GET not allowed for URL /api/auth'
    request = requests.delete(server_url_auth, headers=headers, json=data)
    assert request.status_code == INT_SERVER_ERROR
    assert request.json()['message'] == 'Method DELETE not allowed for URL /api/auth'


def test_auth_wrong_user():
    """
        test Authentication API - user not exists.
    """
    global access_token
    headers = {'Content-Type': 'application/json'}
    data = {'username': 'test_1', 'password': '1234'}
    request = requests.post(server_url_auth, headers=headers, json=data)
    assert request.status_code == UNAUTHORIZED
    assert request.json()['reasons'] == ['User not found.']


def test_auth_wrong_password():
    """
        test Authentication API - wrong password.
    """
    global access_token
    headers = {'Content-Type': 'application/json'}
    data = {'username': 'test', 'password': '12345'}
    request = requests.post(server_url_auth, headers=headers, json=data)
    assert request.status_code == UNAUTHORIZED
    assert request.json()['reasons'] == ['Password is incorrect.']


def test_auth():
    """
        test Authentication API.
        save token for later test cases.
    """
    global access_token
    headers = {'Content-Type': 'application/json'}
    data = {'username': 'test', 'password': '1234'}
    request = requests.post(server_url_auth, headers=headers, json=data)
    assert request.status_code == OK
    access_token = request.json()['access_token']


def test_get_all_data():
    """
        test getting all data when database is empty.
    """
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    request = requests.get(server_url_poly, headers=headers)
    assert request.status_code == OK
    assert request.json() == []


def test_get_all_data_no_auth():
    """
        test getting all data when database is empty with no authentication.
        -- SHOULD FAIL !! --
    """
    headers = {'Content-Type': 'application/json'}
    request = requests.get(server_url_poly, headers=headers)
    assert request.status_code == UNAUTHORIZED
    assert request.json()['reasons'] == ['Authorization header not present.']


def test_post_data():
    """
        test posting one poly-data.
        saves object_id for later use.
    """
    global first_obj_id
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    data = {
        "data":
            [
                {
                    "key": "key1",
                    "val": "val_1",
                    "valType": "str"
                }
            ]
    }
    request = requests.post(f'{server_url_poly}', headers=headers, json=data)
    assert request.status_code == OK
    first_obj_id = request.json()['id']
    assert request.json() == {"id": first_obj_id, "values": [{"key": "key1", "val": "val_1", "valType": "str"}]}


def test_delete_data_by_id():
    """
        test deleting the poly-data that has been posted previously.
    """
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    request = requests.delete(f'{server_url_poly}/{first_obj_id}', headers=headers)
    assert request.status_code == OK
    assert request.json() == ''


def test_delete_data_by_id_no_auth():
    """
        test deleting data with no authentication.
    """
    headers = {'Content-Type': 'application/json'}
    request = requests.delete(f'{server_url_poly}/{first_obj_id}', headers=headers)
    assert request.status_code == UNAUTHORIZED
    assert request.json()['reasons'] == ['Authorization header not present.']


def test_delete_wrong_endpoint():
    """
        test deleting the '/api/poly' endpoint - which isn't allowed.
    """
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    request = requests.delete(f'{server_url_poly}', headers=headers)
    assert request.status_code == INT_SERVER_ERROR
    assert request.json()['message'] == 'Method DELETE not allowed for URL /api/poly/'


def test_delete_data_not_exists():
    """
        test deleting the poly-data from previous tests which doesn't exists anymore.
        -- SHOULDN'T FAIL ?? --
    """
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    request = requests.delete(f'{server_url_poly}/{first_obj_id}', headers=headers)
    assert request.status_code == OK
    assert request.json() == ''


def test_get_data_by_id():
    """
        test getting data by id.
        post -> get -> delete.
    """
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    data = {
        "data":
            [
                {
                    "key": "key1",
                    "val": "val_1",
                    "valType": "str"
                }
            ]
    }
    request = requests.post(f'{server_url_poly}', headers=headers, json=data)
    obj_id = request.json()['id']
    request = requests.get(f'{server_url_poly}/{obj_id}', headers=headers)
    assert request.status_code == OK
    assert request.json()['data'][0]['key'] == 'key1'
    assert request.json()['data'][0]['val'] == 'val_1'
    assert request.json()['data'][0]['valType'] == 'str'
    request = requests.delete(f'{server_url_poly}/{obj_id}', headers=headers)
    assert request.status_code == OK


def test_get_by_id_not_existed():
    """
        test getting data by id that doesn't exists.
    """
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    request = requests.get(f'{server_url_poly}/1', headers=headers)
    assert request.status_code == NOT_FOUND
    assert request.json()['message'] == 'Resource with id 1 was not found'


def test_get_data_by_id_no_auth():
    """
        test getting data by id.
        post -> get(w/o auth) -> delete(w/ auth).
    """
    headers = {'Content-Type': 'application/json'}
    data = {
        "data":
            [
                {
                    "key": "key1",
                    "val": "val_1",
                    "valType": "str"
                }
            ]
    }
    request = requests.post(f'{server_url_poly}', headers=headers, json=data)
    obj_id = request.json()['id']
    request = requests.get(f'{server_url_poly}/{obj_id}', headers=headers)
    assert request.status_code == UNAUTHORIZED
    assert request.json()['reasons'] == ['Authorization header not present.']
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    request = requests.delete(f'{server_url_poly}/{obj_id}', headers=headers)
    assert request.status_code == OK


def test_get_multiple_data_by_ids():
    """
        test getting multiple data objecys, to verify database can store more than one object.
        post(1) -> post(2) -> get(1) -> get(2) -> delete(1) -> delete(2)
    """
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    data1 = {
        "data":
            [
                {
                    "key": "key1",
                    "val": "val_1",
                    "valType": "str"
                }
            ]
    }
    request1 = requests.post(f'{server_url_poly}', headers=headers, json=data1)
    data2 = {
        "data":
            [
                {
                    "key": "key2",
                    "val": "val_2",
                    "valType": "str"
                }
            ]
    }
    request2 = requests.post(f'{server_url_poly}', headers=headers, json=data2)
    obj_id1 = request1.json()['id']
    obj_id2 = request2.json()['id']
    request1 = requests.get(f'{server_url_poly}/{obj_id1}', headers=headers)
    request2 = requests.get(f'{server_url_poly}/{obj_id2}', headers=headers)
    assert request1.status_code == OK
    assert request1.json()['data'][0]['key'] == 'key1'
    assert request1.json()['data'][0]['val'] == 'val_1'
    assert request1.json()['data'][0]['valType'] == 'str'
    assert request2.status_code == OK
    assert request2.json()['data'][0]['key'] == 'key2'
    assert request2.json()['data'][0]['val'] == 'val_2'
    assert request2.json()['data'][0]['valType'] == 'str'
    for obj_id in [obj_id1, obj_id2]:
        request = requests.delete(f'{server_url_poly}/{obj_id}', headers=headers)
        assert request.status_code == OK
