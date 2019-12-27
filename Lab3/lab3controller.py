# Lab 3 Skeleton
# David Nguyen 
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pprint import pprint 
log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.macToPort = {}

    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
    print "Example Code."
    #print packet 

    #print "/n"

    #print packet_in

    # Get the source and destination MAC, and also the input port
    # for a given packet
  
  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return
    #pprint(vars(event))
    #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    #pprint(vars(packet))
    #print "-----------------------------------------------"



    

    def flood (packet):
      """ Floods the packet """
      #msg = of.ofp_packet_out()
      #msg.data = event.ofp
      #msg.in_port = event.port
      #self.connection.send(msg)
      
      #msg = of.ofp_packet_out()
      #msg.buffer_id = event.ofp.buffer_id
      #msg.in_port = event.port
      #self.connection.send(msg)
      print("installing flow for %s.%i -> %s" %(packet.src, event.port, packet.dst))
      #port = self.macToPort[packet.dst]
      
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 100
      msg.hard_timeout = 200
      msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
      #msg.data = event.ofp # 6a
      self.connection.send(msg)
      
     

    def drop (packet):
      """
      Drops this packet and optionally installs a flow to continue
      dropping similar ones for a while
      """
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 100
      msg.hard_timeout = 200
      msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
      #msg.data = event.ofp # 6a
      self.connection.send(msg)
      
    #checks to see if IP/ARP packet, if IP check if IPv4 and tcp, flood,
    def parse_icmp(eth_packet):
      if eth_packet.find('ip'):
        ip_packet = eth_packet.payload
        if ip_packet.find('ipv4') and ip_packet.find('tcp'):
           print("TCP!!!!!!!!!!!!!!!!!!!!!!!!!1")
           flood(ip_packet)
        else:
          drop(ip_packet)
      elif eth_packet.find('arp'):
        print("ARP!!!!!!!!!!!!!!!!!!!!!!!!!1")
        flood(eth_packet)
      else:
        drop(eth_packet)





        #if ip_packet.protocol == pkt.TCP_PROTOCOL:
         # icmp_packet = ip_packet.payload'''
    self.macToPort[packet.src] = event.port
    sike = parse_icmp(packet)

   

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

    '''if packet.type == packet.TCP: #or packet.type == packet.TCP:
      flood() # 2a
    else:
      drop()'''
'''
    #tcpp = event.parsed.find('tcp')
    aarp = event.parsed.find('arp')
    if aarp: 
      flood()
      return # Not TCP
    else:
      drop()
      return
'''
    



  
  

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)

  core.openflow.addListenerByName("ConnectionUp", start_switch)
