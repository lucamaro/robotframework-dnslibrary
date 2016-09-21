#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of robotframework-dnslibrary.
# https://github.com/lucamaro/robotframework-dnslibrary

# Licensed under the Apache License 2.0 license:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2016, Luca Maragnani <luca.maragnani@gmail.com>

import unittest
from preggy import expect
from mock import MagicMock, create_autospec

from DNSLibrary import DNSLibrary
import dns
from tests.base import TestCase

class LibraryTestCase(TestCase):
    def test_set_target(self):
        client = DNSLibrary('localhost')
        client.set_dns_target('1.1.1.1')
        expect(client.target).to_equal('1.1.1.1')
        expect(client.resolver).to_be_null()
        
    def test_set_use_tcp(self):
        client = DNSLibrary()
        expect(client.use_tcp).to_be_false()
        client.set_use_tcp(True)
        expect(client.use_tcp).to_be_true()
        
    def test_query_record_A(self):
        client = DNSLibrary()
        
        class MockRecordA(object):
            def __init__(self):
                self.address = 'www.example.org'
                
        class MockResolver(object):
            def query(self, rr_type, rr_query, tcp=None):
                record = create_autospec(dns.rdtypes.IN.A)
                record.address = 'www.example.org'
                return [record]

        client._DNSLibrary__get_resolver = MagicMock(return_value=MockResolver())
        client.query_record('A','www.exmple.org')
        client.server_returned_n_answers(1)
    
    
if __name__ == "__main__":
    unittest.main()        