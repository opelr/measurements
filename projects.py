from measurements import Measurement

PRECISION: int = 16


def existing_nursery_builtin() -> None:
    heights = ['2"', '52 1/4"', '3/4"', '2"', '12"']
    widths = ['3 1/2"', '16 1/2"', '16 1/2"', '6 1/2"']

    total_height = sum(
        [Measurement.from_string(h, precision=PRECISION) for h in heights]
    )
    total_width = sum([Measurement.from_string(w, precision=PRECISION) for w in widths])

    print(f"Height: {total_height}")
    print(f"Width: {total_width}")


if __name__ == "__main__":
    existing_nursery_builtin()
