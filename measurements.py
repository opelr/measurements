import re
from fractions import Fraction
from numbers import Real
from typing import Optional, Union


REGEX = re.compile(
    r"((?P<feet>[0-9]+)\' )?((?P<inches>[0-9]+)\"?) ?((?P<frac_num>[0-9]+)\/(?P<frac_denom>[0-9]+)\"?)?"
)


class Measurement:
    __slots__ = ["_distance", "_precision", "_format"]

    def __init__(
        self,
        inches: Real = None,
        fraction: Real = None,
        *,
        feet: int = None,
        format: str = "inches",
        precision: int = 64,
    ) -> None:
        if feet is None:
            feet = 0

        if inches is None:
            inches = 0

        if fraction is None:
            fraction = Fraction()
        elif type(fraction) is float:
            fraction = Fraction(fraction)

        self._distance: float = (feet * 12) + inches + fraction
        self._precision = precision

        if format not in ["inches", "feet"]:
            raise ValueError("'format' must be 'inches' or 'feet'")
        self._format = format

    @classmethod
    def from_string(cls, string, *, precision: int = 64) -> None:
        def to_int(x: Optional[str]) -> Optional[int]:
            if x is None:
                return x

            return int(x)

        matches = REGEX.search(string)
        feet: Optional[int] = to_int(matches.group("feet"))
        inches: Optional[int] = to_int(matches.group("inches"))
        frac_num: Optional[int] = to_int(matches.group("frac_num"))
        frac_denom: Optional[int] = to_int(matches.group("frac_denom"))

        fraction = None
        if frac_num is not None and frac_denom is not None:
            fraction = Fraction(frac_num, frac_denom)

        return cls(
            inches=inches,
            fraction=fraction,
            feet=feet,
            precision=precision,
        )

    def __add__(self, other: Union["Measurement", Real]) -> "Measurement":
        if type(other) is Measurement:
            return Measurement(
                self._distance + other._distance,
                precision=max(self._precision, other._precision),
            )

        return Measurement(self._distance + other)

    def __mul__(self, factor: int) -> "Measurement":
        return Measurement(self._distance * factor, precision=self._precision)

    def __radd__(self, other):
        return self + other

    def __str__(self) -> str:
        feet = int()
        inches = int()

        if self._format == "feet":
            feet = int(self._distance // 12)
            inches = int(self._distance % 12 // 1)
        else:
            inches = int(self._distance // 1)

        raw_fraction = Fraction(self._distance % 1)
        fraction = Fraction(int(round(self._precision * raw_fraction)), self._precision)

        output: str = ""
        if feet:
            output += f"{feet}'"

        output: str = ""
        if inches and fraction:
            output = f'{inches} {fraction}"'
        elif inches:
            output = f'{inches}"'
        elif fraction:
            output = f'{fraction}"'

        if feet:
            output = f"{feet}' {output}"

        return output

    def __repr__(self) -> str:
        return f"Measurement({str(self)})"
