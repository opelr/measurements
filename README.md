# Measurements

Small Python library for performing imperial measurement length calculations,
particularly for carpentry / woodworking projects.

```python
from typing import List

from measurements import Measurement

PRECISION: int = 16


widths: List[str] = ['3 1/2"', '16 1/2"', '16 1/2"', '6 1/2"']
sum_widths: Measurement = sum([Measurement.from_string(w, precision=PRECISION) for w in widths])
double_width: Measurement = sum_widths * 2
print(f"Width: {double_width}")
```
