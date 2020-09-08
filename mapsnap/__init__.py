#!/usr/bin/env python3

"""
    mapsnap - Apple Maps Web Snapshots on Python

    Generates static maps using Apple's MapKit API

    Check the docs at: https://mapsnap.ygor.dev

"""

__title__ = "mapsnap"
__description__ = "Apple Maps Web Snapshots on Python"
__url__ = "https://mapsnap.ygor.dev"
__author__ = "Ygor Lemos"
__copyright__ = "2020 Ygor Lemos"
__contact__ = "ygbr@mac.com"
__email__ = "ygbr@mac.com"
__license__ = "MIT"
__status__ = "Development"

__version__ = "1.0.1"

import json
from base64 import urlsafe_b64encode
from dataclasses import dataclass, fields
from enum import Enum
from hashlib import sha256
from io import BytesIO
from typing import List, Union
from urllib.parse import urlencode

import requests
from ecdsa import SigningKey

from .utils import (  # noqa: F401
    Annotation,
    ColorScheme,
    Image,
    MapType,
    MarkerStyle,
    Overlay,
)


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

        if isinstance(self._key, bytes):
            self._sk = SigningKey.from_pem(self._key)
        elif isinstance(self._key, str):
            with open(self._key, "rb") as fp:
                self._sk = SigningKey.from_pem(fp.read())
        else:
            raise ValueError(
                "_key must be a str with the path or a bytes object with the raw key"
            )

        self._qs = self.serialize()
        self._sig = self.sign()

        del self._sk
        self._key = None
        self.teamId = None
        self.keyId = None

        self.url = f"{self.BASE_URL}{self._sig}"

        del self._sig

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
