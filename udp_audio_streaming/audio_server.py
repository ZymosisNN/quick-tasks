import asyncio
import logging
import sys
from asyncio import transports
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from log_mixin import LogMixin

ADDR = '127.0.0.1', 9999
RECV_DIR = Path(__file__).parent / 'waves_server'
TIMESTAMP_FMT = '%Y-%m-%d__%H-%M-%S-%f'


class UdpServer(LogMixin):
    async def run(self, duration: int = None):
        self.log.info('Starting UDP server')
        loop = asyncio.get_event_loop()
        transport, protocol = await loop.create_datagram_endpoint(UdpHandler, local_addr=ADDR)
        try:
            await asyncio.sleep(duration or 3600)
        finally:
            transport.close()


class UdpHandler(asyncio.DatagramProtocol, LogMixin):
    # transport: transports.DatagramTransport = None

    def __init__(self):
        LogMixin.__init__(self)
        self.connections: dict[str, ConnectionData] = {}

    def connection_made(self, transport: transports.DatagramTransport) -> None:
        self.log.debug('connection_made')
        # self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        self.log.info(f'datagram_received from {addr}')

        key = f'{addr[0]}:{addr[1]}'
        if key not in self.connections:
            self.connections[key] = ConnectionData(*addr)
            self.log.debug(f'    NEW ---> {self.connections[key]}')
        else:
            # TODO: add time check for old connections with the same host:port
            self.connections[key].counter += 1
            self.log.debug(f'    ---> {self.connections[key]}')

        c = self.connections[key]
        filename = f'{c.creation_time.strftime(TIMESTAMP_FMT)}__{c.ip}_{c.port}.wav'

        # TODO: better to do it via factory
        with open(RECV_DIR / filename, 'ab') as file:
            file.write(data)

    # def error_received(self, exc: Exception) -> None:
    #     self.log.error(f'error_received: {exc}')
    #
    # def connection_lost(self, exc) -> None:
    #     self.log.debug('connection_lost')
    #
    # def pause_writing(self) -> None:  # TODO: use it for overload protection?
    #     self.log.debug('pause_writing')
    #
    # def resume_writing(self) -> None:  # TODO: use it for overload protection?
    #     self.log.debug('resume_writing')


@dataclass
class ConnectionData:
    ip: str
    port: int
    counter: int = 0
    creation_time: datetime = None

    def __post_init__(self):
        self.creation_time = datetime.now()

    def __str__(self):
        return f'{self.creation_time.strftime(TIMESTAMP_FMT)}  [{self.counter}]'


async def run_server():
    await UdpServer().run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout,
                        format='%(asctime)-15s  |%(levelname)+8s| %(name)+30s |  %(message)s')
    asyncio.run(run_server())
