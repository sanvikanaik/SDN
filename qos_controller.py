from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr

log = core.getLogger()

# Priority levels
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
        # Rule 1: High priority for ICMP (ping) traffic
        msg = of.ofp_flow_mod()
        msg.priority = HIGH_PRIORITY
        msg.match.dl_type = 0x0800
        msg.match.nw_proto = 1  # ICMP
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("High priority rule installed for ICMP traffic")

        # Rule 2: Low priority for all other traffic
        msg = of.ofp_flow_mod()
        msg.priority = LOW_PRIORITY
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("Low priority rule installed for all other traffic")

def launch():
    core.registerNew(QoSController)
