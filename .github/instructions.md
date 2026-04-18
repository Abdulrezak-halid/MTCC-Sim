# 📞 Multi-Tier Call Center Simulation System

## 🎯 Project Overview
This project aims to design and implement a **Discrete Event Simulation system** for a multi-level call center using **Python + SimPy**, followed by a **React Dashboard** to visualize and analyze system performance under different scenarios.

The goal is to simulate realistic call center behavior and evaluate system efficiency based on key performance metrics.

---

# 🧩 Project Structure

## 1. Simulation & Analysis Layer (Python + SimPy)

### 🎯 Objective
Build a realistic simulation model of a tiered call center system using probabilistic and event-driven logic.

---

## 🏗️ System Model

### 📌 Entities
- **Customer** (Normal / VIP)
- **Call**

---

### 🧑‍💼 Resources
- Tier 1 Agents (First-level support)
- Tier 2 Specialists (Advanced support)
- IVR System (Initial classification)

---

### 🔁 Call Flow
1. Customer arrival (Poisson process)
2. IVR classification
3. Enter queue (priority-based)
4. Served by Tier 1
5. Either resolved or escalated
6. If escalated → Tier 2
7. Call completed OR abandoned

---

## ⚙️ Core Logic

### 📊 Arrival Process
- Modeled using **Poisson distribution**

### ⏱️ Service Time
- Modeled using **Exponential or Normal distribution**

### 🎯 Resolution Logic
- Tier 1 resolves calls based on probability (dynamic, not fixed)
- Unresolved calls escalate to Tier 2

### ⏳ Call Abandonment
- Each customer has a **random patience time**
- If waiting time exceeds patience → call is dropped

### 👑 VIP Priority
- Priority queue system
- VIP customers get higher priority (lower wait time)

---

## 📈 Key Metrics

- Average Waiting Time
- Average Service Time
- Queue Length Over Time
- Agent Utilization (Tier 1 & Tier 2)
- Call Abandonment Rate
- SLA Compliance (% calls answered within threshold)

---

## 🔬 Simulation Scenarios

Run multiple experiments:

- Normal Load
- Peak Load (2x–3x arrivals)
- Reduced staff scenario
- Increased VIP ratio
- Improved staff efficiency

---

## 🧱 Architecture
```
simulation/
├── environment.py
├── entities.py
├── resources.py
├── processes.py
├── metrics.py
├── scenarios.py
└── run_simulation.py
```


---

## 🧰 Tools

- Python
- SimPy
- NumPy
- Pandas
- JSON (for exporting results)

---

## 💡 Best Practices

- Avoid hardcoded values → use parameters
- Use probability distributions instead of fixed values
- Run multiple simulations (Monte Carlo approach)
- Use random seeds for reproducibility
- Separate simulation logic from metrics and output
- Validate model behavior (sanity checks)

---

---

# 🟩 2. Visualization Layer (React Dashboard)

## 🎯 Objective
Create an interactive dashboard to visualize simulation results and compare different scenarios.

---

## 🔄 Data Flow
```
SimPy Simulation → JSON Output → API → React Dashboard
```


---

## ⚙️ Backend Layer (Recommended)

### FastAPI
Acts as a bridge between simulation and frontend.

### Example Endpoints:
- `/run-simulation`
- `/get-metrics`
- `/compare-scenarios`

---

## 📊 Dashboard Features

### 📌 KPI Cards
- Average Wait Time
- Abandonment Rate
- SLA %
- Agent Utilization

---

### 📈 Charts
- Queue Length Over Time (Line Chart)
- Agent Utilization (Bar Chart)
- Scenario Comparison
- Call Distribution

---

### 🎛️ Controls
- Scenario Selector
- Number of Agents (Slider)
- VIP Ratio Control
- Arrival Rate Adjustment

---

## 🧰 Tools

- React
- TypeScript
- TailwindCSS
- Chart.js or Recharts
- Axios
- Zustand or Redux

---

## 💡 Best Practices

- Focus on clarity, not complexity
- Show only meaningful metrics (avoid raw data overload)
- Implement scenario comparison (critical for analysis)
- Use modular components:
  - KPI Cards
  - Charts
  - Controls

---

---

# 🚀 Project Workflow

## Step 1: System Design
- Define entities, resources, and flow

## Step 2: Simulation Implementation
- Build SimPy processes
- Add randomness and logic

## Step 3: Run Experiments
- Execute multiple scenarios
- Collect metrics

## Step 4: Export Data
- Save results as structured JSON

## Step 5: Build API
- Serve simulation data via FastAPI

## Step 6: Build Dashboard
- Visualize KPIs and charts
- Add controls for interaction

## Step 7: Analysis
- Compare scenarios
- Draw conclusions

---

# 🚨 Critical Quality Requirements

- No deterministic logic → must be probabilistic
- Multiple simulation runs required
- Scenario comparison is mandatory
- Metrics must be clear and meaningful
- Clean separation between simulation, analysis, and UI

---

# 💣 Final Note

If implemented properly, this is not just a university project —  
it becomes a **full simulation system + data visualization platform** suitable for a strong portfolio.

If implemented poorly (basic queue only), it becomes average and forgettable.

Execution quality is everything.
