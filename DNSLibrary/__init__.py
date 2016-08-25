#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of robotframework-dnslibrary.
# https://github.com/someuser/somepackage

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, lucamaro <luca.maragnani@gmail.com>

'''
    Module docstring
'''
from DNSLibrary.version import __version__  # NOQA
from robot.api import logger
from robot.api.deco import keyword
from robot.utils import asserts
import dns.resolver
import string


class DNSLibrary(object):
    '''
        Class docstring
    '''

    def __init__(self, target=None):
        '''
            Initialize class, with optionally the target specified
        '''
        self.target = target
        self.resolver = None
        self.answers = None

    def set_target(self, target):
        '''
            Set the new DNS target and force the reinitialization of resolver
        '''
        self.target = target
        self.resolver = None

    def __get_resolver(self):
        '''
            Returns the resolver initialized
        '''
        if self.resolver is None:
            self.resolver = dns.resolver.Resolver()

            if self.target is None:
                logger.info("No target specified, using system resolver")
            else:
                self.resolver.nameservers = [self.target]
        return self.resolver

    @keyword('Query ${rr_type:[^ ]+} for ${rr_query:[^ ]+}')
    def query_record(self, rr_type, rr_query):
        '''
            Resolve A record, keep an internal answer object to be analized
        '''
        self.answers = self.__get_resolver().query(rr_query, rr_type)

    @keyword('Server Returned ${n_answers:\d+}')
    def server_returned_n_answers(self, n_answers):
        '''
            Method documentation
        '''
        if len(self.answers) != int(n_answers):
            raise Exception("Expected " + str(n_answers) +
                            " answers, but received (" + len(self.answers) + ")")

    def answer_is(self, ans_number, ans_type, **kwargs):
        '''
            Assert that the received answer is equal to parameters specified
            Parameters:
                + ans_number: select answer number
                + ans_type: query type (e.g. "A")
                + kwargs: resource specific data
                
            Examples:
            Answer Is   ${0}    A   address=10.10.10.10
            Answer Is   ${0}    MX   exchange=mx.example.org    preference=${10}
        '''
        answer = self.answers[ans_number]
        errors = []

        for attr in kwargs:
            if not hasattr(answer, attr):
                raise Exception(
                    "Field " +
                    attr +
                    " not found. Answer has fields: " +
                    dir(answer))
            if kwargs[attr] != getattr(answer, attr):
                errors.append(
                    "Expected " +
                    attr +
                    " equals to " +
                    str(kwargs[attr]) +
                    ", but found " +
                    str(getattr(
                        answer,
                        attr)))
                        
        if len(errors) > 0:
            raise Exception(
                "Found those errors:\n\t" +
                string.join(
                    errors,
                    '\n\t'))
