"""Compiler-robust Hopf differential-frame research utilities."""

from .ancilla_depth import AncillaDepthRow, ancilla_depth_row
from .frames import complex_frame_matrix, real_frame_matrix

__all__ = [
    "AncillaDepthRow",
    "ancilla_depth_row",
    "complex_frame_matrix",
    "real_frame_matrix",
]

__version__ = "0.1.0a0"
