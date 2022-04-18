#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from functools import partial

class MyTopo( Topo ):
    "Tugas SDN04 Finding Shortest Paths."

    def addSwitch( self, name, **opts ):
        kwargs = { 'protocols' : 'OpenFlow13'}
        kwargs.update( opts )
        return super(MyTopo, self).addSwitch( name, **kwargs )

    def __init__( self ):
        # Inisialisasi Topology
        "Custom Topology 3 Switch 6 Host - Topology Ring"
        Topo.__init__( self )

        # Add hosts
        info('*** Add Hosts\n')
        h1 = self.addHost( 'h1',ip='10.1.0.1/8' )
        h2 = self.addHost( 'h2',ip='10.1.0.2/8' )
        h3 = self.addHost( 'h3',ip='10.2.0.3/8' )
        h4 = self.addHost( 'h4',ip='10.2.0.4/8' )
        h5 = self.addHost( 'h5',ip='10.3.0.5/8' )
        h6 = self.addHost( 'h6',ip='10.3.0.6/8' )

	# Add switches
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )
        s5 = self.addSwitch( 's5' )
        s6 = self.addSwitch( 's6' )

        # Add links host to switch
        self.addLink( s1, h1, 1, 1 )
        self.addLink( s2, h2, 1, 1 )
        self.addLink( s3, h3, 1, 1 )
        self.addLink( s4, h4, 1, 1 )
        self.addLink( s5, h5, 1, 1 )
        self.addLink( s6, h6, 1, 1 )
        # Add links switch to switch
        self.addLink( s1, s2, 2, 2 )
        self.addLink( s1, s3, 3, 2 )
        self.addLink( s2, s4, 3, 2 )
        self.addLink( s2, s5, 4, 2 )
        self.addLink( s3, s4, 3, 3 )
        self.addLink( s3, s6, 4, 2 )
        self.addLink( s4, s5, 4, 3 )
        self.addLink( s4, s6, 5, 3 )

def run():
    "The Topology for Server - Round Robin LoadBalancing"
    topo = MyTopo()
    net = Mininet( topo=topo, controller=RemoteController, autoSetMacs=True, autoStaticArp=True, waitConnected=True )
    
    info("\n***Disabling IPv6***\n")
    for host in net.hosts:
        print("disable ipv6 in", host)
        host.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
    
    for sw in net.switches:
        print("disable ipv6 in", sw)
        sw.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")

    info("\n\n************************\n")
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()

