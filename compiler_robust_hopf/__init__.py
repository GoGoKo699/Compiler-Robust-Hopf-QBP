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
from .optimal_parallel import (
    OptimalityPlanRow,
    RouteWorkspaceLedger,
    optimality_plan_row,
    route_workspace_ledger,
    tail_block_diagonal_frame,
)

__all__ = [
    "AncillaDepthRow",
    "CheckpointInterfaceSafeExample",
    "CheckpointStateColumnCounterexample",
    "ComplexWorkspaceRow",
    "GlobalStateColumnCounterexample",
    "OptimalityPlanRow",
    "RouteWorkspaceLedger",
    "ancilla_depth_row",
    "complex_frame_matrix",
    "complex_workspace_row",
    "optimality_plan_row",
    "real_frame_matrix",
    "route_workspace_ledger",
    "tail_block_diagonal_frame",
    "two_qubit_checkpoint_interface_safe_example",
    "two_qubit_checkpoint_state_column_counterexample",
    "two_qubit_global_state_column_counterexample",
]

__version__ = "0.1.0a0"
