# Smart Visual Alarm System

A TinyML-based smart visual alarm system for embedded IoT devices.

The project detects three classes from camera images:

- 👤 Person
- 🐾 Animal
- 🌿 Empty scene

The system is designed for low-power edge devices using an ESP32-S3-EYE and a Raspberry Pi.

---

# Project Overview

The architecture consists of four main components:

1. ESP32-S3-EYE
   - Camera acquisition
   - TinyML inference
   - MQTT publisher

2. Raspberry Pi
   - MQTT broker (Mosquitto)
   - Node-RED automation
   - Event logging
   - Image storage

3. Dashboard
   - Real-time monitoring
   - Confidence gauge
   - Confidence history
   - Detection statistics

4. Telegram Bot
   - Instant notifications
   - Captured image
   - Confidence score
   - Timestamp

---

# Repository Structure

```
Smart-Visual-Alarm-System/

├── dataset/
│   ├── raw/
│   ├── processed/
│   ├── incoming/
│   ├── rejected/
│   └── splits/
│
├── training/
│
├── models/
│   ├── mlp/
│   ├── mcunet/
│   └── tinyvit/
│
├── results/
│
├── firmware/
│   └── esp32_s3_eye_alarm/
│
├── raspberry/
│
├── NodeRed/
│
├── runtime/
│   ├── images/
│   ├── logs/
│   └── events.csv
│
├── report/
│
└── README.md
```

---

# Hardware

- ESP32-S3-EYE
- Raspberry Pi
- USB Camera (ESP32 integrated)
- WiFi Network

---

# Software

- ESP-IDF 6.0
- ESP-DL
- ESP-PPQ
- Python
- PyTorch
- Mosquitto MQTT
- Node-RED
- Telegram Bot API

---

# Machine Learning Pipeline

Dataset

↓

Manual labeling

↓

Data augmentation

↓

Train / Validation / Test split

↓

Model training

↓

Model comparison

↓

INT8 quantization

↓

ESP-DL conversion

↓

ESP32 deployment

---

# Models

Current models:

- MLP Baseline
- MCUNet
- TinyViT (work in progress)

---

# Raspberry Pi Features

- MQTT Broker
- Event logger
- Image storage
- CSV logging
- Node-RED Dashboard
- Telegram notifications

---

# Dashboard

Current dashboard includes:

- Detection class
- Confidence gauge
- Confidence history
- Detection counters
- Last detected class
- Last detection timestamp

---

# Telegram Notifications

Each detection sends:

- Captured image
- Detection class
- Confidence
- Timestamp

---

## Current project status

### Verified

- Camera initialization on ESP32-S3-EYE
- JPEG image acquisition
- Image preprocessing
- MCUNet INT8 model loading
- On-device inference
- Continuous classification loop
- Class mapping:
  - `0 = animal`
  - `1 = empty`
  - `2 = person`

### Implemented but not yet verified

- Wi-Fi connection module
- MQTT client and prediction publishing
- HTTP JPEG upload to the Raspberry Pi
- Integration between HTTP upload and MQTT event publication

### Pending

- Final firmware build after the latest changes
- Flash and serial monitor test
- Wi-Fi connection test
- MQTT broker connection test
- MQTT message reception on Raspberry Pi
- HTTP upload test
- Validation of `runtime/images/latest.jpg`
- Node-RED integration test
- Telegram notification with the real captured image
- InfluxDB and Grafana final integration
- Complete end-to-end system test

---

# Author

Stefano Murtas

Master's Degree in Data Science

University of Trento

---

# License

MIT License