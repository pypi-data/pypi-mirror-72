# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.api.content_files_api import ContentFilesApi  # noqa: E501
from pulpcore.client.pulp_file.rest import ApiException


class TestContentFilesApi(unittest.TestCase):
    """ContentFilesApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_file.api.content_files_api.ContentFilesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create(self):
        """Test case for create

        Create a file content  # noqa: E501
        """
        pass

    def test_list(self):
        """Test case for list

        List file contents  # noqa: E501
        """
        pass

    def test_read(self):
        """Test case for read

        Inspect a file content  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
