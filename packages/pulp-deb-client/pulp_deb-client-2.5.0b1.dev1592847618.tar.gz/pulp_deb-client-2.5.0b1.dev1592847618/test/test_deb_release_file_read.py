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

import pulpcore.client.pulp_deb
from pulpcore.client.pulp_deb.models.deb_release_file_read import DebReleaseFileRead  # noqa: E501
from pulpcore.client.pulp_deb.rest import ApiException

class TestDebReleaseFileRead(unittest.TestCase):
    """DebReleaseFileRead unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DebReleaseFileRead
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_deb.models.deb_release_file_read.DebReleaseFileRead()  # noqa: E501
        if include_optional :
            return DebReleaseFileRead(
                pulp_href = '0', 
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                artifacts = {
                    'key' : '0'
                    }, 
                codename = '0', 
                suite = '0', 
                distribution = '0', 
                relative_path = '0'
            )
        else :
            return DebReleaseFileRead(
                artifacts = {
                    'key' : '0'
                    },
                codename = '0',
        )

    def testDebReleaseFileRead(self):
        """Test DebReleaseFileRead"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
