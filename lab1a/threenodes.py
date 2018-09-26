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
               Sim.scheduler.current_time(),
               Sim.scheduler.current_time() - packet.created,
               packet.transmission_delay,
               packet.propagation_delay,
               packet.queueing_delay))


def generic_3node(file_name, time_to_send_packet):
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network(file_name)

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')

    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n1.add_forwarding_entry(address=n3.get_address('n2'), link=n1.links[0])

    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

    n2.add_forwarding_entry(address=n3.get_address('n2'), link=n2.links[1])
    n3.add_forwarding_entry(address=n2.get_address('n3'), link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)

    # send 10,000 packets
    for i in range(1, 10001):
        p = Packet(destination_address=n3.get_address('n2'), ident=i, protocol='delay', length=1000)
        calc_delay = (i - 1) * time_to_send_packet
        Sim.scheduler.add(delay=calc_delay, event=p, handler=n1.send_packet)




    # run the simulation
    Sim.scheduler.run()

def main():
    ('***Scenario 1***')
    single_packet_time = 1000.00 / (10.00 ** 6)
    generic_3node('../lab1a/networks/fast-fast.txt', single_packet_time)

    ('***Scenario 2***')
    single_packet_time = 1000.00 / (10.00 ** 9)
    generic_3node('../lab1a/networks/faster-faster.txt', single_packet_time)

    ('***Scenario 3***')
    single_packet_time = 1000.00 / (10.00 ** 6)
    generic_3node('../lab1a/networks/fast-slow.txt', single_packet_time)

if __name__ == '__main__':
    main()