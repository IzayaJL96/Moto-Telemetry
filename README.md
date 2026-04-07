# Moto-Telemetry

Wearable telemetry system for motorcycle riders — built from scratch.  
Captures motion and physiological data across the rider’s body during real-world riding.

**Status:** Active development — early prototype validated

---

## What this project shows

- Ability to go from zero to a working embedded system  
- Direct interaction with hardware (I2C, registers, sensors)  
- Real debugging of physical systems (power, wiring, soldering)  
- Structured engineering documentation (DEVLOG, versioning, validation)  
- Use of AI as an engineering tool with defined rules  

---

## Overview

This project aims to build a **distributed telemetry system** using multiple IMUs and biometric sensors to analyze rider behavior, body dynamics, and performance.

Inspired by professional motorsport telemetry (e.g., MotoGP), but designed to be:
- Low-cost  
- Modular  
- Open-source  
- Reproducible  

It is both:
- A **personal real-world system** (not theoretical)  
- A **technical portfolio project** documenting the full engineering process  

---

## Current Capabilities

- Dual IMU setup using ICM-20948 sensors  
- Simultaneous acquisition via independent I2C buses  
- Real-time acceleration and gyroscope data (converted to physical units)  
- Error handling and automatic sensor reconnection  
- Stable external power configuration  

Validated through physical testing:
- Sensors respond correctly to motion  
- Data changes consistently with orientation  
- System runs continuously without crashes  

---

## System Architecture

Layer 1 — Motorcycle dynamics *(planned)*  
└── IMU on bike: lean angle, G-forces  

Layer 2 — Rider data *(in progress)*  
├── 5× IMU (ICM-20948) — body tracking  
├── Heart rate + SpO2 (MAX30102)  
├── Temperature (DS18B20)  
├── EMG muscle activity  
└── Smartwatch integration  

---

## Hardware

### Microcontroller
- ESP32-WROVER-E (development)
- ESP32-S3 (planned production)

### Sensors
- ICM-20948 (9-axis IMU)
- MAX30102 (planned)
- DS18B20 (planned)
- EMG sensor (planned)

### Power
- External regulated 5V supply  
- Internal 3.3V regulation via ESP32  

---

## Key Technical Decisions

### Direct Register Access (No Abstraction Libraries)

The project avoids third-party libraries and interacts directly with sensor registers.

**Why:**
- Full control over configuration  
- Better understanding of hardware  
- Easier migration to ESP-IDF (C/C++)  

---

### Dual I2C Bus Architecture

- Multiple sensors run on separate I2C buses  
- Avoids address conflicts  
- Scales cleanly to more sensors  

---

### Hardware-First Debugging

Critical issues encountered:
- Power instability  
- Cold solder joints  
- Wiring faults  

**Approach:**
1. Validate power  
2. Verify hardware  
3. Debug firmware  

---

## Repository Structure

/docs  
    DEVLOG.md          → full engineering log  
    rules.md           → development & AI usage rules  

/MEDIA  
    → images, videos, prototypes  

/src  
    → firmware (MicroPython → ESP-IDF planned)  

---

## 📚 Knowledge Base

Common issues, debugging cases, and hardware lessons learned:  
→ `docs/knowledge-base/`

*(Will be expanded as the project evolves)*

---

## Development Log

The project includes a detailed DEVLOG documenting:

- Firmware versions (SemVer)  
- Hardware revisions  
- Bugs, root causes, and fixes  
- Real validation data  

This acts as a **full engineering trace**, not just a changelog.

---

## Roadmap

### Phase 1 — Data Logging *(Current)*
- SD card integration  
- CSV logging  
- Timestamp synchronization  
- First stable release (v1.0.0)

### Phase 2 — Real-Time Transmission
- WiFi + MQTT  
- Sensor expansion  

### Phase 3 — Data Visualization
- Python dashboard (FastAPI + Plotly)  
- Smartwatch integration  

### Phase 4 — Full Body Tracking
- 5 IMUs across the body  
- I2C multiplexer  

### Phase 5 — Production System
- Migration to ESP-IDF (C/C++)  
- Higher sampling rates  
- Full biomechanical analysis  

---

## Engineering Approach

- Datasheet-driven development  
- Hardware + software co-design  
- Iterative validation with real measurements  
- Documentation-first debugging mindset  

The project also integrates **AI-assisted development** with strict rules for:
- Code attribution  
- Result validation  
- Maintaining engineering rigor  

---

## Media

See `/MEDIA` for:
- Prototype builds  
- Test setups  
- Development videos  

*(More content will be added over time)*

---

## Why This Project

This is not a tutorial-based build.

It is a full system developed from scratch to demonstrate:
- Embedded systems engineering  
- Sensor integration  
- Real-world debugging  
- End-to-end system design  

---

## License

GPL v3 — use it, modify it, and keep it open.

---

## Author

Jairo J. López Torres  
GitHub: https://github.com/IzayaJL96
