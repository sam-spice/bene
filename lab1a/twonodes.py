from __future__ import print_function

import sys

sys.path.append('..')

from bene.network import Network
from bene.sim import Sim
from bene.packet import Packet


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet, **kwargs):
        print((packet.ident,
               packet.created,
               Sim.scheduler.current_time()))


def generic_1packet(file_name):
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network(file_name)

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    # send one packet
    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # run the simulation
    Sim.scheduler.run()

def generic_4packets(file_name):
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network(file_name)

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    # send three packets

    # packet 1
    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # packet 2
    p = Packet(destination_address=n2.get_address('n1'), ident=2, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # packet 3
    p = Packet(destination_address=n2.get_address('n1'), ident=3, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # send 4th delayed packet
    p = Packet(destination_address=n2.get_address('n1'), ident=4, protocol='delay', length=1000)
    Sim.scheduler.add(delay=2, event=p, handler=n1.send_packet)

    # run the simulation
    Sim.scheduler.run()

def main():
    print('***Scenario 1***')
    generic_1packet('../lab1a/networks/fast-long.txt')

    print('***Scenario 2***')
    generic_1packet('../lab1a/networks/slow-short.txt')

    print('***Scenario 3***')
    generic_4packets('../lab1a/networks/fast-short.txt')


if __name__ == '__main__':
    main()
