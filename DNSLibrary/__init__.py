#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of robotframework-dnslibrary.
# https://github.com/lucamaro/robotframework-dnslibrary

# Licensed under the Apache License 2.0 license:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2016, Luca Maragnani <luca.maragnani@gmail.com>

'''
    Module docstring
'''
from DNSLibrary.version import __version__  # NOQA
from robot.api import logger
from robot.api.deco import keyword
from robot.utils import asserts
import dns.resolver
import string
import re

ATTRS = {
    'A': ['address'],
    'AAAA': ['address'],
    'CNAME': ['target'],
    'NS': ['target'],
    'PTR': ['target'],
    'MX': [
        'exchange',
        'preference'],
    'SOA': [
        'expire',
        'minimum',
        'mname',
        'refresh',
        'retry',
        'rname',
        'serial'],
    'SPF': ['strings'],
    'TXT': ['strings'],
    'NAPTR': [
        'flags',
        'order',
        'preference',
        'regexp',
        'replacement',
        'service'],
    'SRV': [
        'port',
        'priority',
        'target',
        'weight']}


def _print_answers(answers, rr_type):
    '''
        Takes a list of answers and print them into log file
    '''
    for i in range(len((answers))):
        attrs_string = ""
        for attr in ATTRS[rr_type]:
            if attrs_string != "":
                attrs_string += ", "
            attrs_string += attr + ": " + \
                str(getattr(answers[i], attr))
        logger.info(
            "Attributes for record " +
            str(i) +
            ": " +
            attrs_string)


class DNSLibrary(object):
    '''
    This is DNSLibrary version 0.1.0 for RobotFramework.
    The aim is testing a DNS target as a client, using dnspython library.
    '''

    def __init__(self, target=None):
        '''
            Initialize class, with optionally the target specified
        '''
        self.target = target
        self.resolver = None
        self.answers = None
        self.use_tcp = False

    def set_dns_target(self, target):
        '''
            Set the new DNS target and force the reinitialization of resolver
        '''
        self.target = target
        self.resolver = None

    def set_use_tcp(self, use_tcp=True):
        '''
            Set TCP/UDP usage (by default will be used UDP)
        '''
        self.use_tcp = use_tcp

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
            Resolve a record of type ``rr_type``, keep an internal answer
            object to be analized
        '''
        logger.debug('Sending query to ' + str(self.target) + ' with protocol ' + ('TCP' if self.use_tcp else 'UDP'))
        self.answers = self.__get_resolver().query(rr_query, rr_type, tcp=self.use_tcp)
        _print_answers(self.answers, rr_type)

    @keyword('Server Returned ${n_answers:\d+} Answers')
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
            - ans_number: select answer number
            - ans_type: query type (e.g. "A")
            - kwargs: resource specific data

            Examples:
            | Answer Is   ${0}    A   address=10.10.10.10
            | Answer Is   ${0}    MX   exchange=mx.example.org    preference=${10}
        '''
        answer = self.answers[ans_number]
        errors = []

        for attr in kwargs:
            if not hasattr(answer, attr):
                raise Exception(
                    "Field " +
                    attr +
                    " not found. Answer has fields: " +
                    str(dir(answer)))

            if re.match(re.compile(str(kwargs[attr])), str(
                    getattr(answer, attr))) is None:
                errors.append(
                    "Expected " +
                    attr +
                    " equals to " +
                    str(kwargs[attr]) +
                    " but found " +
                    str(getattr(
                        answer,
                        attr)))

        if len(errors) > 0:
            raise Exception(
                "Found those errors:\n\t" +
                string.join(
                    errors,
                    '\n\t'))
