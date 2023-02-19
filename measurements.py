from fractions import Fraction
from numbers import Real
from typing import List, Union


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
    def from_string(
        cls, string: str, *, format: str = "inches", precision: int = 64
    ) -> "Measurement":
        parts: List[str] = string.split(" ")

        if len(parts) == 3:
            feet, inches, frac = [i.replace('"', "").replace("'", "") for i in parts]
            return cls(
                feet=int(feet),
                inches=int(inches),
                fraction=Fraction(frac),
                format=format,
                precision=precision,
            )

        if len(parts) == 2:
            first, second = parts

            if "'" in first:
                feet = int(first.replace("'", ""))
                if "/" in second:
                    return cls(
                        feet=feet,
                        fraction=Fraction(second.replace('"', "")),
                    )

                return cls(
                    feet=feet,
                    inches=int(second.replace('"', "")),
                    format=format,
                    precision=precision,
                )

            return cls(
                inches=int(first),
                fraction=Fraction(second.replace('"', "")),
                format=format,
                precision=precision,
            )

        if len(parts) == 1:
            distance: str = parts[0]
            if "'" in distance:
                return cls(
                    feet=int(distance.replace("'", "")),
                    format=format,
                    precision=precision,
                )

            if "/" in distance:
                return cls(
                    fraction=Fraction(distance.replace('"', "")),
                    format=format,
                    precision=precision,
                )

            return cls(
                inches=int(distance.replace('"', "")),
                format=format,
                precision=precision,
            )

        raise ValueError(f"Cannot parse {string} as Measurement")

    def __add__(self, other: Union["Measurement", Real]) -> "Measurement":
        if type(other) is Measurement:
            return Measurement(
                self._distance + other._distance,
                precision=max(self._precision, other._precision),
            )

        return Measurement(self._distance + other)

    def __sub__(self, other: Union["Measurement", Real]) -> "Measurement":
        if type(other) is Measurement:
            return Measurement(
                self._distance - other._distance,
                precision=max(self._precision, other._precision),
            )

        return Measurement(self._distance - other)

    def __mul__(self, factor: int) -> "Measurement":
        return Measurement(self._distance * factor, precision=self._precision)

    def __truediv__(self, factor: int) -> "Measurement":
        return Measurement(self._distance / factor, precision=self._precision)

    def __radd__(self, other):
        return self + other

    def __eq__(self, other: Union["Measurement", Real]):
        if type(other) is Measurement:
            return self._distance == other._distance

        return self._distance == other

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
