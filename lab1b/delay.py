from __future__ import print_function

import sys

sys.path.append('..')

from bene.network import Network
from bene.sim import Sim
from bene.packet import Packet
import random
import csv

class Generator(object):
    def __init__(self, node, destination, load, duration):
        self.node = node
        self.load = load
        self.destination = destination
        self.duration = duration
        self.start = 0
        self.ident = 1

    def handle(self, event):
        # quit if done
        now = Sim.scheduler.current_time()
        if (now - self.start) > self.duration:
            return

        # generate a packet
        self.ident += 1
        p = Packet(destination_address=self.destination, ident=self.ident, protocol='delay', length=1000)
        Sim.scheduler.add(delay=0, event=p, handler=self.node.send_packet)
        # schedule the next time we should generate a packet
        Sim.scheduler.add(delay=random.expovariate(self.load), event='generate', handler=self.handle)


class DelayHandler(object):
    def __init__(self, csv_file):
        self.received = list()
        self.csv_file = csv_file

    def receive_packet(self, packet, **kwargs):
        self.received.append([Sim.scheduler.current_time(), packet.queueing_delay])
        print((Sim.scheduler.current_time(),
               packet.ident,
               packet.created,
               Sim.scheduler.current_time() - packet.created,
               packet.transmission_delay,
               packet.propagation_delay,
               packet.queueing_delay))

    def write_out(self):
        with open(self.csv_file, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['curr_time', 'q_delay'])
            for row in self.received:
                csv_writer.writerow(row)



def generic_3node(p, csv_file_name):
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('../lab1b/networks/fast-fast.txt')

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
    d = DelayHandler(csv_file_name)
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)

    # setup packet gen   erator
    destination = n3.get_address('n2')
    max_rate = 1000000 // (1000 * 8)
    load = p * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=600)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    #write out results
    d.write_out()

def main():
    p_array = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.98]
    for p in p_array:
        csv_file_name = "data/queue-" + "{0:.2f}".format(p) + ".csv"
        generic_3node(p, csv_file_name)

if __name__ == '__main__':
    main()