# Adaptive Multimodal AI Architecture for Edge Devices

> Issue Reference: #1174
> Status: Proposed
> Category: Edge Computing · Multimodal AI · Resource Optimization

---

## 1. Overview / Problem Statement

Modern edge devices — smartphones, IoT sensors, autonomous drones, smart home hubs — increasingly require sophisticated AI capabilities such as real-time object detection, natural language understanding, and multimodal reasoning. However, these devices operate under strict constraints:

- **Limited compute**: CPU/GPU/NPU resources vary wildly across device tiers.
- **Energy budgets**: Battery-powered devices cannot sustain heavy inference workloads.
- **Memory constraints**: RAM and storage are finite, preventing large model deployment.
- **Intermittent connectivity**: Cloud offloading is unreliable in remote or mobile scenarios.
- **Privacy requirements**: Sensitive data (medical, biometric) must stay on-device.

Current solutions are monolithic: either a lightweight model is deployed (sacrificing accuracy) or a full model is cloud-offloaded (sacrificing latency and privacy). There is no adaptive system that dynamically balances model complexity against available resources while preserving accuracy and privacy.

This proposal defines an **Adaptive Multimodal AI Architecture** — a self-optimizing, resource-aware framework that continuously adjusts its computational footprint to match device capabilities, task requirements, and energy budgets in real time.

---

## 2. Proposed Solution

We propose a **layered, modular architecture** with four core subsystems:

1. **Resource Monitoring Engine (RME)** — Continuously profiles device capabilities (CPU/GPU/NPU utilization, memory pressure, thermal state, battery level, network latency/bandwidth).

2. **Adaptive Model Orchestrator (AMO)** — Selects and switches between model variants (full, distilled, quantized, pruned) based on RME signals and task criticality.

3. **On-Device Learning Pipeline (ODLP)** — Performs knowledge distillation, federated fine-tuning, and continual learning directly on the edge device using gradient compression and memory-efficient optimizers.

4. **Edge-Cloud Hybrid Scheduler (ECHS)** — Makes intelligent offloading decisions by evaluating task urgency, data sensitivity, connectivity quality, and cost-benefit trade-offs.

The system operates as a closed-loop controller: sense resources → select model → execute inference → monitor outcomes → adjust. This feedback loop runs at sub-second intervals, enabling seamless transitions between computational tiers without user-perceptible degradation.

---

## 3. Key Features

1. **Dynamic Model Scaling** — Real-time switching between full-precision, half-precision, 8-bit, and 4-bit quantized model variants with zero-copy weight reloading.

2. **Resource-Aware Inference Scheduling** — Priority-based task queue that considers deadline constraints, energy budgets, and thermal throttling thresholds.

3. **Automatic Model Distillation** — On-device teacher-student distillation pipeline that creates optimized sub-models tailored to current workload patterns.

4. **Incremental Knowledge Transfer** — Lightweight gradient accumulation and delta-compression for continual learning without catastrophic forgetting.

5. **Hybrid Edge-Cloud Processing** — Intelligent task decomposition that routes compute sub-graphs to cloud only when latency and privacy constraints permit.

6. **Multimodal Fusion Engine** — Unified processing pipeline for vision, audio, text, and sensor data with cross-modal attention mechanisms.

7. **Adaptive Memory Management** — LRU-based model caching with predictive pre-loading based on usage patterns and upcoming task forecasts.

8. **Privacy-Preserving Computation** — Homomorphic encryption and secure enclave integration for sensitive inference paths; local-only processing by default.

9. **Energy-Proportional Computing** — Inference throughput scales linearly with available power budget, using dynamic voltage-frequency scaling (DVFS) hints.

10. **Federated Learning Support** — Aggregation-ready model updates that can be contributed to federated learning clusters without raw data exposure.

11. **Thermal-Aware Throttling** — Predictive thermal models prevent overheating by preemptively reducing model complexity before thermal shutdown triggers.

12. **Offline-First Design** — Full functionality without network connectivity; cloud features degrade gracefully rather than failing.

