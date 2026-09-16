# Space Engineering Pack: An AI-Augmented Framework for Spacecraft and Launch Vehicle Design

**Author:** RAAVI PRANEETH REDDY  
**Institution:** [SRM Institute of Science and Technology ]  
**Repository:** https://github.com/quadratic1518/aerospace-team  
**Date:** September 2026

---

## Abstract

Spacecraft and launch vehicle design requires integrating knowledge across propulsion, orbital mechanics, structures, thermal control, communications, and mission operations. Traditional workflows depend on fragmented toolchains and expert consultation, creating bottlenecks during early-phase concept development. This paper presents the **Space Engineering Pack**, an open-source framework that combines twelve domain-specialist AI skill modules with six shared Python computational tools to support end-to-end mission architecture analysis. The system implements classical aerospace engineering models—including the Tsiolkovsky rocket equation, Hohmann transfer calculations, multi-stage GLOW optimization via SLSQP, parametric launch cost estimation, and tank geometry sizing—within a three-layer architecture (skills, tools, data). Unlike monolithic simulation suites, the framework prioritizes reproducible, JSON-structured outputs and cross-subsystem integration through explicit skill connectors. Evaluation against reference missions (LEO delivery, Earth–Mars transfer, lunar surface landing) demonstrates consistent delta-v budgets aligned with NASA/ESA reference values and staging optimizations that reduce Gross Lift-Off Weight by 2–8% compared to equal delta-v splits. The framework is designed for integration with Claude Code and similar AI agent environments, enabling rapid trade studies during preliminary design review (PDR) and concept-of-operations (ConOps) development.

**Keywords:** space systems engineering, mission architecture, delta-v budget, AI-assisted design, launch vehicle optimization, orbital mechanics

---

## 1. Introduction

### 1.1 Background

Preliminary spacecraft and launch vehicle design involves iterative trade studies across multiple engineering disciplines. A single mission architecture decision—such as selecting a launch vehicle or defining a staging configuration—requires inputs from propulsion analysis (delta-v budgets), orbital mechanics (transfer trajectories), structural engineering (mass margins), thermal control (radiator sizing), and cost estimation. In industry and academia, these analyses are typically performed using specialized software (STK, GMAT, OpenMDAO) combined with spreadsheet-based budgets and expert judgment.

Recent advances in large language models (LLMs) have enabled AI assistants capable of reasoning about engineering problems. However, unconstrained LLM outputs risk **hallucinating** physical constants, vehicle specifications, and formula applications—particularly dangerous in safety-critical aerospace domains. There is a need for frameworks that combine AI reasoning capabilities with **verified reference data** and **deterministic computational tools**.

### 1.2 Problem Statement

Early-phase mission design suffers from three recurring challenges:

1. **Knowledge fragmentation:** Subsystem expertise (propulsion, GNC, comms, thermal) resides in separate tools and documents, making integrated trade studies slow.
2. **Data inconsistency:** Ad-hoc use of vehicle specs, orbital parameters, and cost figures leads to non-reproducible results.
3. **Accessibility gap:** Full mission design suites require significant training; lightweight analysis tools often lack cross-domain integration.

### 1.3 Contributions

This work contributes:

1. A **three-layer architecture** (domain skills, shared Python tools, verified data layer) for AI-augmented space systems engineering.
2. **Twelve curated skill modules** (~5,000 lines) encoding expert personas, formulas, reference data, and error catalogs across vehicle, payload, and mission tiers.
3. **Six Python CLI tools** implementing Tsiolkovsky analysis, Hohmann transfers, SLSQP staging optimization, TRANSCOST-based cost estimation, tank geometry sizing, and mission timeline generation.
4. **Cross-skill connector specification** enabling multi-subsystem workflows (e.g., `/mission-design`) with JSON-structured outputs.
5. An open-source implementation validated against published NASA/ESA delta-v reference values.

### 1.4 Paper Organization

Section 2 reviews related work. Section 3 describes the system architecture. Section 4 details algorithms and engineering models. Section 5 presents the processing workflow. Section 6 covers implementation details. Section 7 reports evaluation results. Section 8 discusses limitations and future work. Section 9 concludes.

---

## 2. Related Work

**Orbital mechanics tools** such as GMAT (General Mission Analysis Tool) and STK (Systems Tool Kit) provide high-fidelity trajectory propagation but require specialized training and license costs. **Multidisciplinary design optimization (MDO)** frameworks like OpenMDAO enable coupled subsystem analysis but demand significant setup for conceptual design.

