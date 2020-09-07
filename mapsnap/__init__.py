#!/usr/bin/env python3

"""
    mapsnap - Apple Maps Web Snapshots on Python

    Generates static maps using Apple's MapKit API

    @author Ygor Lemos <ygbr@mac.com>

    * First you need to convert your .p8 key to a EC PEM format that python-ecdsa can use.
        * You can do that using: #openssl ec -in [PATH_TO_ORIGINAL_KEY.p8] -out [PATH_TO_OUTPUT_PEM_KEY.pem]
        * You need to set the path for this generated .pem on the *_key* parameter
    * Requirements:
        * Python 3.7 or superior
        * ecdsa[gmpy2]
        * requests
    * Official Apple Docs: https://developer.apple.com/documentation/snapshots
"""

__author__ = "Ygor Lemos"
__copyright__ = "Ygor Abreu Lemos 2020"
__contact__ = "ygbr@mac.com"
__email__ = "ygbr@mac.com"
__license__ = "MIT"
__maintainer__ = "Ygor Lemos"
__status__ = "Development"

__version__ = "1.0.0"

import json
from base64 import urlsafe_b64encode
from dataclasses import dataclass, fields
from enum import Enum
from hashlib import sha256
from io import BytesIO
from typing import List, Union
from urllib.parse import urlencode

import requests
from ecdsa import SigningKey, VerifyingKey

from .utils import MapType, ColorScheme, MarkerStyle, Overlay, Image, Annotation


@dataclass
class MapSnap:

    BASE_URL = "https://snapshot.apple-mapkit.com"

    _key: str
    teamId: str
    keyId: str
    center: Union[list, str]
    z: float = None
    spn: str = None
    size: str = None
    scale: int = 2
    t: MapType = None
    colorScheme: ColorScheme = None
    poi: bool = None
    lang: str = "en-US"
    annotations: List[Annotation] = None
    overlays: Union[None, Overlay] = None
    referer: str = None
    expires: int = None
    imgs: List[Image] = None

    def __str__(self):
        """Returns the str representation of the instance as the encoded+signed URL"""

        return self.url

    def __post_init__(self):
        """Initialize, Serialize and Sign"""

        with open(self._key, "rb") as fp:
            self._sk = SigningKey.from_pem(fp.read())

        self._qs = self.serialize()
        self._sig = self.sign()
        self.url = f"{self.BASE_URL}{self._sig}"

    def serialize(self):
        """Serializes all parameters before performing the request"""

        params = {}

        for field in fields(self):
            if field.name.startswith("_"):
                continue

            fval = getattr(self, field.name)
            if fval is not None:
                if isinstance(fval, Enum):
                    fval = fval.value
                elif isinstance(fval, list):
                    if field.name == "annotations":
                        fval = json.dumps([a.serialized for a in fval])
                    else:
                        fval = ",".join([str(v) for v in fval])
                elif isinstance(fval, bool):
                    fval = 1 if fval else 0
                params[field.name] = fval

        return urlencode(params)

    def sign(self):
        """Signs the URI Path + URL-encoded params"""

        complete_path = f"/api/v1/snapshot?{self._qs}"

        sig = self._sk.sign(complete_path.encode(), hashfunc=sha256)

        signature = urlsafe_b64encode(sig).decode().rstrip("=")

        return f"{complete_path}&signature={signature}"

    def png(self):
        """Requests the signed url from Apple and returns a PNG file object"""
        png_file_req = requests.get(self.url, stream=True)

        png_file = BytesIO()

        for chunk in png_file_req.iter_content(chunk_size=128):
            png_file.write(chunk)

        png_file.seek(0)

        return png_file
