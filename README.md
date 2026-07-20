# Project Rebel

> **An intelligent, embedded AI assistant system built on NVIDIA Jetson Orin Nano Super -- designed for real-world autonomy, multi-modal interaction, and progressive capability expansion across five major versions.**

---

## Table of Contents

- [Project Description](#project-description)
- [Goals](#goals)
- [Hardware](#hardware)
- [Version Roadmap](#version-roadmap)
  - [V1 -- Foundation](#v1--foundation)
  - [V2 -- Vision & Awareness](#v2--vision--awareness)
  - [V3 -- Intelligence & Autonomy](#v3--intelligence--autonomy)
  - [V4 -- Multi-Modal Mastery](#v4--multi-modal-mastery)
  - [V5 -- Full Autonomy & Deployment](#v5--full-autonomy--deployment)
- [Current Progress](#current-progress)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## Project Description

**Project Rebel** is an embedded AI platform powered by the NVIDIA Jetson Orin Nano Super. It combines computer vision, natural language processing, physical button I/O, and real-time LCD feedback into a single cohesive system. Rebel is designed from the ground up to be modular, extensible, and deployable -- evolving from a basic interactive terminal to a fully autonomous AI agent capable of operating in the real world.

The name "Rebel" reflects the project's philosophy: building a capable, independent intelligence that operates on edge hardware -- no cloud dependency required.

---

## Goals

- Build a fully functional, edge-based AI assistant that runs entirely on local hardware
- Demonstrate progressive AI capability through a structured version roadmap
- Integrate camera-based perception, voice/text I/O, and physical hardware controls into a unified system
- Serve as a learning and development platform for embedded AI, robotics, and autonomous systems
- Achieve production-level reliability and real-world deployment by V5

---

## Hardware

| Component | Details |
|---|---|
| **Compute** | NVIDIA Jetson Orin Nano Super |
| **Camera** | CSI / USB Camera Module |
| **Display** | LCD Screen (I2C or SPI interface) |
| **Input** | Physical Push Buttons (GPIO) |
| **Storage** | MicroSD / NVMe SSD |
| **Power** | DC Barrel Jack / USB-C Power Supply |
| **OS** | JetPack SDK (Ubuntu-based) |

---

## Version Roadmap

---

### V1 -- Foundation

**Theme:** Get the system alive. Establish core I/O, basic interaction, and a stable software base.

#### Goals
- Initialize and configure Jetson Orin Nano Super with JetPack
- Establish communication between all hardware components
- Build a minimal interactive loop with button input and LCD output
- Lay the software foundation for future version expansions

#### Features
- GPIO button detection and debouncing
- LCD display driver with text rendering
- Basic menu system navigable via physical buttons
- System diagnostics display (CPU, RAM, temp)
- Modular config file for hardware pin mapping
- **Numeric barcode generation** -- produces a valid barcode number the user manually types into an external system
- Checksum calculation and validation for generated numeric codes

#### Success Criteria
- [ ] All buttons register input reliably without false triggers
- [ ] LCD renders multi-line text without glitching
- [ ] System boots cleanly and enters main loop within 30 seconds
- [ ] Hardware diagnostic screen updates in real-time
- [ ] Generated numeric codes pass checksum validation every time
- [ ] Numeric barcode is clearly displayed on LCD for manual entry

#### Challenges
- GPIO debouncing and interrupt handling on Jetson
- I2C/SPI LCD compatibility and refresh rate tuning
- Stable boot environment with JetPack dependencies
- Fitting a readable numeric barcode code onto a small LCD display

---

### V2 -- Vision & Awareness

**Theme:** Give Rebel eyes. Integrate the camera and add basic computer vision capabilities.

#### Goals
- Integrate camera feed into the system pipeline
- Run real-time object detection and scene understanding
- Display vision results on the LCD
- Begin building a perception layer as the foundation for autonomy

#### Features
- Live camera feed capture (OpenCV)
- Real-time object detection (YOLOv8 / TensorRT optimized)
- Object label + confidence display on LCD
- Face detection and basic recognition
- Motion detection with alert trigger on physical output
- Camera toggle via physical button

#### Success Criteria
- [ ] Object detection runs at >=15 FPS on Jetson hardware
- [ ] LCD displays detected object labels in real-time
- [ ] Face detection correctly identifies presence/absence
- [ ] Motion detection triggers reliably with <1s latency
- [ ] TensorRT model inference time <50ms per frame

#### Modules
- `src/camera/` -- Camera capture, preprocessing, calibration
- `src/ai/detector.py` -- TensorRT inference pipeline
- `src/interface/lcd.py` -- LCD rendering for vision results
- `src/interface/buttons.py` -- Camera toggle button handler

#### Challenges
- TensorRT model conversion and optimization for Orin Nano Super
- Balancing inference performance with power consumption
- LCD refresh rate keeping up with real-time detections

---

### V3 -- Intelligence & Autonomy

**Theme:** Give Rebel a brain. Upgrade from numeric codes to fully scannable barcodes and introduce AI-driven prediction.

#### Goals
- Upgrade barcode output from a manually-typed number to a **rendered, scannable barcode image**
- Integrate AI-based product detection and prediction using the camera
- Connect detections to the database for automatic product lookup
- Build a reasoning loop that closes the full scan -> identify -> record pipeline

#### Key Upgrade: Numeric -> Scannable Barcode
> In V1, barcode generation produces a numeric code the user reads off the LCD and types manually into an external system. In V3, the system renders a real scannable barcode image (e.g., Code 128, EAN-13) that any standard barcode scanner or phone camera can read directly -- no manual entry required.

#### Features
- **Scannable barcode image generation** (Code 128 / EAN-13 via `src/barcode/generator.py`)
- Barcode rendered to display or exported as image file
- AI-driven product detection via camera (`src/ai/detector.py`)
- Confidence scoring to gate uncertain detections (`src/ai/confidence.py`)
- Automatic product lookup against `data/products.db` on successful scan
- Prediction pipeline for unknown/partial matches (`src/ai/predictor.py`)
- Button-triggered manual override for low-confidence results

#### Success Criteria
- [ ] Generated barcode scans correctly with a standard barcode reader 100% of the time
- [ ] Barcode image renders clearly on LCD or export at usable resolution
- [ ] Camera-based detection identifies known products with >=85% accuracy
- [ ] Confidence threshold correctly gates detections before DB lookup
- [ ] Full pipeline (detect -> lookup -> display) completes in <3 seconds

#### Modules
- `src/barcode/generator.py` -- Scannable barcode image rendering
- `src/barcode/checksum.py` -- Barcode checksum calculation
- `src/barcode/validator.py` -- Validates generated codes before output
- `src/ai/detector.py` -- Camera-based product detection
- `src/ai/predictor.py` -- Inference and product matching
- `src/ai/confidence.py` -- Confidence scoring and threshold logic
- `src/database/crud.py` -- Product lookup and record creation

#### Challenges
- Rendering a barcode image scannable at LCD resolution vs. exporting to file
- Balancing AI model size against inference speed for real-time detection
- Handling low-confidence detections gracefully without frustrating the user
- Keeping the detect -> barcode -> DB pipeline atomic and error-safe

---

### V4 -- Multi-Modal Mastery

**Theme:** Unify all modalities. Rebel sees, hears, speaks, thinks, and responds as a cohesive system.

#### Goals
- Fully integrate vision, audio, and language into a unified pipeline
- Enable context-aware conversations grounded in real-world perception
- Introduce memory and persistent state across sessions
- Achieve smooth, human-like interaction with <2s end-to-end response time

#### Features
- Multi-modal prompt construction (image + text -> LLM)
- Persistent memory store (session + long-term facts)
- Wake-word detection for hands-free activation
- Emotional tone detection from voice input
- Contextual LCD UI that adapts based on active mode
- Skill/plugin system for expandable behaviors
- Activity logging and replay

#### Success Criteria
- [ ] End-to-end voice interaction latency <=2 seconds
- [ ] LLM correctly references camera context in responses
- [ ] Wake word activates system with <500ms response
- [ ] Memory persists correctly across reboots
- [ ] At least 3 loadable skills/plugins function correctly

#### Modules
- `src/interface/menus.py` -- Adaptive LCD UI based on active mode
- `src/ai/` -- Full multi-modal pipeline integration
- `src/database/crud.py` -- Persistent session and memory storage
- `src/utils/logger.py` -- Activity logging and replay
- `src/barcode/` -- Expanded barcode skill integration

#### Challenges
- Real-time multi-modal pipeline coordination without bottlenecks
- Wake-word detection running in parallel with other inference
- Designing a clean plugin API that doesn't break core stability

---

### V5 -- Full Autonomy & Deployment

**Theme:** Rebel goes live. Production-ready, self-sufficient, deployable in the real world.

#### Goals
- Achieve full autonomous operation with minimal human intervention
- Package Rebel for reliable deployment and easy reproduction
- Build monitoring, self-diagnostics, and graceful failure recovery
- Create a clean public-facing release with documentation and demos

#### Features
- Autonomous task execution based on environmental triggers
- Self-diagnostic system with auto-restart on failure
- Remote dashboard (web UI) for monitoring and control
- Full deployment packaging (Docker / systemd service)
- Comprehensive test suite for all subsystems
- Public demo mode with guided interaction
- Complete documentation and setup guide
- OTA (Over-The-Air) update capability

#### Success Criteria
- [ ] System runs unattended for 24+ hours without manual intervention
- [ ] All subsystems recoverable from fault states automatically
- [ ] Web dashboard displays live system stats and camera feed
- [ ] Docker image builds and runs on a fresh Jetson in <15 minutes
- [ ] Test suite achieves >=90% coverage across all modules
- [ ] Public demo mode engages correctly with first-time users

#### Modules
- `tests/` -- Full integration and unit test suite
- `docs/` -- Final user and developer documentation
- `assets/wiring/` -- Hardware wiring diagrams for reproducible setup
- `data/backups/` -- Automated DB backup pipeline
- `data/models/` -- Exported, versioned model weights

#### Challenges
- Long-term thermal management and power stability
- Robust failure recovery without external intervention
- Making deployment reproducible across hardware variations

---

## Current Progress

| Version | Status | Completion |
|---|---|---|
| V1 -- Foundation | In Progress | ~1% |
| V2 -- Vision & Awareness | Not Started | 0% |
| V3 -- Intelligence & Autonomy | Not Started | 0% |
| V4 -- Multi-Modal Mastery | Not Started | 0% |
| V5 -- Full Autonomy & Deployment | Not Started | 0% |

### V1 Completed So Far
- [ ] Jetson Orin Nano Super flashed and configured with JetPack
- [ ] Hardware components connected and verified
- [ ] GPIO button driver implemented
- [ ] LCD driver and text rendering working
- [ ] Basic menu system functional
- [ ] System diagnostics display active

> **Last Updated:** July 19, 2026

---

## How to Run

### Prerequisites

- NVIDIA Jetson Orin Nano Super with JetPack 6.x installed
- Python 3.10+
- Camera connected (CSI or USB)
- LCD connected via I2C/SPI
- Physical buttons wired to GPIO pins per `config.py`

### 1. Clone the Repository

```bash
git clone https://github.com/TroubleJake/Project_Rebel
cd Project_Rebel
