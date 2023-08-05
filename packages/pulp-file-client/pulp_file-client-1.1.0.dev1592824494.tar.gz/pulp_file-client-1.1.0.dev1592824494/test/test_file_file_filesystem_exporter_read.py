# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.models.file_file_filesystem_exporter_read import FileFileFilesystemExporterRead  # noqa: E501
from pulpcore.client.pulp_file.rest import ApiException

class TestFileFileFilesystemExporterRead(unittest.TestCase):
    """FileFileFilesystemExporterRead unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test FileFileFilesystemExporterRead
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_file.models.file_file_filesystem_exporter_read.FileFileFilesystemExporterRead()  # noqa: E501
        if include_optional :
            return FileFileFilesystemExporterRead(
                pulp_href = '0', 
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                name = '0', 
                path = '0'
            )
        else :
            return FileFileFilesystemExporterRead(
                name = '0',
                path = '0',
        )

    def testFileFileFilesystemExporterRead(self):
        """Test FileFileFilesystemExporterRead"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
