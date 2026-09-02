"""Compiler-robust Hopf differential-frame research utilities."""

from .ancilla_depth import AncillaDepthRow, ancilla_depth_row
from .complex_analysis import (
    complex_magnitude_gradient,
    complex_phase_gradient,
    complex_state,
    diagonal_parity_angles,
)
from .complex_resources import (
    ComplexWorkspaceRow,
    DiagonalSynthesisRow,
    complex_workspace_row,
    diagonal_synthesis_row,
)
from .frames import complex_frame_matrix, real_frame_matrix

__all__ = [
    "AncillaDepthRow",
    "ComplexWorkspaceRow",
    "DiagonalSynthesisRow",
    "ancilla_depth_row",
    "complex_frame_matrix",
    "complex_magnitude_gradient",
    "complex_phase_gradient",
    "complex_state",
    "complex_workspace_row",
    "diagonal_parity_angles",
    "diagonal_synthesis_row",
    "real_frame_matrix",
]

__version__ = "0.2.0a0"
