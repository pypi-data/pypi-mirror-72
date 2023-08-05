# CHIME/FRB Constants

Constants is a is pure-python, lightweight and zero dependency package to access variables used in the CHIME/FRB software projects.

## Installation
```
pip install chime-frb-constants
```

## Usage
```python
import chime_frb_constants as constants
print (constants.K_DM)
```

## Changelog
### 2020.06.2
  - `FREQ` and `FREQ_FREQ` availaible once again, but with type changes
    ```python
    FREQ: np.array -> FREQ: List[float]
    FPGA_FREQ: np.array -> FPGA_FREQ: List[float]
    ```
### 2020.06
  - Initial release on [PYPI](https://pypi.org/project/chime-frb-constants/)
  - All constants are now uppercase
  - All physical constants from `scipy` are not availaible anymore under constants. If you still need them, import them directly from
    ```python
    from scipy import constants as phys_const
    ```
  - `FREQ` and `FREQ_FREQ` currently unavailaible.



