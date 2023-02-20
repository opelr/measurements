# Measurements

Small Python library for performing imperial measurement length calculations,
particularly for carpentry / woodworking projects.

## Features

* Supports feet, inches, and inch fractions
* Addition, multiplication, and division of measurements
* Rounding to common inch divisions (e.g. 1/4, 1/8, 1/16, etc.)

## Example

```python
from typing import List

from measurements import Measurement

PRECISION: int = 16


widths: List[str] = ['3 13/32"', '16 49/64"', '16 1/2"', '6 3/4"']
sum_widths: Measurement = sum([Measurement.from_string(w, precision=PRECISION) for w in widths])
double_width: Measurement = sum_widths * 2
print(f"Width: {double_width}")
# > Width: 86 13/16"
```

## Recommended Resources

* [Cut List Optimizer](https://www.cutlistoptimizer.com/)
