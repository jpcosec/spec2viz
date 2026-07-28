import warnings

warnings.warn(
    "The 'yaml_charts' package is deprecated and has been renamed to 'spec2viz'. "
    "Please update your imports to use 'spec2viz' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Export everything from spec2viz so it acts as a drop-in replacement if needed
from spec2viz import *
