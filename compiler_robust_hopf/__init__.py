"""Compiler-robust Hopf differential-frame research utilities."""

from .ancilla_depth import AncillaDepthRow, ancilla_depth_row
from .compiler_boundaries import (
    CheckpointInterfaceSafeExample,
    CheckpointStateColumnCounterexample,
    GlobalStateColumnCounterexample,
    two_qubit_checkpoint_interface_safe_example,
    two_qubit_checkpoint_state_column_counterexample,
    two_qubit_global_state_column_counterexample,
)
from .complex_resources import ComplexWorkspaceRow, complex_workspace_row
from .frames import complex_frame_matrix, real_frame_matrix

__all__ = [
    "AncillaDepthRow",
    "CheckpointInterfaceSafeExample",
    "CheckpointStateColumnCounterexample",
    "ComplexWorkspaceRow",
    "GlobalStateColumnCounterexample",
    "ancilla_depth_row",
    "complex_frame_matrix",
    "complex_workspace_row",
    "real_frame_matrix",
    "two_qubit_checkpoint_interface_safe_example",
    "two_qubit_checkpoint_state_column_counterexample",
    "two_qubit_global_state_column_counterexample",
]

__version__ = "0.1.0a0"
