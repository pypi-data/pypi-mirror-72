"""
UNet module provide a asyncio Transport Layer to comunicate peers.

This module is mainly intended to send pub/sub messages to remote peers.

TODO: encapsulate pub/sub messages (key, payload)

"""
import asyncio
import socket
import random
import re
import struct
import ujson as json
import pickle
import base64
import logging
import zlib
import uuid

from asyncio.protocols import DatagramProtocol

# own libraries
from gutools.tools import add_to_loop, new_uid, parse_uri, serializable_container, rebuild
from gutools.uagents import UAgent, Domestic, domestic
from gutools.uobjects import UObject, SmartContainer, Answer


from loganalyzer.loganalyzer import setup_config


class Request(object):
    """Encapsulate a request with related response."""
    def __init__(self, uri):
        self.uri = uri
        self.uid = new_uid()
        self.response = Response()

class Response(Answer):
    """Encapsulate a response.
    Inherits from Answer."""
    pass

class Session(object):
    "TBD"
    pass

class UProtocolFactory():
    """Protocol Factory used by TL."""
    def __init__(self, uid, link, tl):
        self.uid = uid
        self.link = link
        self.tl = tl
        self.types = {
            'broadcast': UProtocol,
            'direct': UProtocol,
        }

    def __call__(self):
        # TODO: implemente a real factory here based on config or (hash) uid
        proto_klass = self.types.get(self.link)
        return proto_klass(self.uid, self.tl)


