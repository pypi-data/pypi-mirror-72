import math
from dataclasses import dataclass
from dataclasses import field
from typing import Optional


KPH_PER_KNOT: float = 463 / 250.0  # Approx 1.852
"""Conversion rate from knots to kilometers per hour."""


def parse_three_digits(digits: str, *, conversion_factor: float = 1.0,
                       degrees: bool = False) -> Optional[float]:
    """Parse three digits from a CourseSpeed-style data extension.

    This may optionally convert the value, if required, given a conversion
    factor. The parsed value will be multiplied by the conversion factor.
    For example, to convert from knots to km/h:

    >>> parse_three_digits("036", conversion_factor=KPH_PER_KNOT)
    66.672

    Special handling can be used for degrees, where 0° is represented on the
    wire as 360:

    >>> parse_three_digits("360", degrees=True)
    0

    If a "placeholder" value is used, then *None* is returned:

    >>> [parse_three_digits(x) for x in ["000", "...", "   "]]
    [None, None, None]

    :param digits: 3 character string to parse
    :param conversion_factor: conversion factor to multiply by
    :param degrees: use special handling for degrees
    """
    if len(digits) != 3:
        raise ValueError(f"expected 3 digits but got {digits}")
    if digits in ["000", "   ", "..."]:
        return None
    if degrees and digits == "360":
        return 0
    else:
        return float(digits) * conversion_factor


def format_three_digits(value: Optional[float], *,
                        conversion_factor: float = 1.0,
                        degrees: bool = False) -> str:
    """Format three digits for a CourseSpeed-style data extension.

    This may optionally convert the value, if required, given a conversion
    factor. The formatted value will have been divided by the conversion
    factor. For example, to convert from km/h to knots:

    >>> format_three_digits(66.672, conversion_factor=KPH_PER_KNOT)
    '036'

    Special handling can be used for degrees, where 0° is represented on the
    wire as 360:

    >>> format_three_digits(0, degrees=True)
    '360'

    If the value is None, then the placehold value of "␣␣␣" (three spaces)
    will be returned.

    >>> format_three_digits(None)
    '   '

    :param value: value to format
    :param conversion_factor: conversion factor to multiply by
    :param degrees: use special handling for degrees
    """
    if value is None:
        return "   "
    if value < 0 or value >= 1000:
        raise ValueError("value out of range, must be 0 ≤ value < 1000, got: "
                         f"{value}")
    elif degrees and value == 0:
        return "360"
    else:
        return f"{value / conversion_factor:03.0f}"


class DataExtension:
    """A generic data extension."""

    def from_content(self, content: str):
        """Create a new data extension from packet content.

        :param content: packet content
        """
        raise NotImplementedError


@dataclass
class CourseSpeed(DataExtension):
    """Course and Speed data extension.

    The 7-byte CSE/SPD Data Extension can be used to represent the course and
    speed of a vehicle, pedestrian or other APRS Object.

    Unit conversion is performed within this class:

    ============= ================ =================
    Property      API Units        Wire Format Units
    ============= ================ =================
    Direction     Degrees          Degrees
    Speed         Kilometers/Hour  Knots
    ============= ================ =================

    In the wire format, the course is expressed in degrees (001-360), clockwise
    from due north. The speed is expressed in knots. Both numbers are right
    justified and padded with leading zeros if necessary. A forward slash
    (ASCII 0x2F) character separates the two numbers.

    While the numbers will always contain 3 digits each, the forward slash may
    be useful to identify this data extension format when used.

    If either the course or speed are unknown, they may be set to "000", "...",
    or "␣␣␣" (three spaces). It would be preferable to avoid the use of "000"
    when sending unknown values, as this has a special meaning in some cases.

    This implementation will use "␣␣␣" for an unknown value.

    For example:

    >>> CourseSpeed.from_content("088/036")
    CourseSpeed(course=88.0, speed=66.672)

    This represents a course of 88 degrees, traveling at 66.6km/h (36 knots).
    To convert to the wire format:

    >>> w = WindDirectionSpeed(88.0, 66.6)
    >>> str(w)
    '088/036'

    :param course: Course as a bearing in degrees.
    :param speed: Speed in kilometers/hour.
    """

    course: Optional[float]
    """Direction as a bearing in degrees."""
    speed: Optional[float]
    """Speed of travel in kilometers/hour."""

    def __str__(self) -> str:
        """Return data extension as a string."""
        return "/".join([
            format_three_digits(self.course, degrees=True),
            format_three_digits(self.speed, conversion_factor=KPH_PER_KNOT),
        ])

    @classmethod
    def from_content(cls, content: str):  # -> DirectionSpeed
        """Create a new data extension from packet content.

        :param content: 7 bytes of packet content containing the data
                        extension.
        :raises ValueError: unable to parse packet content.
        """
        if len(content) != 7 or content[3] != "/":
            return ValueError("Could not parse content. Expected nnn/nnn but "
                              f"got: {content}")
        cse = parse_three_digits(content[0:3], degrees=True)
        spd = parse_three_digits(content[4:8], conversion_factor=KPH_PER_KNOT)
        return cls(cse, spd)


