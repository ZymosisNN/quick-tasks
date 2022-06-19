import asyncio
import logging
import sys
from asyncio import transports
from pathlib import Path

from log_mixin import LogMixin

ADDR = '127.0.0.1', 9999
SRC_DIR = Path(__file__).parent / 'waves_client'
UDP_MAX_SIZE = 65507


class UdpClient(LogMixin):
    def __init__(self, dst_addr: tuple[str, int]):
        super().__init__()
        self.dst_addr = dst_addr

    async def send(self, wave_filename: str):
        with open(SRC_DIR / wave_filename, 'rb') as wav:
            data = wav.read()

        loop = asyncio.get_running_loop()
        on_con_lost = loop.create_future()

        self.log.info('Create transport')
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UdpDataSender(on_con_lost),
            remote_addr=self.dst_addr
        )

        self.log.info(f'Send {wave_filename}')
        await protocol.send_bytes(data)
        self.log.info('Close transport')
        transport.close()

        try:
            await on_con_lost
        finally:
            transport.close()
        self.log.info(f'Sent {wave_filename}')


class UdpDataSender(asyncio.DatagramProtocol, LogMixin):
    transport: transports.DatagramTransport = None

    def __init__(self, on_con_lost: asyncio.Future):
        LogMixin.__init__(self)
        self.on_con_lost = on_con_lost

    async def send_bytes(self, data: bytes):
        self.log.debug('Sending...')
        for i, chunk in enumerate(to_chunks(data)):
            self.log.info(f'Send chunk #{i}')
            self.transport.sendto(chunk)
            await asyncio.sleep(.03)  # Server input buffer stupid overflow protection

        self.log.debug('All sent')

    def connection_made(self, transport: transports.DatagramTransport) -> None:
        self.log.debug('connection_made')
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        self.log.debug(f'datagram_received: {data.decode()}, close socket')
        self.transport.close()

    def error_received(self, exc: Exception) -> None:
        self.log.error(f'error_received: {exc}')

    def connection_lost(self, exc) -> None:
        self.log.debug('connection_lost')
        self.on_con_lost.set_result(True)

    def pause_writing(self) -> None:  # TODO: use it for overload protection?
        self.log.debug('pause_writing')

    def resume_writing(self) -> None:  # TODO: use it for overload protection?
        self.log.debug('resume_writing')


def to_chunks(data: bytes, size=UDP_MAX_SIZE) -> list[bytes]:
    return [data[i: i + size] for i in range(0, len(data), size)]


# def make_data() -> bytes:
#     from itertools import cycle
#     value_gen = cycle(range(255))
#     size = 65536 * 7
#     return bytes(next(value_gen) for _ in range(size))


async def main():
    client = UdpClient(dst_addr=ADDR)
    tasks = [asyncio.create_task(client.send(wave_filename=f'{i:02d}.wav'))
             for i in range(1, 4)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout,
                        format='%(asctime)-15s  |%(levelname)+8s| %(name)+30s |  %(message)s')
    asyncio.run(main())
