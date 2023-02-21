from contextlib import contextmanager
from fractions import Fraction
from typing import List

import pytest

from measurements import Format, Measurement


class NullContext:
    """
    No-op context for asserting raised exceptions in parametrized test cases
    """

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, *args, **kwargs):
        pass


does_not_raise = NullContext()


@pytest.mark.parametrize(
    "string, measurement, context",
    [
        ("124", Measurement(inches=124), does_not_raise),
        ('124"', Measurement(inches=124), does_not_raise),
        ("1 13/16", Measurement(inches=1, fraction=Fraction(13 / 16)), does_not_raise),
        ('1 13/16"', Measurement(inches=1, fraction=Fraction(13 / 16)), does_not_raise),
        ("13/16", Measurement(fraction=Fraction(13 / 16)), does_not_raise),
        ('13/16"', Measurement(fraction=Fraction(13 / 16)), does_not_raise),
        (
            '''5' 1 13/16"''',
            Measurement(feet=5, inches=1, fraction=Fraction(13 / 16)),
            does_not_raise,
        ),
        ("6'", Measurement(feet=6), does_not_raise),
        ("6' 3", Measurement(feet=6, inches=3), does_not_raise),
        ("6' 3\"", Measurement(feet=6, inches=3), does_not_raise),
        ('5" 1/2"', None, pytest.raises(ValueError)),
    ],
)
def test_from_string(string: str, measurement: Measurement, context: contextmanager):
    with context:
        assert Measurement.from_string(string) == measurement


@pytest.mark.parametrize(
    "measurement, string",
    [
        (Measurement(inches=18.5, format=Format.inches), '18 1/2"'),
        (Measurement(inches=18.5, format=Format.feet), "1' 6 1/2\""),
        (
            Measurement(inches=18, fraction=Fraction(1, 2), format=Format.inches),
            '18 1/2"',
        ),
        (
            Measurement(inches=18, fraction=Fraction(1, 2), format=Format.feet),
            "1' 6 1/2\"",
        ),
        (
            Measurement(
                feet=1, inches=6, fraction=Fraction(1, 2), format=Format.inches
            ),
            '18 1/2"',
        ),
        (
            Measurement(feet=1, inches=6, fraction=Fraction(1, 2), format=Format.feet),
            "1' 6 1/2\"",
        ),
    ],
)
def test_str(measurement: Measurement, string: str):
    assert str(measurement) == string


@pytest.mark.parametrize(
    "fraction, precision, string, expect",
    [
        (Fraction(53, 64), 64, '53/64"', does_not_raise),
        (Fraction(53, 64), 32, '13/16"', does_not_raise),
        (Fraction(53, 64), 16, '13/16"', does_not_raise),
        (Fraction(53, 64), 8, '7/8"', does_not_raise),
        (Fraction(13, 16), 4, '3/4"', does_not_raise),
        (Fraction(9, 16), 2, '1/2"', does_not_raise),
        (Fraction(13, 16), 1, '1"', does_not_raise),
        (Fraction(1, 2), 65, None, pytest.raises(ValueError)),
        (Fraction(1, 2), 63, None, pytest.raises(ValueError)),
    ],
)
def test_precision(
    fraction: Fraction, precision: int, string: str, expect: contextmanager
):
    with expect:
        assert str(Measurement(fraction=fraction, precision=precision)) == string


@pytest.mark.parametrize(
    "string, factor, expected",
    [
        ("12", 2, Measurement(inches=24)),
        ('13 1/3"', 3, Measurement(inches=40)),
        ("1'", 4, Measurement(inches=48)),
    ],
)
def test_multiply(
    string: str,
    factor: int,
    expected: Measurement,
):
    assert Measurement.from_string(string) * factor == expected


@pytest.mark.parametrize(
    "string, factor, expected",
    [
        ('12"', 2, Measurement(inches=6)),
        ('13"', 3, Measurement(inches=4, fraction=Fraction(1, 3))),
        ("4'", 4, Measurement(feet=1)),
    ],
)
def test_divide(
    string: str,
    factor: int,
    expected: Measurement,
):
    assert Measurement.from_string(string) / factor == expected


def test_example():
    PRECISION: int = 16

    widths: List[str] = ['3 13/32"', '16 48/64"', '16 1/2"', '6 3/4"']
    sum_widths: Measurement = sum(
        [Measurement.from_string(w, precision=PRECISION) for w in widths]
    )
    double_width: Measurement = sum_widths * 2
    assert str(double_width) == '86 13/16"'


def test_string_addition():
    m = Measurement()
    m += '16 1/2"'
    m -= '1 3/16"'
    assert str(m) == '15 5/16"'
