
# Simple QoS Priority Controller using SDN

## Problem Statement

In traditional networks, all traffic is treated equally regardless of its importance. This causes issues for latency-sensitive applications like video calls or real-time communication.

**Software Defined Networking (SDN)** separates the control plane from the data plane, allowing a central controller to manage traffic programmatically. This project implements a Simple QoS Priority Controller that identifies traffic types, assigns priority levels, installs rules on a virtual switch, and measures latency impact.

---

## Tools & Requirements

| Tool | Version |
|------|---------|
| Ubuntu (VMware) | 22.04 |
| Mininet | 2.3.0 |
| POX Controller | 0.7.0 (gar) |
| Python | 3.10 |

---

## Setup & Execution Steps

```bash
# Step 1 - Update system
sudo apt-get update

# Step 2 - Install Mininet
sudo apt install mininet -y

# Step 3 - Install Open vSwitch
sudo apt-get install openvswitch-switch

# Step 4 - Clone POX
cd ~/Desktop && git clone https://github.com/noxrepo/pox

# Step 5 - Add QoS controller file
nano ~/Desktop/pox/pox/forwarding/qos_controller.py
```

**Terminal 1 — Start POX Controller:**
```bash
cd ~/Desktop/pox
python3 pox.py forwarding.qos_controller
```

**Terminal 2 — Start Mininet:**
```bash
sudo mn --controller=remote --topo=single,3
```

**Run Tests:**
```bash
pingall
h1 ping -c 5 h2
h1 ping -c 5 h3
```

---

## POX Controller Code

```python
from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr

log = core.getLogger()

HIGH_PRIORITY = 100
LOW_PRIORITY = 10

class QoSController(object):
    def __init__(self):
        core.openflow.addListeners(self)
        log.info("QoS Controller started!")

    def _handle_ConnectionUp(self, event):
        log.info("Switch connected: %s", dpidToStr(event.dpid))
        self.install_qos_rules(event)

    def install_qos_rules(self, event):
        # High priority for ICMP traffic
        msg = of.ofp_flow_mod()
        msg.priority = HIGH_PRIORITY
        msg.match.dl_type = 0x0800
        msg.match.nw_proto = 1
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("High priority rule installed for ICMP traffic")

        # Low priority for all other traffic
        msg = of.ofp_flow_mod()
        msg.priority = LOW_PRIORITY
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("Low priority rule installed for all other traffic")

def launch():
    core.registerNew(QoSController)
```

---

## Expected Output & Results

**POX Controller:**
```
INFO:forwarding.qos_controller:QoS Controller started!
INFO:core:POX 0.7.0 (gar) is up.
INFO:forwarding.qos_controller:High priority rule installed for ICMP traffic
INFO:forwarding.qos_controller:Low priority rule installed for all other traffic
```

**Pingall Result:**
```
*** Results: 0% dropped
```

**Latency Results:**

| Test | Min (ms) | Avg (ms) | Max (ms) | Std Dev (ms) |
|------|----------|----------|----------|--------------|
| h1 → h2 (High Priority ICMP) | 0.090 | 0.293 | 0.921 | 0.314 |
| h1 → h3 (Low Priority Other) | 0.121 | 0.248 | 0.578 | 0.169 |

---

## Proof of Execution

### POX Controller Running
![POX Controller](screenshots/pox_running.png)!)<img width="397" height="97" alt="Screenshot 2026-04-12 173504" src="https://github.com/user-attachments/assets/f52067fb-816f-48a5-b2cb-3a4f573cffde" />



### Pingall Results  
![Pingall](screenshots/pingall_results.png)<img width="268" height="57" alt="Screenshot 2026-04-12 174619" src="https://github.com/user-attachments/assets/8cc365bb-c05e-46f3-8d32-0cccb256d3a2" />

### H1 to H2 Ping (High Priority)
![H1 H2](screenshots/h1_h2_ping.png)<img width="323" height="105" alt="Screenshot 2026-04-12 175150" src="https://github.com/user-attachments/assets/eb1b09ab-156f-4b7b-9e9d-848278a3d063" />


### H1 to H3 Ping (Low Priority)
![H1 H3](screenshots/h1_h3_ping.png)<img width="308" height="108" alt="Screenshot 2026-04-12 174646" src="https://github.com/user-attachments/assets/9bb15bde-eb4f-4be5-af77-1f11290b1c37" />

---

## References

1. POX SDN Controller — https://noxrepo.github.io/pox-doc/html/
2. Mininet — http://mininet.org/
3. OpenFlow Specification — https://opennetworking.org/
4. SDN: Software Defined Networks — Thomas D. Nadeau & Ken Gray
