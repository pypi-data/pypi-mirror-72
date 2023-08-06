#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module test Loop features

"""

import pytest
import time


import functools

from lswarm.stm import Layer, Reactor, \
    STATE_INIT, STATE_READY, STATE_END,\
    MERGE_ADD

class FakeEventInjector():
    """Helper class to inyect some events from time to time
    using a local socket as transport layer.
    """
    
class FakeServer():
    """"""
    
class FakeClient():
    """"""

from .helpers import _TestLayer

class Clock(_TestLayer):

    def _setup_test_clock(self):
        states = {
        }
        transitions = {
            STATE_READY: {
                # set an additional timer
                'each:3,2': [
                    [STATE_READY, [], ['timer']],
                ],
            },
        }
        return states, transitions, MERGE_ADD
    
@pytest.fixture
def reactor():
    reactor = Reactor()
    return reactor


def test_layer_definition(reactor):
    """"
    - [ ] Load a STM definition from a file
    - [ ] Bind (strict=False) with a class / instance which such methods
    - [ ] Bind (strict=True) with a class / instance which a missing method
    - [ ] Bind with an external class / instance which doesn't hinherit from Layer
    """

def test_timers(reactor):
    """"
    - [ ] Test Timeout
    - [ ] Test Restarting Timer
    - [ ] Test Restarting Timer with Timeout
    """
    reactor = Reactor()
    clock = Clock()
    reactor.attach(clock)
    reactor.loop.run()
    foo = 1
    
    
def test_stm_sharing_same_context(reactor):
    """"
    - [ ] Stack many layers that respond to the same event buy they share the same context (STM)
    """


def test_connect():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_listen():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_attaching_existing_protocol():
    """
    - [ ] connect to somewhere and attach a STM
    - [ ] seach for an existing connection
    - [ ] attach to existing connection
    """


def test_multiples_reactors():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_serialize_app():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_register_protocols():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

def test_foo():
    """"
    - [ ] xxx
    - [ ] xxx
    - [ ] xxx
    """