class UProtocol(DatagramProtocol, Domestic):
    """
    DatagramProtocol to comunicate with a peer.

    It will keep input and output queues in order to provide a
    reliable *stream* of datagrams.

    User can use direct functions like `send(key, data, to, address)`
    or publishing in the same realm with key='/net/publish'

    - `uid`: the uid of the peer-connection.
    - `realm`: the realm to attend pub/sub.

    Special keys:

    - `MISSING`: used for requesting missing datagrams
    - `WATERMARK`: update peer watermark and drop packets received by peer.

    (sender, to, payload)
    """
    def __init__(self, uid, tl):
        DatagramProtocol.__init__(self)
        Domestic.__init__(self)
        self.uid = uid
        self.tl = tl

        self._output = dict()
        self._input = dict()
        self._out_sequence = dict()
        self._in_sequence = dict()

        self._oob_handlers = {
            'MISSING': self._resend_missing,
            'WATERMARK': self._update_watermark,
        }

    def connection_made(self, transport):
        self.transport = transport
        addr = self.transport.get_extra_info('socket').getsockname()
        logging.debug("connection_made: {}: {}".format(self.uid, addr))

    def connection_lost(self, exc):
        logging.debug(f'connection_lost: {exc}')

    def datagram_received(self, raw, addr):
        baddr = self.transport.get_extra_info('socket').getsockname()
        raw = zlib.decompress(raw)
        sender, to, sequence, payload = json.decode(raw.decode())
        if sender == self.uid:
            logging.debug(f'>> [{self.uid}] Skip <{payload}> self-loop-message from {addr} in {baddr}')
            return

        if to in (self.uid, ):  # direct message (broadcast or direct socket)
            logging.debug(f">> [{self.uid}] Received <{payload}> from {sender}:{addr} to '{to}' in {baddr}")

            in_sequence = self._in_sequence.get(sender, 0)
            if sequence < in_sequence:
                return  # already dispatched message (is an echo)

            inputs = self._input.get(sender)
            if inputs is None:
                inputs = self._input[sender] = dict()
            inputs[sequence] = (payload, addr)

            while in_sequence in inputs:
                (key, data), addr = inputs.pop(in_sequence)
                in_sequence += 1
                # TODO: include sender in published message?
                self.tl.hub.publish(key, data)

            self._in_sequence[sender] = in_sequence
            # self.request_missing()

        elif to in ('', '*'):  # anyone or OOB message, do not manage sequences
            logging.debug(f">> [{self.uid}] Received <{payload}> from {sender}:{addr} to '{to}' in {baddr}")
            (key, data) = payload
            func = self._oob_handlers.get(key)
            if func:
                func(key, data, sender)
            else:
                self.tl.hub.publish(key, data)
        else:
            logging.warn(f">> [{self.uid}] Ignoring <{payload}> from {sender}:{addr} to '{to}' in {baddr}")

    def send(self, key, data, to, address):
        """Send a (key, data) pub/sub message to a specific peers or
        broadcasting.

        - If `to` is empty or '*' then message is consider broadcast.
        - Else is added to the specific peer queue.
        - `address` could be an <broadcast> address or direct one.
        """
        logging.debug(f"send: {self.uid} -> {to}: {address}")

        # get peer sequence
        if to not in ('', '*'):
            sequence = self._out_sequence.setdefault(to, 0)
            self._out_sequence[to] += 1
        else:
            sequence = -1

        # encode raw message
        payload = (key, data)
        raw = json.encode((self.uid, to, sequence, payload)).encode()
        raw = zlib.compress(raw)

        # save message for replaying when network fails
        if to not in ('', '*'):
            output = self._output.get(to)
            if output is None:
                output = self._output[to] = dict()
            output[sequence] = (raw, address)

        self.transport.sendto(raw, address)

    @domestic(restart=2)
    def request_missing(self):
        "domestic task for request missing datagrams"
        for sender, inputs in self._input.items():
            keys = inputs.keys()
            if keys:
                m = max(keys)
                missing = set(range(self._in_sequence[sender], m))
                missing.difference_update(keys)
                _, address = inputs[m]
                if missing:
                    logging.debug(f'{self.uid} Request MISSING: {missing}')
                    self.send('MISSING', missing, '', ('<broadcast>', 9999))
            else:
                watermark = self._in_sequence[sender] - 1
                logging.debug(f'{self.uid} Sending WATERMARK: {watermark}')
                self.send('WATERMARK', watermark, '', ('<broadcast>', 9999))
        foo = 1

    def _resend_missing(self, key, missing, sender):
        "resent some missing datagrams"
        logging.debug(f'{self.uid} Resend MISSING: {missing}')
        output = self._output.get(sender)
        if output and missing:
            for sequence in missing:
                info = output.get(sequence)
                info and self.transport.sendto(*info)
            watermark = min(missing) - 1
            self._update_watermark(key, watermark, sender)

    def _update_watermark(self, key, watermark, sender):
        "Update the watermark and remove the already sent messages"
        output = self._output.get(sender, {})
        for k in [k for k in output.keys() if k <= watermark]:
            output.pop(k)

    @domestic()
    def _shake_channels(self):
        """Domestic function that tries to *shake* peers channels taking a
        proactive role sending a random packet or the last sent packet
        to the peer.

        This behavior pretend to update remote queues in order the remote
        peers can request for updated information.

        This is due *missing packets* request or the *last packet* maybe can
        be lost so peers may think there is nothing else to do, but
        actually they have missing information that may never
        receive unless the sender sent more packets that hopefuly update the
        last packet sequence creating a *hole* that can be filled.
        """
        if random.random() > 0.5:
            # send Last Packet (to update missing in remote site)
            for sender, sequence in self._out_sequence.items():
                info = self._output[sender].get(sequence - 1)
                if info:
                    logging.debug(f'{self.uid} Sending Last: {sequence-1}')
                    self.transport.sendto(*info)
        else:
            # send a random packet because if more probable that
            # remote peer already know the end of the queue
            # so we're proactivel send a possible 'missing' packet
            # due missing requests may also be lost
            for sender, info in self._output.items():
                if info:
                    sequence = random.choice(list(info.keys()))
                    info = info[sequence]
                    logging.debug(f'{self.uid} Sending Random Packet: {sequence}')
                    self.transport.sendto(*info)



