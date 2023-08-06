import warnings
from autodl.__version__ import __version__, __version_suffix__

name = "autodl"
version = __version__

# Suppress warnings from skopt using deprecated sklearn API
warnings.filterwarnings(
    "ignore", category=FutureWarning
)