13. **Hardware Abstraction Layer (HAL)** — Unified API across CPU, GPU, NPU, DSP, and FPGA accelerators via pluggable compute backends.

14. **Observability Dashboard** — Real-time telemetry for model accuracy, latency, energy consumption, and resource utilization exposed via OpenTelemetry.

15. **OTA Model Updates** — Secure, differential model update mechanism with rollback support and A/B testing capabilities.

---

## 4. Technical Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                                │
│  ┌──────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────────────┐  │
│  │ Computer │  │    NLP /     │  │  Sensor    │  │   Multimodal     │  │
│  │ Vision   │  │    LLM       │  │  Fusion    │  │   Reasoning      │  │
│  └────┬─────┘  └──────┬───────┘  └─────┬──────┘  └────────┬─────────┘  │
│       │               │                │                   │            │
├───────┴───────────────┴────────────────┴───────────────────┴────────────┤
│                     ADAPTIVE MODEL ORCHESTRATOR (AMO)                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Model Registry  │  Variant Selector  │  Switch Controller       │  │
│  │  ┌─────────┐     │  ┌──────────────┐  │  ┌──────────────────┐   │  │
│  │  │Full FP32│     │  │Resource Score │  │  │Hot-Swap Engine  │   │  │
│  │  │Half FP16│     │  │Task Priority  │  │  │Weight Streaming │   │  │
│  │  │Int8 QAT │     │  │Latency Budget │  │  │Pipeline Flush   │   │  │
│  │  │Int4 GPTQ│     │  │Accuracy Req   │  │  │State Transfer   │   │  │
│  │  │Pruned   │     │  └──────────────┘  │  └──────────────────┘   │  │
│  │  └─────────┘     │                    │                          │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│                     HARDWARE ABSTRACTION LAYER (HAL)                     │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐               │
│  │  CPU   │ │  GPU   │ │  NPU   │ │  DSP   │ │  FPGA  │               │
│  │Backend │ │Backend │ │Backend │ │Backend │ │Backend │               │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘               │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│                     RESOURCE MONITORING ENGINE (RME)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ CPU/GPU  │ │ Memory   │ │ Thermal  │ │ Battery  │ │   Network    │  │
│  │ Utiliz.  │ │ Pressure │ │ Monitor  │ │ Monitor  │ │ Quality Est. │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│                   EDGE-CLOUD HYBRID SCHEDULER (ECHS)                     │
│  ┌────────────────┐  ┌─────────────────┐  ┌────────────────────────┐   │
│  │ Offload Decider│  │ Secure Channel  │  │ Result Aggregator      │   │
│  │ (Privacy Gate) │  │ (mTLS + HE)     │  │ (Merge Local + Remote)│   │
│  └────────────────┘  └─────────────────┘  └────────────────────────┘   │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│                   ON-DEVICE LEARNING PIPELINE (ODLP)                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────────┐  │
│  │ Knowledge    │ │ Gradient     │ │ Federated    │ │ Model         │  │
│  │ Distillation │ │ Compression  │ │ Aggregation  │ │ OTA Updates   │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └───────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Data Flow

### 5.1 Inference Request Flow

```
App Request → Task Classifier → AMO (select variant)
    → HAL (dispatch to compute unit) → Inference Engine
    → Post-Processing → Result Cache → App Response
```

1. Application submits a multimodal inference request (image + text + sensor data).
2. **Task Classifier** categorizes the request (e.g., "real-time object detection", "batch NLP summarization").
3. **AMO** queries RME for current resource state and selects the optimal model variant.
4. **HAL** dispatches computation to the best available accelerator (NPU preferred, GPU fallback, CPU last resort).
5. **Inference Engine** executes the model; intermediate results may be streamed for real-time applications.
6. **Post-Processing** applies task-specific formatting, confidence calibration, and output fusion.
7. Results are cached for potential replay and returned to the application.

### 5.2 Adaptive Scaling Flow