class TL(UAgent):
    """An asyncio Transport Layer

    This class send pub/sub message to remote peers.

    - Message sendings are reliable.
    - Uses two channels for UDP and UDP broadcasting.

    User can simply publish to `/net/publish` channel in the same `realm`
    or use `send()` method.
    """
    def __init__(self, uid=None, app=None, uri='>udp://:9090', loop=None):
        super(TL, self).__init__(uid, app)
        self.uri = uri
        self._uri = parse_uri(uri, bind='')
        self.channels = dict()
        "active transports and protocols"

        self._loop = None  # set in start()

        "Future that points out when all channels are ready for use."

        self.app.hub.subscribe('/net/publish', self.send_pubsub)
        self.app.hub.subscribe('/net/receive', self.receive_pubsub)

        foo = 1

    async def main(self):
        """`main` asyncio method for TL agent.

        - open channels
        - wait until agent is stopped
        - close channels
        """
        # open communications channels
        await self.start()
        self.channels_ready.set_result(True)

        # now coroutine holds until Agent is stopped
        await self.running

        # close channels
        await self.stop()

    def stop(self):
        for link, (transport, protocol, _, _) in self.channels.items():
            protocol.stop_domestics()  # del protocol ?
            # transport.close()  # done in self.stop

        self.running.set_result(False)


    def send_pubsub(self, key, message):
        """Send a pub/sub (key, message) by broadcasting to all peers in
        the same <broadcast> address.

        TODO: need to review encapsulation. Do not use URecord.
        """
        # payload = (key, message)
        raw = pickle.dumps(message)
        raw = base64.urlsafe_b64encode(raw)
        # raw = zlib.compress(raw)
        transport, protocol, baddr, saddr = self.channels['broadcast']
        protocol.send(key='/net/receive', data=raw, to='*', address=saddr)

    def receive_pubsub(self, key, raw):
        """Inject a remote (key, data) pub/sub message"""
        # raw = zlib.decompress(raw)
        raw = base64.urlsafe_b64decode(raw)
        key, data = pickle.loads(raw)
        self.hub.publish(key, data)

    async def start(self):
        """Create open channels for <broadcast> and direct communications.

        - Create a UDP socket with specific options.
        - Bind the socket.
        - Create a asyncio transport and protocol.
        - Add to self.channels dict
        """

        # TODO: are asyncio.events instead futures?
        self.running = self._loop.create_future()
        self.channels_ready = self._loop.create_future()

        channels = {
            'broadcast': {
                'options': [(socket.SO_BROADCAST, 1), (socket.SO_REUSEADDR, 1), ],
                'bind': ('', 9999),
            },
            'direct': {
                'options': [(socket.SO_BROADCAST, 1), (socket.SO_REUSEADDR, 1), ],
            }
        }
        address = list(self._uri['address'])
        for i, (link, info) in enumerate(channels.items()):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                     socket.SOL_UDP)
            for option, value in info['options']:
                sock.setsockopt(socket.SOL_SOCKET, option, value)

            addr = info.get('bind', tuple(address))
            sock.bind(addr)
            # print(self.uri, link, addr)
            # address[1] += 1  # next link will be binded to the next port

            factory = UProtocolFactory(
                uid=self.uid, link=link, tl=self
            )

            transport, protocol = await self._loop.create_datagram_endpoint(
                lambda: factory(),
                sock=sock,
            )
            if link in ('broadcast', ):
                saddr = tuple([f'<{link}>', addr[1]])
            else:
                saddr = addr
            self.channels[link] = (transport, protocol, addr, saddr)
        foo = 1

    async def stop(self):
        """Close all active channels by closing its transports."""
        for link, (transport, _, _, _) in self.channels.items():
            transport.close()


# HEADER_FORMAT = '>L'
# HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
# class UStreamAgent(UAgent):
    # def __init__(self,  uid=None, realm='', uri='tcp://localhost:9090'):
        # super().__init__(uid, realm)
        # self.uri = uri
        # self._uri = parse.urlparse(uri)
        # self.address = split_netloc(self._uri.netloc)

        # self.reader = None
        # self.writer = None

        # self.running = asyncio.Future()
        # self.channels_ready = asyncio.Future()

        # self.msg = b''

    # async def _next_message(self, reader, writer):
        # context = {}
        # while len(self.msg) < HEADER_SIZE:
            # data = await reader.read(0x1000)
            # self.msg += data

        # size, = struct.unpack_from(HEADER_FORMAT, self.msg)
        # cut = size + HEADER_SIZE
        # while len(self.msg) < cut:
            # data = await reader.read(0x1000)
            # self.msg += data

        # data, self.msg = self.msg[4:cut], self.msg[cut:]
        # data = json.decode(data)
        # return data, context

    # async def _send(self, data, writer):
        # msg = bytes(json.encode(data), encoding='UTF-8')
        # msg = struct.pack(HEADER_FORMAT, len(msg)) + msg
        # writer.write(msg)
        # await writer.drain()

    # async def main(self):
        # await self.start()
        # self.channels_ready.set_result(True)
        # while not self.running.done():
            # await asyncio.sleep(1000)
            # message, context = await self._next_message(self.reader, self.writer)
            # self.hande(message, context)

    # def _handle(self, message, context):
        # print(f"receive: {message}")
        # if message == 'quit':
            # self.running.set_result(False)

    # async def start(self):
        # raise NotImplementedError('Must be overriden')


