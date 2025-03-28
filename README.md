# Simulation Analysis: Queue Performance & Cost-Efficient Maintenance Strategies

## Overview
This repository contains Python implementations for two simulation problems from the "Principles of Simulation" course at Amirkabir University of Technology. The solutions demonstrate discrete-event simulation techniques for analyzing system performance and cost optimization.

## Contents

### 1. Single-Channel Service Station Simulation
- Models a queue system with one server
- Analyzes customer wait times and server utilization
- Key metrics: average wait time, server idle percentage, system throughput

### 2. Bearing Maintenance Simulation
- Compares two maintenance strategies for industrial equipment:
  1. **Repair Method**: Replace only failed bearings
  2. **Maintenance Method**: Replace all bearings when any fails
- Simulates over 30,000 operating hours
- Includes cost analysis of both approaches

## Files

- `CourseWork1_Q1.ipynb`: Service station simulation (single-server queue)
- `CourseWork1_Q2.ipynb`: Bearing maintenance simulation with comparative analysis
- `Assignment1.pdf`: Original problem statements (in Persian)
- `Report.pdf`: Detailed report (in Persian)

## Key Features

1. **Discrete-Event Simulation Framework**:
   - Future Event List (FEL) management
   - Time-advance mechanism
   - Statistical collection

2. **Probability Distributions**:
   - Custom discrete distributions for failure times
   - Uniform distributions for service times

3. **Performance Analysis**:
   - Cost breakdown visualization
   - 1000-run Monte Carlo simulation
   - Comparative histograms and density plots

4. **Optimization Insights**:
   - Quantifies cost savings from preventive maintenance
   - Analyzes tradeoffs between repair frequency and downtime costs

## Usage

1. Install dependencies:
   ```bash
   pip install numpy pandas matplotlib scipy
   ```

2. Run the Jupyter notebooks:
   ```bash
   jupyter notebook CourseWork1_Q1.ipynb
   jupyter notebook CourseWork1_Q2.ipynb
   ```

## Results Highlights

### Bearing Maintenance Simulation
| Metric                | Repair Method | Maintenance Method |
|-----------------------|---------------|--------------------|
| Average Total Cost    | $16,222       | $12,748            |
| Cost Reduction        | -             | 21.4%              |
| Failure Events        | 67            | 20                 |
| Downtime Minutes      | 1,290         | 1,260              |

![image](https://github.com/user-attachments/assets/634cf8f5-3758-4d0e-97e7-c468c54f20e5)
![image](https://github.com/user-attachments/assets/cabbbd7c-1717-4b3c-883b-16748e473d36)


## Contributors
- Hessam Ebrahimi
- Amirhosein RezaGharebagh  
- Farid Mohammadzadeh (mailto: frdmohammadzadeh@gmail.com)

## License
Academic use only. Unauthorized distribution prohibited.
