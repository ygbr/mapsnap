from dataclasses import dataclass, fields
from enum import Enum
from typing import List, Union


class MapType(Enum):
    STANDARD = "standard"
    HYBRID = "hybrid"
    SATELLITE = "satellite"
    MUTEDSTANDARD = "mutedStandard"


class ColorScheme(Enum):
    LIGHT = "light"
    DARK = "dark"


class MarkerStyle(Enum):
    DOT = "dot"
    BALLOON = "balloon"
    LARGE = "large"
    IMG = "img"


@dataclass
class Overlay:
    points: List[str]
    strokeColor: str
    lineWidth: int
    lineDash: Union[None, List[int]]


@dataclass
class Image:
    height: int
    url: str
    width: int


@dataclass
class Annotation:

    color: str = None
    glyphText: str = None
    markerStyle: MarkerStyle = MarkerStyle.BALLOON
    point: str = "center"
    imgIdx: int = None
    offset: str = None

    def __post_init__(self):
        self.serialized = self.serialize()

    def serialize(self):
        params = {}

        for field in fields(self):
            fval = getattr(self, field.name)
            if fval is not None:
                if isinstance(fval, Enum):
                    fval = fval.value
                elif isinstance(fval, list):
                    fval = ",".join([str(v) for v in fval])
                elif isinstance(fval, bool):
                    fval = 1 if fval else 0
                params[field.name] = fval

        return params
