import re
import sys
import base64
import requests
import logging
from typing import NamedTuple, Union, List
from datetime import datetime

from cli.client import TextToQR, Client
from cli.colors import colored
from cli.ascii_table import print_file_details

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_ascii_qr_code(qr: TextToQR, margin: int = 2) -> List[str]:
    decoded = bytes(base64.b64decode(qr.c)).decode('utf-8')
    binary = ''.join(list(map(lambda b: bin(ord(b)).replace('0b', '').zfill(8), decoded)))
    binary = binary[qr.n0:]

    x = qr.x

    rows = []
    rows.extend(['  ' * (x + margin * 2) for _ in range(margin)])

    for i in range(x):
        row = binary[i * x:(i + 1) * x]
        row = ''.join(list(map(lambda c: '█' * 2 if c == '1' else '  ', row)))
        rows.append(('  ' * margin) + row + ('  ' * margin))

    rows.extend(['  ' * (x + margin * 2) for _ in range(margin)])

    return rows


def main():
    if len(sys.argv) != 2:
        print(f"Usage: qrs <filename>")
        sys.exit(-1)
    client = Client()
    response = client.upload(sys.argv[1])
    download_url = client.get_direct_download_url(response.dir)

    # TODO: generate QR-code locally
    code = generate_ascii_qr_code(client.text_to_qr(download_url))
    for line in code:
        print(colored(line))

    print_file_details(response.filename, response.size, download_url)
    print()


if __name__ == "__main__":
    main()
