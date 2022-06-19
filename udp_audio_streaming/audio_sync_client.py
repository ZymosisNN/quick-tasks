import logging
import socket
import sys
from pathlib import Path
from time import sleep

ADDR = '127.0.0.1', 9999
SRC_DIR = Path(__file__).parent / 'waves_client'
UDP_MAX_SIZE = 65507
MTU_MINUS_UDP_HEADER = 1432


def send_wave():
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
        sock.connect(ADDR)
        logging.info(sock.getsockname())

        with open(SRC_DIR / '01.wav', 'rb') as wav:
            data = wav.read()

        for i, chunk in enumerate(to_chunks(data)):
            logging.info(f'Send chunk #{i}')
            sock.sendall(chunk)
            sleep(.03)  # Server input buffer overflow protection


def to_chunks(data: bytes, size=UDP_MAX_SIZE):
    return [data[i: i + size] for i in range(0, len(data), size)]


# def make_data() -> bytes:
#     from itertools import cycle
#     value_gen = cycle(range(255))
#     size = 65536 * 7
#     return bytes(next(value_gen) for _ in range(size))


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout,
                        format='%(asctime)-15s  |%(levelname)+8s| %(name)+30s |  %(message)s')
    send_wave()
