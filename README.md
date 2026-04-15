# Simple QoS Priority Controller using SDN

## Problem Statement

In traditional networks, all traffic is treated equally regardless of its importance. This causes issues for latency-sensitive applications like video calls or real-time communication.

**Software Defined Networking (SDN)** solves this by separating the control plane (decision making) from the data plane (packet forwarding), allowing a central controller to manage traffic programmatically.

**Quality of Service (QoS)** in SDN enables prioritization of certain traffic types over others. This project implements a Simple QoS Priority Controller that:
- Identifies different traffic types (ICMP vs other traffic)
- Assigns priority levels using OpenFlow flow rules
- Installs priority rules on a virtual switch
- Measures and compares latency impact

---

## Tools & Requirements

| Tool | Version |
|------|---------|
| Ubuntu (VMware) | 22.04 |
| Mininet | 2.3.0 |
| POX Controller | 0.7.0 (gar) |
| Open vSwitch | Latest |
| Python | 3.10 |
| Git | 2.34.1 |

---

## Setup & Installation

### Step 1 — Update System
```bash
sudo apt-get update
```

### Step 2 — Install Mininet
```bash
sudo apt install mininet -y
```

### Step 3 — Install Open vSwitch
```bash
sudo apt-get install openvswitch-switch
```

### Step 4 — Clone POX Controller
```bash
cd ~/Desktop && git clone https://github.com/noxrepo/pox
```

### Step 5 — Add QoS Controller file
```bash
nano ~/Desktop/pox/pox/forwarding/qos_controller.py
```
Paste the code from `qos_controller.py` in this repository.

---

## Execution Steps

### Terminal 1 — Start POX Controller
```bash
cd ~/Desktop/pox
python3 pox.py forwarding.qos_controller
```

### Terminal 2 — Start Mininet
```bash
sudo mn --controller=remote --topo=single,3
```

### Test Connectivity
```bash
pingall
```

### Measure Latency
```bash
h1 ping -c 5 h2
h1 ping -c 5 h3
```

### Exit Mininet
```bash
exit
```

---

## Expected Output

**POX Controller:**
