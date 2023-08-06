"""CalibrationClientApi class"""

from warnings import warn
from .calibration_client import CalibrationClient


class CalibrationClientApi(CalibrationClient):
    """DEPRECATED: use CalibrationClient instead"""
    def __init__(self, *args, **kwargs):
        warn(
            "CalibrationClientApi is deprecated, use CalibrationClient instead",
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