```
RME Telemetry → Resource Scorer → Threshold Comparator
    → [if degraded] → AMO → Switch to lighter variant
    → [if surplus]   → AMO → Upgrade to higher-accuracy variant
    → Loop (every 500ms)
```

### 5.3 Cloud Offload Flow

```
ECHS Decision Point:
    IF task is privacy-sensitive → Local Only
    IF latency budget > network RTT + cloud compute time → Offload
    IF energy cost of local compute > network energy cost → Offload
    IF bandwidth insufficient → Local Only (degraded)
    ELSE → Hybrid (compute sub-graph decomposition)
```

---

## 6. API Design

| Endpoint | Method | Description | Request Body | Response |
|---|---|---|---|---|
| `/v1/inference` | POST | Submit multimodal inference request | `{ inputs, model_hint, priority, deadline_ms }` | `{ result_id, output, latency_ms, model_used }` |
| `/v1/inference/{id}` | GET | Retrieve async inference result | — | `{ status, output, metrics }` |
| `/v1/models` | GET | List available model variants | `?device_profile=...` | `{ variants: [{ name, size, accuracy, latency }] }` |
| `/v1/models/active` | GET | Get currently active model variant | — | `{ variant, accuracy_score, resource_usage }` |
| `/v1/models/switch` | POST | Force switch to a specific variant | `{ variant_name, reason }` | `{ success, transition_time_ms }` |
| `/v1/resources` | GET | Current device resource snapshot | — | `{ cpu, gpu, memory, battery, thermal, network }` |
| `/v1/resources/subscribe` | WebSocket | Real-time resource telemetry stream | — | Streaming JSON telemetry frames |
| `/v1/offload/decide` | POST | Query offload recommendation | `{ task_type, data_size_mb, privacy_level }` | `{ decision: "local\|cloud\|hybrid", confidence }` |
| `/v1/learning/distill` | POST | Trigger on-device distillation | `{ teacher, student, dataset_ref, epochs }` | `{ job_id, estimated_time }` |
| `/v1/learning/federated/commit` | POST | Submit federated learning update | `{ compressed_gradients, metadata }` | `{ accepted, aggregation_id }` |
| `/v1/ota/update` | POST | Apply model OTA update | `{ model_name, version, delta_url, signature }` | `{ success, rollback_id }` |
| `/v1/ota/rollback` | POST | Rollback to previous model version | `{ rollback_id }` | `{ success, current_version }` |
| `/v1/telemetry` | GET | Export OpenTelemetry-compatible metrics | `?format=prometheus\|json` | Metrics payload |
| `/v1/config` | GET/PUT | Runtime configuration management | `{ energy_budget, accuracy_floor, thermal_limit }` | `{ applied }` |

---

## 7. Technology Stack

### 7.1 Core Framework

| Component | Technology | Rationale |
|---|---|---|
| Runtime Engine | ONNX Runtime / TFLite Micro | Cross-platform, hardware-accelerated inference |
| Model Hub | ONNX Model Zoo + Custom Registry | Standardized model format with quantization support |
| Compute Backends | OpenCL, Vulkan, NNAPI, CoreML, TensorRT | Maximum hardware coverage across device tiers |
| IPC / Messaging | ZeroMQ + Protocol Buffers | Low-latency inter-component communication |
| Scheduling | Custom priority queue (lock-free) | Sub-millisecond task dispatch |
| Configuration | TOML + Environment Overrides | Human-readable, mergeable config |

### 7.2 Resource Monitoring

| Component | Technology | Rationale |
|---|---|---|
| CPU/Memory | `/proc/stat`, `sysctl`, Windows PDH | Platform-native metrics |
| GPU Utilization | NVML, Metal Performance Shaders, Adreno SDK | Vendor-specific performance APIs |
| Thermal | Linux `sysfs`, Android `BatteryManager`, iOS `ProcessInfo` | Standardized thermal APIs |
| Battery | UPower, Android Intent, iOS UIDevice | Cross-platform energy monitoring |
| Network | TCP RTT probing, bandwidth estimation | Passive + active quality measurement |

