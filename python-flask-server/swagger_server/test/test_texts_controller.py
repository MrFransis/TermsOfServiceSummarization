# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.text import Text  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTextsController(BaseTestCase):
    """TextsController integration test stubs"""

    def test_add_text(self):
        """Test case for add_text

        Add a new text
        """
        body = Text()
        response = self.client.open(
            '/v2/text',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