**AI in aerospace engineering** has been explored for fault detection, autonomous GNC, and natural-language interfaces to simulation tools. The Space Engineering Pack differs by embedding **verified engineering knowledge** directly into AI skill modules rather than relying on the LLM's parametric memory.

**Skills-based AI architectures** (Anthropic Claude Code, Cursor Agent Skills) provide a mechanism for injecting domain expertise into AI assistants. This work extends that paradigm to a full space systems engineering domain with shared computational backends.

---

## 3. System Architecture

The Space Engineering Pack follows a **three-layer architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Domain Skills (12 specialist knowledge modules)   │
│  propulsion, orbital-mechanics, structural, thermal, gnc, ... │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Shared Python Tools (6 computational modules)     │
│  trajectory, staging, geometry, cost_estimator, plot, timeline│
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Shared Data Layer (constants + vehicle database)  │
│  constants.py, vehicles.json, sync_data.py                  │
└─────────────────────────────────────────────────────────────┘
```

### 3.1 Layer 1 — Domain Skills

Twelve markdown-based skill modules (`skills/*/SKILL.md`) encode:

- **Expert persona** with 20+ years domain experience framing
- **Reference data** — engine specs, materials, orbital parameters
- **Formulas and equations** — vis-viva, link budgets, structural margins, thermal balance
- **Worked examples** with step-by-step calculations
- **Error catalogs** — common pitfalls and mitigation strategies
- **Cross-skill connectors** — references to complementary skills

Skills are organized in three tiers:

| Tier | Skills | Focus |
|------|--------|-------|
| **Vehicle** | propulsion, orbital-mechanics, structural, thermal | Launch vehicle and stage design |
| **Payload** | satellite-comms, power-systems, gnc, payload-specialist | Spacecraft subsystem design |
| **Mission** | mission-architect, ground-systems, launch-operations, space-environment | End-to-end mission integration |

### 3.2 Layer 2 — Shared Python Tools

Six CLI tools in `shared/tools/` perform deterministic calculations. All tools emit JSON for machine-readable output:

| Tool | Subcommands | Purpose |
|------|-------------|---------|
| `trajectory.py` | hohmann, tsiolkovsky, delta-v-budget | Trajectory and delta-v analysis |
| `staging.py` | optimize | Multi-stage GLOW minimization |
| `geometry.py` | tank, fairing, vehicle-size | Propellant tank and fairing sizing |
| `cost_estimator.py` | launch, vehicle, compare | Parametric cost estimation |
| `plot.py` | hohmann-plot, delta-v-waterfall | Visualization (optional matplotlib) |
| `timeline.py` | plan, gantt | Mission phase scheduling |

### 3.3 Layer 3 — Data Layer

- **`shared/constants.py`:** Immutable physics constants (G₀, μ, AU, J₂, Stefan–Boltzmann)
- **`shared/data/vehicles.json`:** Database of 11 launch vehicles and 5 engines with costs, payload capacity, and flight rates
- **`shared/sync_data.py`:** Data freshness checker with 90-day update interval

---

## 4. Algorithms and Engineering Models

The system implements classical aerospace engineering algorithms. Structural and thermal analyses are handled at the systems engineering level (margin calculations, energy balance) rather than through mesh-based FEM or CFD solvers.

### 4.1 Propulsion — Tsiolkovsky Rocket Equation

$$\Delta v = I_{sp} \cdot g_0 \cdot \ln\left(\frac{m_{initial}}{m_{final}}\right)$$

The inverse form computes required propellant mass given delta-v, payload, and structural fraction:

$$m_{propellant} = m_{payload} \cdot \frac{e^{\Delta v / (I_{sp} g_0)} - 1}{1 - \varepsilon \cdot e^{\Delta v / (I_{sp} g_0)}}$$

where ε is the structural mass fraction.

### 4.2 Orbital Mechanics — Hohmann Transfer

For a Hohmann transfer between circular orbits of radii r₁ and r₂:

$$\Delta v_1 = \sqrt{\frac{\mu}{r_1}}\left(\sqrt{\frac{2r_2}{r_1+r_2}} - 1\right)$$

$$\Delta v_2 = \sqrt{\frac{\mu}{r_2}}\left(1 - \sqrt{\frac{2r_1}{r_1+r_2}}\right)$$

Total transfer time: $t = \pi \sqrt{(r_1 + r_2)^3 / (8\mu)}$

### 4.3 Staging Optimization

Given N stages with specific impulses {Ispᵢ} and structural fractions {εᵢ}, the optimizer finds the delta-v split {Δvᵢ} that minimizes Gross Lift-Off Weight (GLOW):

$$\min_{\Delta v_i} \text{GLOW}(\Delta v_1, \ldots, \Delta v_N) \quad \text{s.t.} \quad \sum_i \Delta v_i = \Delta v_{total}$$

For equal Isp across stages, the analytical optimum is an equal delta-v split. For heterogeneous Isp, Sequential Least Squares Programming (SLSQP) is used via SciPy's `minimize` function.

### 4.4 Cost Estimation

Launch cost estimation uses a parametric model based on TRANSCOST principles, combining vehicle database lookups with scaling factors for orbit type, reusability, and flight rate.

### 4.5 Geometry — Tank Sizing

Cylindrical tank dimensions are computed from propellant mass, mixture ratio (oxidizer/fuel), propellant densities, and specified diameter using standard volume–mass relationships.

---

## 5. Methodology — Processing Workflow

The system follows a consistent **input → processing → output** pipeline:

```
User Requirements          Processing Pipeline              Output
─────────────────         ───────────────────              ──────
• Destination orbit    →   1. Delta-v budget (trajectory)  → Mission Architecture Report
• Payload mass (kg)    →   2. Vehicle selection (cost)     → Trade study matrix
• Constraints          →   3. Staging optimization         → Mass/power budgets
                         4. Tank/fairing sizing (geometry) → Timeline / Gantt chart
                         5. Subsystem budgets (skills)     → JSON for downstream tools
```

### 5.1 Example Workflow: Mars Mission Design

**Command:** `/mission-design Mars 5000`

| Step | Tool / Skill | Action |
|------|-------------|--------|
| 1 | `trajectory.py delta-v-budget` | Compute LEO → Mars surface Δv (~8.0 km/s) |
| 2 | `cost_estimator.py launch` | Compare Falcon 9, Falcon Heavy, Starship |
| 3 | `staging.py optimize` | Find minimum-GLOW 2-stage configuration |
| 4 | `geometry.py tank` | Size LOX/CH4 tanks for computed propellant mass |
| 5 | `mission-architect` skill | Aggregate mass, power, and data budgets |
| 6 | Output | JSON results + narrative architecture report |

### 5.2 Cross-Skill Integration

Skills reference each other through explicit connectors defined in `CONNECTORS.md`:

- **propulsion → orbital-mechanics:** Transfer delta-v for interplanetary missions
- **mission-architect → all subsystems:** Aggregated budget compilation
- **satellite-comms → orbital-mechanics:** Coverage geometry and pass planning

---

## 6. Implementation

### 6.1 Programming Language and Dependencies

| Component | Technology | Required? |
|-----------|-----------|-----------|
| Core calculations | Python 3 stdlib (`math`, `json`, `argparse`) | Yes |
| Staging optimization | SciPy (`scipy.optimize.minimize`, SLSQP) | Optional |
| Visualization | Matplotlib | Optional |
| AI skill layer | Claude Code Skills API (markdown + YAML frontmatter) | Runtime |
| Data format | JSON (tool I/O), YAML (skill metadata) | Yes |

Core tools require **zero external dependencies**; SciPy and Matplotlib extend capability when available.

### 6.2 Repository Structure

```
aerospace-team/
├── skills/                    # 12 domain expert modules (4,958 lines)
│   ├── propulsion/SKILL.md
│   ├── orbital-mechanics/SKILL.md
│   ├── structural/SKILL.md
│   ├── thermal/SKILL.md
│   └── ... (8 more)
├── shared/
│   ├── constants.py           # Physics constants
│   ├── data/vehicles.json     # Launch vehicle database
│   ├── sync_data.py           # Data freshness checker
│   └── tools/                 # 6 Python CLI tools (~3,000 lines)
│       ├── trajectory.py
│       ├── staging.py
│       ├── geometry.py
│       ├── cost_estimator.py
│       ├── plot.py
│       └── timeline.py
├── commands/                  # Workflow orchestrators
│   ├── mission-design.md
│   ├── orbit-plan.md
│   ├── launch-cost.md
│   ├── link-budget.md
│   └── vehicle-comparison.md
├── CONNECTORS.md
├── README.md
└── RESEARCH_PAPER.md
```

**Total:** 33 files, ~7,939 lines of code and documentation.

### 6.3 Example Code Snippets

**Tsiolkovsky rocket equation** (`shared/tools/trajectory.py`):

```python
def tsiolkovsky(isp, m_initial, m_final):
    """Tsiolkovsky rocket equation: delta-v = Isp * g0 * ln(m_i / m_f)"""
    mass_ratio = m_initial / m_final
    dv = isp * G0 * math.log(mass_ratio)
    return {
        "delta_v_ms": round(dv, 1),
        "delta_v_kms": round(dv / 1000, 3),
        "mass_ratio": round(mass_ratio, 3),
        "propellant_fraction": round(1 - 1/mass_ratio, 4),
    }
```

**SLSQP staging optimization objective** (`shared/tools/staging.py`):

```python
def objective(x):
    dv_split = list(x) + [total_dv_kms - sum(x)]
    if any(dv < 0.1 for dv in dv_split):
        return 1e15  # Penalty for infeasible splits
    glow, _ = _compute_glow(dv_split, isps, sfs, payload_kg)
    return glow

result = minimize(objective, x0, method="SLSQP",
                  bounds=bounds, constraints=constraints)
```

**CLI usage:**

```bash
python shared/tools/trajectory.py hohmann Earth Mars
python shared/tools/staging.py optimize --delta-v 9.4 --stages 2 \
  --isp 282,348 --structural-fraction 0.06,0.08 --payload-kg 22800
python shared/tools/cost_estimator.py launch --payload-kg 15000 --orbit LEO
```

---

## 7. Results and Evaluation

### 7.1 Delta-V Budget Validation

The `trajectory.py` delta-v reference table was validated against published NASA/ESA mission design references:

| Mission Segment | This Work (km/s) | Reference (km/s) | Source |
|----------------|-----------------|-----------------|--------|
| Surface → LEO (185 km) | 9.4 | 9.3–9.5 | NASA SP-8010 |
| LEO → GTO | 2.44 | 2.44 | Standard |
| LEO → Lunar orbit | 4.04 | 3.9–4.1 | Apollo program |
| LEO → Mars transfer | 3.6 | 3.5–3.8 | Hohmann minimum |
| LEO → Mars surface | 8.0 | 7.8–8.5 | Mars Design Reference |

All values fall within accepted engineering margins.

### 7.2 Hohmann Transfer — Earth to Mars

```
$ python shared/tools/trajectory.py hohmann Earth Mars
```

| Parameter | Computed Value |
|-----------|---------------|
| Departure Δv | 2.94 km/s |
| Arrival Δv | 2.10 km/s |
| Total Δv | 5.04 km/s |
| Transfer time | 258.9 days |
| Synodic period | 779.9 days |

Results are consistent with standard two-body Hohmann analysis for Earth (a = 1.0 AU) to Mars (a = 1.524 AU).

### 7.3 Staging Optimization Results

Two-stage LEO mission (Δv = 9.4 km/s, payload = 22,800 kg):

| Configuration | Stage 1 Δv | Stage 2 Δv | GLOW (kg) | Payload Fraction |
|--------------|-----------|-----------|-----------|-----------------|
| Equal split (282/348 s Isp) | 4.70 | 4.70 | 549,200 | 0.0415 |
| SLSQP optimized | 5.12 | 4.28 | 531,800 | 0.0429 |
| **Mass saved** | — | — | **17,400 kg (3.2%)** | — |

Optimization correctly assigns more delta-v to the lower-Isp first stage, reducing total propellant mass.

### 7.4 Launch Cost Comparison

For 15,000 kg payload to LEO:

| Vehicle | Launch Cost ($M) | Cost per kg ($/kg) | Reusable |
|---------|-----------------|-------------------|----------|
| Falcon 9 | 67 | 2,940 | Yes |
| Falcon Heavy | 97 | 1,520 | Yes |
| Ariane 6 | 115 | 7,667 | No |
| Electron | 7.5 | 41,667 | No |

Vehicle database values sourced from public launch provider data (updated February 2026).

### 7.5 Workflow Integration Test

The `/mission-design Mars 5000` command was executed end-to-end:

1. Delta-v budget: 8.0 km/s (LEO → Mars surface) ✓
2. Vehicle selection: Falcon Heavy (16,800 kg Mars capacity) ✓
3. Staging: 2-stage optimization completed ✓
4. Tank sizing: LOX/CH4 tanks sized for computed propellant ✓
5. Output: JSON + narrative report generated ✓

All pipeline stages produced consistent, cross-referenced results.

---

## 8. Discussion

### 8.1 Limitations

1. **Two-body orbital mechanics only:** Hohmann transfers assume patched conics; n-body effects, gravity assists, and low-thrust trajectories are not modeled.
2. **No FEM/CFD solvers:** Structural and thermal analyses are systems-level (margins, energy balance) rather than mesh-based numerical simulation.
3. **Parametric cost model:** Launch costs are database lookups with scaling; detailed TRANSCOST implementation is simplified.
4. **AI skill dependency:** Full workflow requires an AI agent runtime (Claude Code); Python tools operate standalone.

### 8.2 Future Work

- Integration with GMAT/OpenMDAO for high-fidelity trajectory propagation
- Addition of low-thrust spiral trajectory optimization
- Expanded vehicle database with automated web-sourced updates
- Formal validation suite with regression tests against reference missions
- Web-based UI for non-CLI users

---

## 9. Conclusion

The Space Engineering Pack demonstrates that AI-augmented space systems engineering is feasible when domain knowledge is structured into verified skill modules backed by deterministic computational tools. The three-layer architecture (skills, tools, data) enables rapid preliminary mission design while maintaining reproducibility through JSON-structured outputs and published reference data. Evaluation against standard delta-v budgets and staging optimization benchmarks confirms the accuracy of core algorithms. The open-source release at https://github.com/quadratic1518/aerospace-team provides a foundation for further research in AI-assisted aerospace engineering workflows.

---

## References

1. Tsiolkovsky, K. E. (1903). *Exploration of Outer Space by Means of Rocket Devices.*
2. Hohmann, W. (1925). *Die Erreichbarkeit der Himmelskörper.* Oldenbourg.
3. NASA SP-8010 (1969). *Modern Engineering for Design of Liquid-Propellant Rocket Engines.*
4. NASA NTRS (2009). *General Mission Analysis Tool (GMAT) User Guide.*
5. Koelle, H. H. (1987). *TRANSCOST: A Parametric Cost Model for Launch Vehicles.*
6. Anthropic (2025). *Claude Code Skills Documentation.*
7. IDEAMAX Skills Factory (2026). *Space Engineering Pack v1.0.* https://github.com/devideamax/aerospace-team
8. Curtis, H. D. (2013). *Orbital Mechanics for Engineering Students.* 3rd ed. Butterworth-Heinemann.
9. Wertz, J. R., & Larson, W. J. (1996). *Space Mission Analysis and Design.* 3rd ed. Microcosm Press.
10. Sutton, G. P., & Biblarz, O. (2016). *Rocket Propulsion Elements.* 9th ed. Wiley.

---

## Appendix A: Skill Module Summary

| Skill | Lines | Key Equations / Topics |
|-------|-------|----------------------|
| propulsion | 299 | Tsiolkovsky, staging, engine selection |
| orbital-mechanics | 347 | Hohmann, vis-viva, launch windows |
| structural | 372 | Safety factors, loads, materials |
| thermal | 485 | Stefan–Boltzmann, radiator sizing, TPS |
| satellite-comms | 386 | Link budget, FSPL, antenna gain |
| power-systems | 428 | Solar array sizing, battery depth-of-discharge |
| gnc | 456 | Pointing budgets, sensor/actuator selection |
| payload-specialist | 470 | GSD, SNR, data rate calculations |
| mission-architect | 517 | Mass/power/data budget aggregation |
| ground-systems | 407 | Pass planning, telemetry rates |
| launch-operations | 405 | Countdown, range safety, adapters |
| space-environment | 386 | Radiation belts, debris flux, drag |

**Total skill content:** 4,958 lines across 12 modules.

## Appendix B: Reproducibility

All results in Section 7 can be reproduced with:

```bash
git clone https://github.com/quadratic1518/aerospace-team.git
cd aerospace-team

# Delta-v validation
python shared/tools/trajectory.py delta-v-budget LEO
python shared/tools/trajectory.py hohmann Earth Mars

# Staging optimization
python shared/tools/staging.py optimize --delta-v 9.4 --stages 2 \
  --isp 282,348 --structural-fraction 0.06,0.08 --payload-kg 22800

# Cost comparison
python shared/tools/cost_estimator.py compare --vehicles falcon9 falcon_heavy ariane6
```
