'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of # POX convention
import pox.lib.packet as pkt # POX convention
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr, IPAddr
from collections import namedtuple
import os
import csv



log = core.getLogger()
# policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ['HOME']

''' Add your global variables here ... '''
firewall_policies = []

class Firewall (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Proxy Controller Module")
        # with open(policyFile, 'rb') as csvfile:
        #     for row in csv.DictReader(csvfile):
        #         firewall_policy = (row['id'], EthAddr(row['mac_0']), EthAddr(row['mac_1'])) 
        #         firewall_policies.append(firewall_policy)
        #         print firewall_policy


    def _handle_ConnectionUp(self, event):
        ''' Add your logic here ... '''
        msg = of.ofp_flow_mod()
        # msg.match = of.ofp_match(in_port=1, tp_dst=80, nw_proto=6)
        msg.match.in_port = 1
        msg.match.dl_type = pkt.ethernet.IP_TYPE   # or 0x800
        msg.match.tp_dst = 80
        msg.match.nw_proto = 6
        msg.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr("10.0.0.2")))
        msg.actions.append(of.ofp_action_dl_addr.set_dst(EthAddr("00:00:00:00:00:02")))
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)
        log.debug("Flow rule installed")

        msg = of.ofp_flow_mod()
        # msg.match = of.ofp_match(in_port=1, tp_dst=80, nw_proto=6)
        msg.match.in_port = 2
        msg.match.dl_type = pkt.ethernet.IP_TYPE   # or 0x800
        # msg.match.tp_dst = 80
        msg.match.nw_proto = 6
        msg.actions.append(of.ofp_action_nw_addr.set_src(IPAddr("128.30.52.45")))
        # msg.actions.append(of.ofp_action_dl_addr.set_dst(EthAddr("00:00:00:00:00:02")))
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)
        log.debug("Flow rule installed")

        # for firewall_policy in firewall_policies:
        #     msg = of.ofp_flow_mod()
        #     msg.match = of.ofp_match(dl_src = firewall_policy[1], dl_dst = firewall_policy[2])
        #     # msg.actions.append(of.ofp_action_output()) # No action = Drop Packets
        #     msg.priority = 65535
        #     event.connection.send(msg)
  
        # log.info("Firewall rules installed on %s", dpidToStr(event.dpid))


def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
