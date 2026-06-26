# Smart Visual Alarm System for Mountain House Monitoring

## Project Overview

This project aims to develop a smart visual alarm system for monitoring a mountain house environment. The system is designed to detect relevant visual events near the entrance or outdoor area of the house, where people or animals may pass, also during evening or night hours.

The system is based on an embedded camera node and an IoT backend. The camera node acquires images from the monitored area and performs visual classification. When a relevant event is detected, an MQTT message is sent to a Raspberry Pi, which logs the event and forwards a notification to the user through a Telegram bot.

The main goal is not only to implement a working alarm system, but also to evaluate lightweight neural network models suitable for visual classification in resource-constrained IoT scenarios.

## Target Scenario

The project is applied to a real-world mountain house scenario. The monitored area may contain:

- an empty scene;
- a person passing near the house;
- a generic animal passing near the house.

The objective is not to recognize the animal species, but to distinguish between the main classes relevant for the alarm system.

## Target Classes

The classification task is based on three classes:

| Class | Description |
|---|---|
| `empty` | No relevant subject is visible |
| `person` | At least one person is visible |
| `animal` | At least one generic animal is visible |

## System Architecture

The system follows this pipeline:

```text
ESP32-S3-EYE
    ↓
Image acquisition and visual classification
    ↓
MQTT event publishing
    ↓
Raspberry Pi MQTT broker
    ↓
Python backend
    ↓
Event logging and Telegram notification
````

The ESP32-S3-EYE acts as the camera node, while the Raspberry Pi is used as the IoT gateway. The Raspberry Pi runs the MQTT broker, receives alarm events, stores logs, and sends notifications to Telegram.

## Hardware Components

| Component                         | Role                                                        |
| --------------------------------- | ----------------------------------------------------------- |
| ESP32-S3-EYE                      | Camera node for image acquisition and visual classification |
| Raspberry Pi 4 / Raspberry Pi 400 | MQTT broker, Python backend, event logging, Telegram bot    |
| microSD card                      | Raspberry Pi OS and project files                           |
| USB-C data cable                  | Programming and powering the ESP32-S3-EYE                   |
| Camera support / tripod           | Positioning the camera toward the monitored area            |
| Automatic external light          | Helps image acquisition in evening/night conditions         |

## Software Components

| Software          | Purpose                                          |
| ----------------- | ------------------------------------------------ |
| Python            | Training, backend, data processing               |
| PyTorch           | Training and evaluation of neural network models |
| Mosquitto         | MQTT broker running on Raspberry Pi              |
| paho-mqtt         | Python MQTT client                               |
| Telegram Bot API  | Remote alert notification                        |
| ESP-IDF / ESP-WHO | ESP32-S3-EYE firmware development                |
| GitHub            | Version control and project documentation        |

## Neural Network Models

The project evaluates different lightweight neural network architectures for the visual classification task:

1. **Small CNN / MLP baseline**
   A simple lightweight model used as a baseline for comparison.

2. **MCUNet**
   A TinyML-oriented architecture designed for microcontroller-level deployment.

3. **TinyViT**
   A lightweight vision transformer model used as a more modern architecture for comparison.

All models are trained and evaluated on the same dataset using the same target classes.

## Dataset Structure

The dataset is organized as follows:

```text
dataset/
├── raw/
│   ├── empty/
│   ├── person/
│   └── animal/
│
├── processed/
│   ├── train/
│   ├── val/
│   └── test/
│
└── splits/
    ├── train.csv
    ├── val.csv
    └── test.csv
```

Images are collected in the real mountain house environment under different conditions:

* daytime;
* evening/night with automatic light;
* different subject positions;
* different distances from the entrance;
* empty scene, person, and animal presence.

Large image files are not tracked directly in the repository. Only dataset descriptions, scripts, and split files are versioned.

## Repository Structure

```text
smart-visual-alarm-mountain-house/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── docs/
│   ├── project_proposal.md
│   ├── architecture.md
│   ├── dataset_description.md
│   └── results.md
│
├── dataset/
│   ├── README.md
│   ├── raw/
│   ├── processed/
│   └── splits/
│
├── training/
│   ├── train_baseline_cnn.py
│   ├── train_mcunet.py
│   ├── train_tinyvit.py
│   ├── evaluate.py
│   ├── export_model.py
│   └── configs/
│
├── models/
│   ├── baseline_cnn/
│   ├── mcunet/
│   └── tinyvit/
│
├── esp32/
│   ├── README.md
│   ├── camera_test/
│   ├── mqtt_publish_test/
│   └── final_firmware/
│
├── raspberry/
│   ├── install_mosquitto.sh
│   ├── mqtt_subscriber.py
│   ├── telegram_bot.py
│   ├── event_logger.py
│   └── config.example.json
│
├── results/
│   ├── metrics/
│   ├── confusion_matrices/
│   ├── latency_tests/
│   └── plots/
│
└── report/
    ├── figures/
    └── overleaf_notes.md
```

## MQTT Communication

The ESP32-S3-EYE publishes alarm events to an MQTT topic.

Example topic:

```text
mountain_house/alarm/events
```

Example payload:

```json
{
  "event_id": "EVT_001",
  "timestamp": "2026-01-01 22:41:00",
  "label": "animal",
  "confidence": 0.82,
  "location": "mountain_house_entrance"
}
```

The Raspberry Pi subscribes to this topic and processes the received event.

## Telegram Notification

When a relevant event is received, the Raspberry Pi backend sends a Telegram notification to the user.

Example notification:

```text
Smart Visual Alarm

Detected class: animal
Confidence: 82%
Location: mountain_house_entrance
Timestamp: 2026-01-01 22:41:00
```

Telegram tokens and private credentials are not stored in the repository.

## Evaluation Metrics

The project evaluates both machine learning performance and system-level performance.

### Machine Learning Metrics

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix

### Efficiency and System Metrics

* Number of parameters
* Model size
* Inference latency
* MQTT communication latency
* End-to-end notification latency
* False positives
* False negatives

## Project Goals

The main goals of the project are:

1. Collect a small real-world dataset from the target environment.
2. Train and evaluate lightweight neural network models.
3. Compare a baseline model, MCUNet, and TinyViT.
4. Select the most suitable model for the visual alarm task.
5. Implement MQTT communication between ESP32-S3-EYE and Raspberry Pi.
6. Send Telegram notifications when alarm events are detected.
7. Evaluate the complete IoT pipeline in a realistic scenario.

## Current Status

* [ ] Repository structure created
* [ ] Raspberry Pi configured
* [ ] MQTT broker installed
* [ ] ESP32-S3-EYE camera tested
* [ ] Dataset collection started
* [ ] Baseline model implemented
* [ ] MCUNet tested
* [ ] TinyViT tested
* [ ] MQTT event publishing implemented
* [ ] Telegram backend implemented
* [ ] Final integration completed
* [ ] Experimental evaluation completed
* [ ] Final report completed

## Notes

This project is developed as part of an Internet of Things laboratory activity. The focus is on combining embedded vision, lightweight machine learning, MQTT communication, and remote notification in a real-world monitoring scenario.

```
```
