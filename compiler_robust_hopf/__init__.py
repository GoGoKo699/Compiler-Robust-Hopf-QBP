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
    tail_block_diagonal_frame as legacy_tail_block_diagonal_frame,
)
from .tree_decoder import (
    ConditionedPrefixResourceRow,
    ReversibleGate,
    TreeDecoderLayout,
    TreeDecoderResourceRow,
    binary_to_unary_operations,
    conditioned_prefix_resource_row,
    tree_decoder_resource_row,
    unary_hopf_code_action,
)
from .tree_structure import (
    conditioned_prefix_frame,
    tail_block_diagonal_frame,
)
from .unified_compiler import (
    DiagonalUCGResourceRow,
    DirectFrameResourceRow,
    RouteWorkspaceRow,
    UnifiedComplexResourceRow,
    UnifiedFrameResourceRow,
    diagonal_ucg_matrix,
    unified_complex_frame_resource_row,
    unified_real_frame_resource_row,
)

__all__ = [
    "AncillaDepthRow",
    "CheckpointInterfaceSafeExample",
    "CheckpointStateColumnCounterexample",
    "ComplexWorkspaceRow",
    "ConditionedPrefixResourceRow",
    "DiagonalUCGResourceRow",
    "DirectFrameResourceRow",
    "GlobalStateColumnCounterexample",
    "OptimalityPlanRow",
    "ReversibleGate",
    "RouteWorkspaceLedger",
    "RouteWorkspaceRow",
    "TreeDecoderLayout",
    "TreeDecoderResourceRow",
    "UnifiedComplexResourceRow",
    "UnifiedFrameResourceRow",
    "ancilla_depth_row",
    "binary_to_unary_operations",
    "complex_frame_matrix",
    "complex_workspace_row",
    "conditioned_prefix_frame",
    "conditioned_prefix_resource_row",
    "diagonal_ucg_matrix",
    "legacy_tail_block_diagonal_frame",
    "optimality_plan_row",
    "real_frame_matrix",
    "route_workspace_ledger",
    "tail_block_diagonal_frame",
    "tree_decoder_resource_row",
    "two_qubit_checkpoint_interface_safe_example",
    "two_qubit_checkpoint_state_column_counterexample",
    "two_qubit_global_state_column_counterexample",
    "unary_hopf_code_action",
    "unified_complex_frame_resource_row",
    "unified_real_frame_resource_row",
]

__version__ = "0.2.0a0"
