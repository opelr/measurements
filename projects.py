from typing import List

from measurements import Measurement

PRECISION: int = 16


def existing_nursery_builtin() -> None:
    heights: List[str] = ['2"', '52 1/4"', '3/4"', '2"', '12"']
    widths: List[str] = ['3 1/2"', '16 1/2"', '16 1/2"', '6 1/2"']

    total_height: Measurement = sum(
        [Measurement.from_string(h, precision=PRECISION) for h in heights]
    )
    total_width: Measurement = sum(
        [Measurement.from_string(w, precision=PRECISION) for w in widths]
    )

    print(f"Height: {total_height}")
    print(f"Width: {total_width}")


def door_height() -> None:
    height = Measurement.from_string('23 43/64"', precision=PRECISION)
    print(f"Mid-Point: {height / 2}")


def left_panels() -> None:
    stile = Measurement.from_string('52 1/4"')
    h = stile - (Measurement.from_string('2 1/2"') * 5)
    h = h + (Measurement.from_string('3/8"') * 8)
    height = h / 4
    print(f"Left Panel: {height}H")


def right_panels() -> None:
    stile = Measurement.from_string('52 1/2"')
    h = stile - (Measurement.from_string('2 1/2"') * 5)
    h = h + (Measurement.from_string('3/8"') * 8)
    height = h / 4
    print(f"Right Panel: {height}H")


def rail_width(total_width: str) -> None:
    m = Measurement.from_string(total_width)
    rail = (m / 2) - 5 - '1/16"' + '6/8"'
    print(f"Rail width: {rail}")


if __name__ == "__main__":
    # existing_nursery_builtin()
    # door_height()
    left_panels()
    right_panels()

    rail_width('36 3/8"')
    rail_width('36 5/8"')