### 7.3 Learning & Distillation

| Component | Technology | Rationale |
|---|---|---|
| Distillation Framework | Custom PyTorch Mobile + CoreML | Teacher-student with cross-platform export |
| Gradient Compression | 8-bit quantization + top-k sparsification | 100x reduction in update size |
| Optimizer | LAMB (Layer-wise Adaptive Moments) | Memory-efficient for on-device training |
| Replay Buffer | SQLite + Memory-mapped files | Persistent experience storage |

### 7.4 Security & Privacy

| Component | Technology | Rationale |
|---|---|---|
| Transport Encryption | mTLS 1.3 | Mutual authentication for cloud offload |
| Homomorphic Encryption | Microsoft SEAL / Concrete ML | Privacy-preserving cloud inference |
| Secure Enclave | Android Keystore / Apple Secure Enclave / Intel SGX | Hardware-rooted key storage |
| Attestation | Remote attestation via TPM/TEE | Verify model integrity at load time |

### 7.5 Observability

| Component | Technology | Rationale |
|---|---|---|
| Metrics | OpenTelemetry + Prometheus | Industry-standard observability |
| Logging | Structured JSON (spdlog) | Machine-parseable logs |
| Tracing | OpenTelemetry Distributed Tracing | End-to-end request tracing |
| Dashboard | Grafana (edge) + Cloud aggregation | Visual monitoring |

---

## 8. Implementation Roadmap

### Phase 1: Foundation (Months 1–3)

- [ ] Set up project structure, build system (CMake + Bazel), CI/CD pipeline
- [ ] Implement Hardware Abstraction Layer with CPU and GPU backends
- [ ] Build Resource Monitoring Engine with platform-specific probes
- [ ] Create basic model registry with FP32 and INT8 variant support
- [ ] Implement core inference pipeline (single model, single input modality)
- [ ] Unit tests and benchmarking framework
- **Deliverable**: Working inference engine with static model selection

### Phase 2: Adaptive Intelligence (Months 4–6)

- [ ] Implement Adaptive Model Orchestrator with hot-swap capability
- [ ] Build Resource Scorer with weighted multi-signal fusion
- [ ] Add model variant generation pipeline (quantization, pruning)
- [ ] Implement on-device knowledge distillation (teacher → student)
- [ ] Add thermal-aware throttling and energy-proportional scaling
- [ ] Integration tests on reference hardware (Raspberry Pi 5, Jetson Orin Nano, Snapdragon 8 Gen 3)
- **Deliverable**: Self-adapting inference with 3+ model variants per task

### Phase 3: Multimodal & Hybrid (Months 7–9)

- [ ] Implement Multimodal Fusion Engine (vision + audio + text)
- [ ] Build Edge-Cloud Hybrid Scheduler with privacy gate
- [ ] Add secure cloud offload channel (mTLS + optional HE)
- [ ] Implement federated learning client with gradient compression
- [ ] Add OTA model update mechanism with rollback
- [ ] End-to-end testing on real-world scenarios (smart home, drone, mobile photography)
- **Deliverable**: Full multimodal hybrid system with cloud offload

### Phase 4: Production Hardening (Months 10–12)

- [ ] Security audit, penetration testing, compliance review
- [ ] Performance optimization (inference latency < 50ms p99 on target devices)
- [ ] Observability stack deployment (OpenTelemetry → Grafana)
- [ ] Developer SDK and API documentation
- [ ] A/B testing framework for model deployments
- [ ] Production deployment on 3+ device categories
- **Deliverable**: Production-ready system with SDK, docs, and monitoring

---

## 9. Security & Compliance

### 9.1 Threat Model

| Threat | Mitigation |
|---|---|
| Model extraction / IP theft | Encrypted model weights at rest; runtime decryption in TEE |
| Data exfiltration via offload | Privacy gate with mandatory sensitivity classification |
| Model poisoning via OTA | Code signing (ECDSA P-256) + rollback verification |
| Side-channel attacks | Constant-time inference for sensitive paths; TEE isolation |
| Federated learning inversion | Gradient noise injection (DP-SGD with ε ≤ 1.0) |
| Supply chain compromise | Reproducible builds; hash verification for all dependencies |