# class UClient(UStreamAgent):
    # """Encapsulate sending objects to UServer"""

    # def __init__(self,  uid=None, realm='', uri='tcp://localhost:9090'):
        # super().__init__(uid, realm, uri)

    # async def start(self):
        # return asyncio.open_connection(*self.address)

    # # async def main(self):
        # # self.running = asyncio.Future()
        # # self.reader, self.writer = await asyncio.open_connection(*self.address)
        # # self.channels_ready.set_result(True)
        # # while not self.running.done():
            # # message = await self._next_message(self.reader, self.writer)
            # # print(f"Server send: {message}")
            # # if message == 'quit':
                # # self.running.set_result(False)

    # async def send(self, data):
        # while not self.channels_ready.done():
            # await asyncio.sleep(0.1)
        # assert self.writer
        # await self._send(data, self.writer)

# class UServer(UStreamAgent):
    # """Give access to exposed methods using TCP as well"""

    # async def start(self):
        # scheme = self._uri.scheme
        # if scheme in ('tcp', ):
            # self.server = await asyncio.start_server(self.tcp_handle, *self.address)
            # # self.reader, self.writer = server.sockets
        # elif scheme in ('udp', ):
            # foo = 1
        # else:
            # raise RuntimeError(f'Unknown scheme {scheme}')


    # async def main(self):
        # self.running = asyncio.Future()
        # async with await asyncio.start_server(self.tcp_handle, *self.address) as server:
            # addr = server.sockets[0].getsockname()
            # print(f'Serving on {addr}: quit to shutdown server')
            # await self.running
        # foo = 1

    # async def tcp_handle(self, reader, writer):
        # addr = writer.get_extra_info('peername')
        # message = f"{addr!r} is connected !!!!"
        # print(message)
        # while not self.running.done():
            # message = await self._next_message(reader, writer)
            # print(f"Client send: {message}")

            # await self._send(message, writer)
            # if message == "exit":
                # message = f"{addr!r} wants to close the connection."
                # print(message)
                # break
            # if message == 'quit':
                # message = f"{addr!r} wants to shutdown the server"
                # self.running.set_result(False)
        # writer.close()

def test_Request():
    uri = 'tl://121212/uagent/dbrecords/foo'
    req = Request(uri)

    foo = 1


def test_parse_uri():
    uri = parse_uri('http://myhost/mypath')
    assert uri['scheme'] == 'http'
    assert uri['fservice'] == 'myhost'
    assert uri['host'] == 'myhost'
    assert uri['path'] == '/mypath'

    uri = parse_uri('http://agp@myhost/mypath')
    assert uri['scheme'] == 'http'
    assert uri['fservice'] == 'agp@myhost'
    assert uri['host'] == 'myhost'
    assert uri['path'] == '/mypath'

    uri = parse_uri('http://agp:mypassword@myhost/mypath')
    assert uri['scheme'] == 'http'
    assert uri['fservice'] == 'agp:mypassword@myhost'
    assert uri['host'] == 'myhost'
    assert uri['path'] == '/mypath'
    assert uri['user'] == 'agp'
    assert uri['password'] == 'mypassword'

    uri = parse_uri('http://agp:mypassword@myhost/mypath?myquery=1#42')
    assert uri['scheme'] == 'http'
    assert uri['fservice'] == 'agp:mypassword@myhost'
    assert uri['host'] == 'myhost'
    assert uri['path'] == '/mypath'
    assert uri['user'] == 'agp'
    assert uri['password'] == 'mypassword'
    assert uri['query'] == 'myquery=1'
    assert uri['fragment'] == '42'

    uri = parse_uri('>http://agp:mypassword@myhost/mypath?myquery=1&foo=3#42')
    assert uri['direction'] == '>'
    assert uri['fscheme'] == '>http'
    assert uri['scheme'] == 'http'
    assert uri['fservice'] == 'agp:mypassword@myhost'
    assert uri['host'] == 'myhost'
    assert uri['path'] == '/mypath'
    assert uri['user'] == 'agp'
    assert uri['password'] == 'mypassword'
    assert uri['query'] == 'myquery=1&foo=3'
    assert uri['fragment'] == '42'

    foo = 1

if __name__ == '__main__':
    test_parse_uri()
    test_Request()