@dataclass
class WindDirectionSpeed(DataExtension):
    """Wind Direction and Wind Speed data extension.

    The 7-byte DIR/SPD Data Extension can be used to represent the
    wind direction and sustained one-minute wind speed. This data extension can
    only appear from stations using the WX symbol. In other cases, this
    extension should be decoded as a CSE/SPD extension instead.

    Unit conversion is performed within this class:

    ============= ================ =================
    Property      API Units        Wire Format Units
    ============= ================ =================
    Direction     Degrees          Degrees
    Speed         Kilometers/Hour  Knots
    ============= ================ =================

    In the wire format, the direction is expressed in degrees (001-360),
    clockwise from due north. The speed is expressed in knots. Both numbers are
    right justified and padded with leading zeros if necessary. A forward slash
    (ASCII 0x2F) character separates the two numbers.

    While the numbers will always contain 3 digits each, the forward slash may
    be useful to identify this data extension format when used.

    If either the direction or speed are unknown, they may be set to "000",
    "...", or "␣␣␣" (three spaces). This implementation will use "␣␣␣" for an
    unknown value.

    For example:

    >>> WindDirectionSpeed.from_content("220/004")
    WindDirectionSpeed(direction=220.0, speed=7.408)

    This represents a wind direction of 220° and a speed of 7.4km/h (4 knots).
    To convert to the wire format:

    >>> w = WindDirectionSpeed(220, 7.4)
    >>> str(w)
    '220/004'

    :param direction: Direction as a bearing in degrees.
    :param speed: Sustained one-minute wind speed in kilometers/hour.
    """

    direction: Optional[float]
    """Direction as a bearing in degrees."""
    speed: Optional[float]
    """Sustained one-minute wind speed in kilometers/hour."""

    def __str__(self) -> str:
        """Return data extension as a string."""
        return "/".join([
            format_three_digits(self.direction, degrees=True),
            format_three_digits(self.speed, conversion_factor=KPH_PER_KNOT),
        ])

    @classmethod
    def from_content(cls, content: str):  # -> DirectionSpeed
        """Create a new data extension from packet content.

        :param content: 7 bytes of packet content containing the data
                        extension
        :raises ValueError: unable to parse packet content
        """
        if len(content) != 7 or content[3] != "/":
            return ValueError("Could not parse content. Expected nnn/nnn but "
                              f"got: {content}")
        direction = parse_three_digits(content[0:3], degrees=True)
        spd = parse_three_digits(content[4:8], conversion_factor=KPH_PER_KNOT)
        return cls(direction, spd)