### 9.2 Compliance

- **GDPR**: Data minimization; on-device processing by default; no raw data leaves device without explicit consent.
- **CCPA**: User control over data offloading decisions; configurable privacy levels.
- **SOC 2 Type II**: Audit logging for all inference and offload decisions; access control for configuration APIs.
- **ISO 27001**: Information security management system for model lifecycle.

### 9.3 Access Control

- RBAC for configuration APIs (admin, operator, observer roles)
- API authentication via OAuth 2.0 with device-bound tokens
- Secure boot chain: bootloader → OS → runtime → model (verified at each stage)

---

## 10. Performance Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| Inference latency (p50) | < 20ms | End-to-end timestamp |
| Inference latency (p99) | < 50ms | End-to-end timestamp |
| Model switch time | < 100ms | Variant hot-swap duration |
| Memory overhead (RME + AMO) | < 50MB | RSS measurement |
| CPU overhead (monitoring) | < 2% | Platform CPU counters |
| Energy per inference | Device-specific baseline | Power meter / RAPL |
| Model accuracy retention | ≥ 95% of full-model accuracy | Task-specific benchmarks |
| Cloud offload success rate | > 99.5% (when decided) | Retry/failure tracking |
| OTA update failure rate | < 0.1% | Update telemetry |
| Cold start time | < 2s | Process launch to first inference |

---

## 11. Testing Strategy

### 11.1 Unit Testing

- Each subsystem (RME, AMO, ODLP, ECHS, HAL) tested in isolation with mocked dependencies.
- Target: 90%+ line coverage, 80%+ branch coverage.
- Framework: Google Test (C++), pytest (Python bindings).

### 11.2 Integration Testing

- Cross-subsystem integration with real hardware backends.
- Test matrix: CPU-only, GPU-accelerated, NPU-accelerated.
- Automated on CI with QEMU/device farm emulation.

### 11.3 Performance Testing

- Latency benchmarks under varying load (1, 10, 100 concurrent requests).
- Sustained throughput tests (24-hour soak tests).
- Energy profiling on physical devices using Monsoon power monitor.

### 11.4 Accuracy Testing

- Per-task benchmark suites (COCO for vision, GLUE for NLP, LibriSpeech for audio).
- A/B accuracy comparison: full model vs. adaptive variants.
- Regression testing on every model update.

### 11.5 Security Testing

- Fuzz testing of all API endpoints (libFuzzer).
- Penetration testing of cloud offload channel.
- Model integrity verification testing.

### 11.6 Chaos Testing

- Simulated resource exhaustion (CPU throttling, memory pressure, thermal limits).
- Network partition scenarios (offline → degraded → restored).
- Fault injection in model loading and switching paths.

---

## 12. Deployment Architecture

### 12.1 Device-Side Deployment

```
┌─────────────────────────────────────────────┐
│              Edge Device                     │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │        Application Layer             │   │
│  └──────────────┬───────────────────────┘   │
│                 │ gRPC / Shared Library     │
│  ┌──────────────▼───────────────────────┐   │
│  │     Adaptive AI Runtime (AAR)        │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌───────┐  │   │
│  │  │ RME │ │ AMO │ │ODLP │ │ ECHS  │  │   │
│  │  └──┬──┘ └──┬──┘ └──┬──┘ └───┬───┘  │   │
│  │     └───────┴───────┴───────┘       │   │
│  │              │                        │   │
│  │  ┌───────────▼────────────────────┐  │   │
│  │  │   Hardware Abstraction Layer   │  │   │
│  │  └────────────────────────────────┘  │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  Model Storage: /data/aar/models/            │
│  Config: /etc/aar/config.toml                │
│  Logs: /var/log/aar/                         │
└─────────────────────────────────────────────┘
```

### 12.2 Cloud-Side Deployment

