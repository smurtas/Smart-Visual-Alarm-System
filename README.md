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
