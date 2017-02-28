"""
Test Suite
Run via project root `make unit` or `make integration`
"""

import unittest
import os
import sys

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

# Add the external libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../app/'))


class BaseCase(unittest.TestCase):
    """
    Base Unit Test Case
    """
    is_unit = True

    def setUp(self):
        # Create a consistency policy that will simulate the High Replication consistency model.
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)

        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.testbed.init_taskqueue_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_search_stub()

    def tearDown(self):
        self.testbed.deactivate()