```
┌──────────────────────────────────────────────────────────┐
│                    Cloud Infrastructure                    │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐   ┌────────────┐  │
│  │   API Gateway │    │   Offload    │   │ Federated  │  │
│  │   (Kong/Envoy)│───▶│   Server     │   │ Aggregator │  │
│  └──────────────┘    │  (GPU nodes) │   │ (Secure)   │  │
│                      └──────────────┘   └──────┬─────┘  │
│                                                  │        │
│  ┌──────────────┐    ┌──────────────┐   ┌──────▼─────┐  │
│  │  Model Registry│   │   OTA        │   │ Telemetry  │  │
│  │  (Artifactory)│   │   Service    │   │ Collector  │  │
│  └──────────────┘    └──────────────┘   │ (OTLP)     │  │
│                                        └────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 12.3 Packaging

- **Linux (ARM64/x86_64)**: `.deb` and `.apk` packages; Docker containers for x86
- **Android**: AAR library with Gradle plugin
- **iOS**: CocoaPods / Swift Package Manager
- **macOS**: `.pkg` installer with Homebrew tap
- **Windows**: MSI installer and NuGet package

---

## 13. Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Hardware fragmentation (too many accelerators) | High | Medium | Prioritize top 5 SoCs; HAL abstraction isolates backend complexity |
| Model accuracy degradation under quantization | Medium | High | Automated accuracy regression testing; minimum accuracy floor enforcement |
| Thermal throttling causing cascading failures | Medium | High | Predictive thermal model with 30s look-ahead; graceful degradation |
| Cloud offload latency spikes | Medium | Medium | Timeout-based fallback to local; hybrid decomposition as safety net |
| Security breach via compromised OTA | Low | Critical | Multi-signature verification; staged rollout with canary devices |
| On-device learning instability (catastrophic forgetting) | Medium | Medium | Elastic weight consolidation (EWC); replay buffer with importance sampling |
| Vendor lock-in to specific NPU SDK | Medium | Medium | Abstraction via ONNX IR; vendor-agnostic compute graphs |
| Battery drain from continuous monitoring | Low | Medium | Event-driven RME with polling intervals adaptive to change rate |
| Regulatory changes (new privacy laws) | Low | High | Modular privacy gate; configurable compliance profiles |

---

## 14. Success Criteria

### 14.1 Technical Success

- [ ] Inference latency p99 < 50ms on target edge devices (Jetson Orin Nano, Snapdragon 8 Gen 3, Raspberry Pi 5)
- [ ] Model accuracy within 5% of full cloud model for supported tasks
- [ ] Energy consumption reduced by ≥ 50% compared to always-on full-model inference
- [ ] Zero-downtime model switching with < 100ms transition time
- [ ] Successful cloud offload with < 200ms added latency (p50) over good connectivity
- [ ] 99.9% uptime over 30-day sustained testing

### 14.2 Adoption Success

- [ ] SDK integrated into ≥ 3 partner applications within 6 months of GA
- [ ] Deployed on ≥ 3 distinct device categories (mobile, IoT, drone)
- [ ] Developer onboarding time < 4 hours (time to first inference)

### 14.3 Business Impact

- [ ] 70% reduction in cloud inference costs for participating workloads
- [ ] Enables new product categories previously blocked by edge compute limitations
- [ ] Measurable improvement in end-user experience (latency, battery life, privacy)

---

## 15. Open Questions

1. What is the minimum viable set of model architectures to support in Phase 1? (Proposed: ResNet-50, MobileNetV3, DistilBERT)
2. Should the federated learning aggregator be self-hosted or offered as a managed service?
3. What is the licensing model for the edge runtime? (Proposed: Apache 2.0 for core, commercial for cloud services)
4. How do we handle model updates for devices that are offline for extended periods? (Proposed: delta updates with compression)
5. What level of deterministic reproducibility is required for safety-critical applications?

---

*This document serves as the technical specification for Issue #1174: Adaptive Multimodal AI Architecture for Edge Devices. Feedback and contributions are welcome.*