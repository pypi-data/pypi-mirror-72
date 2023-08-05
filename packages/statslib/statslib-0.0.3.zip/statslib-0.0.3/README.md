git clone https://github.com/aforren1/pystatslib --recursive

Example usage:

```python
import statslib as sl
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

x = np.linspace(-3, 3, num=100)
y = sl.dnorm(x, mu=0, sigma=1, log=False)
y2 = norm.pdf(x, loc=0, scale=1)

plt.plot(x, y - y2)
plt.show()
```
