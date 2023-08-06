# CHIME/FRB Constants

Constants is a is pure-python, lightweight and zero dependency package to access variables used in the CHIME/FRB software projects.

## Installation
```
pip install chime-frb-constants
```

## Optional


## Usage
```python
import chime_frb_constants as constants
print (constants.K_DM)
```

## Changelog

### 2020.07
  - Updated `CHANNEL_BANDWIDTH_MHZ`
  - Fixed errors with `FREQ`
  - Added optional physical constants from `scipy`

### 2020.06.3
  - Fixed error with `CHANNEL_BANDWIDTH_MHZ`
  - Change to `SAMPLING_TIME_MS`
  - New constant `SAMPLING_TIME_S`

### 2020.06.2
  - Added `FREQ` and `FREQ_FREQ`, but with type changes

    ```python
    FREQ: np.array -> FREQ: List[float]
    FPGA_FREQ: np.array -> FPGA_FREQ: List[float]
    ```
### 2020.06
  - Initial release on [PYPI](https://pypi.org/project/chime-frb-constants/)
  - All constants are now uppercase
  - All physical constants from `scipy` are not availaible anymore under constants.
    ```python
    from scipy import constants as phys_const
    ```
  - `FREQ` and `FREQ_FREQ` currently unavailaible.