@dataclass
class DirectionFieldOfView(DataExtension):
    """Camera direction and field of view data extension.

    The 7-byte DIR/FOV data extension can be used to represent the camera
    direction and field of view for an APRN report. This data extension can
    only appear from stations using the SSTV symbol. In other cases, this
    extension should be decoded as a CSE/SPD extension instead.

    No unit conversion is performed in this class, both the API and wire format
    use degrees to represent bearings and angles. A forward slash (ASCII 0x2F)
    character separates the two numbers.

    While the numbers will always contain 3 digits each, the forward slash may
    be useful to identify this data extension format when used.

    If either the direction or field of view are unknown, they may be set to
    "000", "...", or "␣␣␣" (three spaces). This implementation will use "␣␣␣"
    for an unknown value.

    For example:

    >>> DirectionFieldOfView.from_content("053/080")
    DirectionFieldOfView(direction=53.0, fov=80.0)

    This represents a camera direction of 53° and a field of view of 80°. To
    convert to the wire format:

    >>> w = DirectionFieldOfView(53, 80)
    >>> str(w)
    '053/080'

    :param direction: Direction of the camera as a bearing in degrees.
    :param fov: Field-of-view of the camera as an angle in degrees.
    """

    direction: Optional[float]
    """Direction of the camera as a bearing in degrees."""
    fov: Optional[float]
    """Field-of-view of the camera as an angle in degrees."""

    def __str__(self) -> str:
        """Return data extension as a string."""
        return "/".join([
            format_three_digits(x, degrees=True)
            for x in (self.direction, self.fov)
        ])

    @classmethod
    def from_content(cls, content: str):  # -> DirectionSpeed
        """Create a new data extension from packet content.

        :param content: 7 bytes of packet content containing the data
                        extension
        :raises ValueError: unable to parse packet content
        """
        if len(content) != 7 or content[3] != "/":
            return ValueError("Could not parse content. Expected nnn/nnn but "
                              f"got: {content}")
        return cls(parse_three_digits(content[0:3], degrees=True),
                   parse_three_digits(content[4:8], degrees=True))


@dataclass
class PreCalculatedRange(DataExtension):
    """Pre-Calculated Radio Range (RNG) data extension."""

    rng: float
    """Pre-calculated radio range in kilometers (km)."""

    def __str__(self) -> str:
        """Return data extension as a string.

        .. note::

            The wire format for this data extension specifies the range in
            miles. This will be converted automatically.

        .. todo::

           Use constant for conversion.
        """
        return f"RNG{self.rng / 1.609:04.0f}"

    @classmethod
    def from_content(cls, content: str):  # -> PreCalculatedRange
        """Create a new PreCalculatedRange from packet content."""
        if len(content) != 7 or content[0:3].upper() != "RNG":
            return ValueError("Could not parse content. Expected RNGnnnn but "
                              f"got: {content}")
        return cls(float(content[3:8]) * 1.609)


@dataclass
class PowerHeightGain(DataExtension):
    """Power Height Gain (PHG) data extension."""

    power: float
    """Transmitter power output in Watts (W)."""
    height: float
    """Height above average terrain (not above sea level) in meters."""
    gain: float
    """Gain of the antenna in decibels (dB)."""
    directivity: Optional[float] = field(default=None)
    """Direction of the antenna as a bearing in degrees."""

    def range(self) -> float:
        """Calculate the radio range given the power, height and gain values.

        The calculation is based on the one used in [aprs-spec]_ for range
        circle plots. The returned value is in kilometers (km).
        """
        power_ratio = 10**(self.gain / 10)
        return 4.122 * math.sqrt(self.height * math.sqrt(
            (self.power / 10.0) * (power_ratio / 2.0)))

    def precalculate(self) -> PreCalculatedRange:
        """Return a pre-calculated range data extension based on this one."""
        return PreCalculatedRange(self.range())

    def __str__(self) -> str:
        """Return data extension as a string."""
        power = round(math.sqrt(self.power))
        haat = round(math.log2(self.height * 0.328))
        if self.directivity:
            directivity = round(self.directivity / 45.0)
        else:
            directivity = 0
        return f"PHG{power:1.0f}{haat:1.0f}{self.gain:1.0f}{directivity:1.0f}"

    @classmethod
    def from_content(cls, content: str):  # -> PowerHeightGain
        """Create a new PowerHeightGain from packet content."""
        if len(content) != 7 or content[0:3].upper() != "PHG":
            return ValueError("Could not parse content. Expected PHGnnnn but "
                              f"got: {content}.")
        power = float(content[3])**2
        height = 3.048 * 2**float(content[4])
        gain = float(content[5])
        if content[6] == "0":
            directivity = None
        else:
            directivity = float(content[6]) * 45
            if directivity > 360:
                raise ValueError("Incorrect value for directivity. Expected "
                                 "value between 0 and 8 but found: "
                                 f"{content[6]}.")
        return cls(power, height, gain, directivity)
