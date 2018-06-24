from . import AbstractTest


class TestFoo(AbstractTest):

    def test_foo_get(self):
        response, status = self.get_json(f"/foo")
        self.assertEqual(status, 200)

    def test_foo_post(self):
        request = {
            "data": "TEST"
        }
        response, status = self.post_json(f"/foo", request)

        self.assertEqual(status, 200)
        assert isinstance(response, dict)
        assert response['returnData'] == "TEST"
