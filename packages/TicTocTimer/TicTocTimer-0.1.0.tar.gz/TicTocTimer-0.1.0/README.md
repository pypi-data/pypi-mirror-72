# TicTocTimer

A very simple and easy to use implementation of timer object for python code, based on the tic/toc matlab syntax.

## Using the common timer

Using the `global` name label,

```python
import time
from tic_toc_timer import tic, toc

tic()
time.sleep(10)
print(f"The total time elasped is {toc()}")
```

Using a custom label(s),

```python
import time
from tic_toc_timer import tic, toc

tic("first")
time.sleep(10)
tic("second")
time.sleep(1)

first_elapsed = toc("first")  # expected ~ 11 secs
second_elapsed = toc("second")  # expected ~ 1 sec
```

## Using a local timer

```python
import time
from tic_toc_timer import TicTocTimer

timer = TicTocTimer()

timer.tic("first")
time.sleep(10)
timer.tic("second")
time.sleep(1)

first_elapsed = timer.toc("first")  # expected ~ 11 secs
second_elapsed = timer.toc("second")  # expected ~ 1 sec
```

# Install (for now, directly from the git repo)

To install from master branch,

```shell
pip install git+https://github.com/LamaAni/TicTocTimer.git@master
```

To install from a release (tag)

```shell
pip install git+https://github.com/LamaAni/TicTocTimer.git@[tag]
```

# Contribution

Feel free to ping me in issues or directly on LinkedIn to contribute.

# Licence

Copyright ©
`Zav Shotan` and other [contributors](https://github.com/LamaAni/postgres-xl-helm/graphs/contributors).
It is free software, released under the MIT licence, and may be redistributed under the terms specified in `LICENSE`.