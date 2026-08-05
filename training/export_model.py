"""
File: training/export_model.py

Description:
Load the trained MCUNet-style checkpoint, export the model to ONNX,
and verify that the exported model produces outputs consistent with
the original PyTorch model.
"""

from pathlib import Path
import sys

import numpy as np
import torch


# ---------------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from train_mcu_net import MCUNet


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RESULTS_DIR = PROJECT_ROOT / "results" / "mcunet"

CHECKPOINT_PATH = RESULTS_DIR / "best_mcunet.pt"
ONNX_PATH = RESULTS_DIR / "mcunet.onnx"

INPUT_SHAPE = (1, 3, 48, 48)

OUTPUT_TOLERANCE = 1e-4


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def load_model() -> tuple[MCUNet, dict]:
    """Load the trained MCUNet model from its checkpoint."""

    if not CHECKPOINT_PATH.exists():
        raise FileNotFoundError(
            f"Checkpoint not found: {CHECKPOINT_PATH}"
        )

    checkpoint = torch.load(
        CHECKPOINT_PATH,
        map_location="cpu",
    )

    class_names = checkpoint.get(
        "class_names",
        ["animal", "empty", "person"],
    )

    dropout = checkpoint.get(
        "dropout",
        0.20,
    )

    image_size = checkpoint.get(
        "image_size",
        48,
    )

    if image_size != INPUT_SHAPE[2]:
        raise ValueError(
            "Checkpoint image size does not match export input size. "
            f"Checkpoint: {image_size}, export: {INPUT_SHAPE[2]}."
        )

    model = MCUNet(
        num_classes=len(class_names),
        dropout=dropout,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model.eval()

    return model, checkpoint


def export_to_onnx(
    model: MCUNet,
    sample_input: torch.Tensor,
) -> None:
    """Export the PyTorch model to ONNX."""

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    torch.onnx.export(
        model,
        (sample_input,),
        ONNX_PATH,
        input_names=["input"],
        output_names=["logits"],
        opset_version=18,
        dynamo=True,
    )


def verify_onnx(
    model: MCUNet,
    sample_input: torch.Tensor,
) -> None:
    """Compare PyTorch and ONNX Runtime outputs."""

    try:
        import onnx
        import onnxruntime as ort

    except ImportError as error:
        raise ImportError(
            "ONNX verification requires 'onnx' and "
            "'onnxruntime'. Install them with:\n"
            "python -m pip install onnx onnxruntime onnxscript"
        ) from error

    onnx_model = onnx.load(ONNX_PATH)
    onnx.checker.check_model(onnx_model)

    with torch.no_grad():
        pytorch_output = model(sample_input).cpu().numpy()

    session = ort.InferenceSession(
        str(ONNX_PATH),
        providers=["CPUExecutionProvider"],
    )

    onnx_output = session.run(
        ["logits"],
        {
            "input": sample_input.cpu().numpy(),
        },
    )[0]

    maximum_difference = float(
        np.max(
            np.abs(
                pytorch_output - onnx_output
            )
        )
    )

    print(
        "Maximum PyTorch/ONNX output difference: "
        f"{maximum_difference:.8f}"
    )

    if not np.allclose(
        pytorch_output,
        onnx_output,
        rtol=OUTPUT_TOLERANCE,
        atol=OUTPUT_TOLERANCE,
    ):
        raise RuntimeError(
            "ONNX verification failed: exported model output "
            "does not sufficiently match the PyTorch output."
        )


# ---------------------------------------------------------------------------
# Main procedure
# ---------------------------------------------------------------------------

def main() -> None:
    """Export and verify the MCUNet model."""

    torch.manual_seed(42)

    model, checkpoint = load_model()

    sample_input = torch.randn(
        *INPUT_SHAPE,
        dtype=torch.float32,
    )

    print("\nMCUNet ONNX export")
    print("=" * 60)
    print(f"Checkpoint: {CHECKPOINT_PATH}")
    print(f"Output: {ONNX_PATH}")
    print(f"Input shape: {INPUT_SHAPE}")
    print(
        "Classes: "
        f"{checkpoint.get('class_names', ['animal', 'empty', 'person'])}"
    )

    export_to_onnx(
        model=model,
        sample_input=sample_input,
    )

    if not ONNX_PATH.exists():
        raise FileNotFoundError(
            f"ONNX export failed: {ONNX_PATH}"
        )

    verify_onnx(
        model=model,
        sample_input=sample_input,
    )

    onnx_size_mb = (
        ONNX_PATH.stat().st_size / (1024 ** 2)
    )

    print("\nExport completed successfully")
    print("-" * 60)
    print(f"ONNX model: {ONNX_PATH}")
    print(f"ONNX size: {onnx_size_mb:.2f} MB")
    print("PyTorch and ONNX outputs are consistent.")


if __name__ == "__main__":
    main()