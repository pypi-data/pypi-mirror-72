#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gutools` package."""

import pytest
import asyncio
import random
import time
import logging

from gutools import tools
from gutools.unet import TL, setup_config
from gutools.uagents import update_domestic, restore_domestic
from gutools.uapplication import UApplication
from aiopb.aiopb import Hub

@pytest.fixture
def app():
    hub = Hub()
    app = UApplication(hub=hub)
    return app

def test_protocol_reliability_TODO():
    """TODO: rewrite network test"""
    return

    setup_config()  # logging configuration

    async def logic(nodes, prob):
        """
        1. Wait until channels are ready
        2. Send broadcast and direct messages
        3. Wrap receive functions to simulate network dropping packets
        4. Listen to TL-1 receiving messages
        5. Send a sequence of numbers from TL-0 -> TL-1
           Some messages will be dropped
           Request/Resend/Watermark will do the work
        6. Wait until the last number is processed
           Stop the nodes
        7. Repeat the process again

        """
        logging.info(f"Network dropping probability : {prob*100}%")
        for tl in nodes:
            logging.debug(f'Starting {tl.uid} : id:{id(tl)}')


        def drop_packet(f, prob):
            def wrap(*args, **kw):
                if random.random() >= prob:
                    return f(*args, **kw)
                logging.debug('packet droppped :)')
            return wrap

        # wait until all channels are ready
        # await asyncio.gather(*[tl.channels_ready for tl in nodes])

        # send a 'broadcast' message
        t0, p0, baddr0, saddr0 = nodes[0].channels['broadcast']
        t1, p1, baddr1, saddr1 = nodes[1].channels['broadcast']
        p0.send('mykey', b'Hello', '*', saddr1)

        # send a 'direct' message
        t0, p0, baddr0, saddr0 = nodes[0].channels['broadcast']
        t1, p1, baddr1, saddr1 = nodes[1].channels['broadcast']

        # wrap functions to simulate packet dropping
        # and speed up the domestic: retry missing, etc
        for tl in nodes:
            for link, (_, protocol, _, _) in tl.channels.items():
                protocol.datagram_received = \
                    drop_packet(protocol.datagram_received, prob=prob)
                update_domestic(protocol.request_missing, restart=0.1)
                update_domestic(protocol._shake_channels, restart=0.1)

        N = 10
        __builtins__['__stop_test_TL_startup'] = False
        def check_end(key, message):
            if message == N - 1:
                logging.debug("Logic: Stopping nodes")
                __builtins__['__stop_test_TL_startup'] = True

        hub = Hub(realm='')
        hub.subscribe('mykey', check_end)

        to = nodes[1].uid
        for i in range(N):
            p0.send('mykey', i, to, saddr1)
            await asyncio.sleep(0.15)

        logging.debug("Logic: Waiting for nodes to end")
        for i in range(100):
            await asyncio.sleep(1)
            if __builtins__['__stop_test_TL_startup']:
                # stop nodes and restart original domestic settings
                for tl in nodes:
                    logging.debug(f"Stopping {tl.uid} : id:{id(tl)}")
                    tl.stop()
                    for link, (_, protocol, _, _) in tl.channels.items():
                        restore_domestic(protocol.request_missing)
                        restore_domestic(protocol._shake_channels)
                # unsubscribe function to not alter any futher test
                hub.unsubscribe('mykey', check_end)
                break

        # await asyncio.gather(*[tl.running for tl in nodes])

        foo = 1

    loop = asyncio.get_event_loop()

    t0 = time.time()
    N = 20
    for tries in range(N):
        test_nodes = []
        baseport = random.randint(10000, 20000)
        for i in range(2):
            uid = f'TL-{baseport}-{i}'
            uri = f'>udp://:{baseport + i}'
            tl = TL(loop=loop, uri=uri, uid=uid, app=app)
            test_nodes.append(tl)

        drop_prob = tries / N
        loop.run_until_complete(asyncio.gather(
            logic(test_nodes, drop_prob), *[tl.main() for tl in test_nodes]))

        elapsed = int(time.time() - t0)
        logging.info(f"Total elapsed time: {elapsed} secs")
        assert elapsed < 180 * 2, "Test is taking too much time"

    foo = 1

def test_1():
    pass

def test_2():
    pass

def test_3():
    pass

def test_4():
    pass

def test_5():
    pass

def test_6():
    pass

def test_7():
    pass

def test_8():
    pass

def test_9():
    pass

def test_A():
    pass

