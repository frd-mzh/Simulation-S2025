# Factory Tool Lending System Simulation

![image](https://github.com/user-attachments/assets/5d2086b0-3c9b-435c-97aa-240e08eeb10a)

## Project Overview
This project simulates and analyzes the performance of a tool lending system in a factory environment. The simulation models:
- Tool borrowing and return processes
- Maintenance and cleaning operations
- Worker allocation strategies
- Queue management systems

Key metrics analyzed:
- Average customer wait times
- Service time distributions
- Queue lengths
- Resource utilization efficiency

## Team Members
- Farid Mohammadzadeh (40025073)
- Amirhossein Reza Gharebagh (40025024)
- Hessam Ebrahimi (9925076)

**Supervisor:** Dr. Abbas Ahmadi  
**University:** Amirkabir University of Technology (Tehran Polytechnic)  
**Date:** Khordad 1404 (June 2024)

## Key Features
- Discrete-event simulation modeling
- Statistical analysis with confidence intervals
- Three operational scenarios:
  1. Baseline system
  2. Modified worker allocation
  3. Improved system proposal
- Visualization of queue dynamics
- Random number generation with statistical validation

## Technical Components
- **Random Variate Generation**:
  - Linear congruential generator (LCG)
  - Kolmogorov-Smirnov uniformity test
  - Independence testing
- **Statistical Analysis**:
  - Confidence interval estimation
  - Point estimation of performance metrics
  - Distribution fitting
- **Simulation Core**:
  - Future Event List (FEL) implementation
  - State tracking for servers and queues
  - 30-day simulation runs

## How to Run
1. Ensure Python 3.7+ is installed
2. Install required packages:
   ```bash
   pip install numpy scipy matplotlib pandas
