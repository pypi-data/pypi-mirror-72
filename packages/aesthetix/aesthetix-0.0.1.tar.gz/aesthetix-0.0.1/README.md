# Aesthetix

This is a python package which facilitates aesthetics in output when using custom training pipelines in machine learning.

## Usage Example

```python
import time
import aesthetix as at

cost  = 3000
acc = 0.9
for i in range(1000):
    at.progress_bar("Progress",i, 1000, num_bars = 40, output_vals={"Cost":cost, "Accuracy":acc})
    cost/=3
    acc *= 1.001
    time.sleep(0.01)
```

### Output

```txt
Progress:[========================================](100.00%)  Cost : 0.00 Accuracy : 2.44
```
