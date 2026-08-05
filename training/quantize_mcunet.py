"""
File: training/quantize_mcunet.py

Description:
Quantize the exported MCUNet ONNX model to an 8-bit ESP-DL model
for deployment on ESP32-S3.

The script uses:
- the exported ONNX model;
- a calibration dataset taken only from the training split;
- the same resize and ImageNet normalization used during training.

Generated files:
- results/mcunet/mcunet_int8.espdl
- results/mcunet/mcunet_int8.info
- results/mcunet/mcunet_int8.json
"""

from pathlib import Path

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from esp_ppq.api import espdl_quantize_onnx


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ONNX_MODEL_PATH = (
    PROJECT_ROOT
    / "results"
    / "mcunet"
    / "mcunet.onnx"
)

ESPDL_MODEL_PATH = (
    PROJECT_ROOT
    / "results"
    / "mcunet"
    / "mcunet_int8.espdl"
)

CALIBRATION_DIR = (
    PROJECT_ROOT
    / "dataset"
    / "calibration"
)

IMAGE_SIZE = 48

# ESP-PPQ expects the shape without the batch dimension.
INPUT_SHAPE = [3, IMAGE_SIZE, IMAGE_SIZE]

TARGET = "esp32s3"
NUM_OF_BITS = 8
DEVICE = "cpu"

BATCH_SIZE = 1
CALIBRATION_STEPS = 60

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


# ---------------------------------------------------------------------------
# Calibration preprocessing
# ---------------------------------------------------------------------------

calibration_transform = transforms.Compose(
    [
        transforms.Resize(
            (IMAGE_SIZE, IMAGE_SIZE)
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=IMAGENET_MEAN,
            std=IMAGENET_STD,
        ),
    ]
)


def calibration_collate_fn(batch):
    """
    Return only the image tensor.

    ImageFolder returns pairs containing image and class label.
    Quantization calibration requires only the input image.
    """

    images, _ = zip(*batch)

    return torch.stack(images).to(DEVICE)


def create_calibration_loader() -> DataLoader:
    """Create the calibration DataLoader."""

    if not CALIBRATION_DIR.exists():
        raise FileNotFoundError(
            f"Calibration directory not found: {CALIBRATION_DIR}"
        )

    dataset = datasets.ImageFolder(
        root=CALIBRATION_DIR,
        transform=calibration_transform,
    )

    if len(dataset) == 0:
        raise RuntimeError(
            f"No calibration images found in: {CALIBRATION_DIR}"
        )

    if len(dataset) < CALIBRATION_STEPS:
        raise RuntimeError(
            "Not enough calibration images. "
            f"Required: {CALIBRATION_STEPS}, "
            f"available: {len(dataset)}."
        )

    return DataLoader(
        dataset=dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
        collate_fn=calibration_collate_fn,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Quantize the MCUNet ONNX model for ESP32-S3."""

    if not ONNX_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"ONNX model not found: {ONNX_MODEL_PATH}"
        )

    ESPDL_MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    calibration_loader = create_calibration_loader()

    print("\nMCUNet ESP-DL quantization")
    print("=" * 70)
    print(f"ONNX model: {ONNX_MODEL_PATH}")
    print(f"Calibration directory: {CALIBRATION_DIR}")
    print(
        f"Calibration images: "
        f"{len(calibration_loader.dataset)}"
    )
    print(f"Input shape: {INPUT_SHAPE}")
    print(f"Target: {TARGET}")
    print(f"Precision: INT{NUM_OF_BITS}")
    print(f"Device: {DEVICE}")
    print(f"Output: {ESPDL_MODEL_PATH}")
    print("=" * 70)

    espdl_quantize_onnx(
        onnx_import_file=str(ONNX_MODEL_PATH),
        espdl_export_file=str(ESPDL_MODEL_PATH),
        calib_dataloader=calibration_loader,
        calib_steps=CALIBRATION_STEPS,
        input_shape=INPUT_SHAPE,
        inputs=None,
        target=TARGET,
        num_of_bits=NUM_OF_BITS,
        collate_fn=None,
        dispatching_override=None,
        device=DEVICE,
        error_report=True,
        skip_export=False,
        export_test_values=True,
        verbose=1,
    )

    if not ESPDL_MODEL_PATH.exists():
        raise FileNotFoundError(
            "Quantization finished without creating the expected "
            f"ESP-DL model: {ESPDL_MODEL_PATH}"
        )

    model_size_kb = (
        ESPDL_MODEL_PATH.stat().st_size / 1024
    )

    print("\nQuantization completed successfully")
    print("-" * 70)
    print(f"ESP-DL model: {ESPDL_MODEL_PATH}")
    print(f"Model size: {model_size_kb:.2f} KB")

    print("\nGenerated companion files")
    print("-" * 70)

    for extension in (".info", ".json"):
        companion_path = (
            ESPDL_MODEL_PATH.with_suffix(extension)
        )

        if companion_path.exists():
            print(companion_path)
        else:
            print(
                f"Not found: {companion_path}"
            )


if __name__ == "__main__":
    main()
    