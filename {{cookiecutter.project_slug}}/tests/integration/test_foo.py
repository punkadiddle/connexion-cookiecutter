from . import get_json, post_json


def test_foo_get():
    response, status = get_json(f"/foo")
    assert status == 200


def test_foo_post():
    request = {
        "data": "TEST"
    }

    response, status = post_json(f"/foo", request)

    assert status == 200
    assert isinstance(response, dict)
    assert response['returnData'] == "TEST"
