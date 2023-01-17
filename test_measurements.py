from fractions import Fraction

import pytest

from measurements import Measurement


@pytest.mark.parametrize(
    "string, measurement",
    [
        ("124", Measurement(inches=124)),
        ('124"', Measurement(inches=124)),
        ("1 13/16", Measurement(inches=1, fraction=Fraction(13 / 16))),
        ('1 13/16"', Measurement(inches=1, fraction=Fraction(13 / 16))),
        ("13/16", Measurement(fraction=Fraction(13 / 16))),
        ('13/16"', Measurement(fraction=Fraction(13 / 16))),
        ('''5' 1 13/16"''', Measurement(feet=5, inches=1, fraction=Fraction(13 / 16))),
        ("6'", Measurement(feet=6)),
        ("6' 3", Measurement(feet=6, inches=3)),
        ("6' 3\"", Measurement(feet=6, inches=3)),
        pytest.param('5" 1/2"', None, marks=pytest.mark.xfail),
    ],
)
def test_from_string(string: str, measurement: Measurement):
    assert Measurement.from_string(string) == measurement


@pytest.mark.parametrize(
    "measurement, string",
    [
        (Measurement(inches=18.5, format="inches"), '18 1/2"'),
        (Measurement(inches=18.5, format="feet"), "1' 6 1/2\""),
        (Measurement(inches=18, fraction=Fraction(1, 2), format="inches"), '18 1/2"'),
        (Measurement(inches=18, fraction=Fraction(1, 2), format="feet"), "1' 6 1/2\""),
        (
            Measurement(feet=1, inches=6, fraction=Fraction(1, 2), format="inches"),
            '18 1/2"',
        ),
        (
            Measurement(feet=1, inches=6, fraction=Fraction(1, 2), format="feet"),
            "1' 6 1/2\"",
        ),
    ],
)
def test_str(measurement: Measurement, string: str):
    assert str(measurement) == string


@pytest.mark.parametrize(
    "precision, string",
    [
        (64, '51/64"'),
        (32, '13/16"'),
        (16, '13/16"'),
        (8, '3/4"'),
        (4, '3/4"'),
        (2, '1"'),
    ],
)
def test_precision(precision: int, string: str):
    assert str(Measurement(fraction=Fraction(51, 64), precision=precision)) == string
