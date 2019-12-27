# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pprint import pprint

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id, event):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    #pprint(vars(packet_in))
    if packet.find('ip') or packet.find('ipv4') or packet.find('ipv6'):
      ip_packet = packet.payload
        #if ip_packet.find('ipv4') and ip_packet.find('tcp'):
      print("IIIIIIIIIIIIIIIIIIIIIIIIIIPPPPPPPPPPPPPPPP")
      if packet.payload.find('tcp') or packet.find('tcp'):
        print("TCCCCCCCCCCCPPPPPPPPPPPPPPPPPP")
      if packet.payload.find('icmp') or packet.find('icmp'):
         print("ICCCCCCCCCCCCCMMMMMMMMMMMMMMMMMMMMMMMP")
      #self.send(packet,of.OFPP_FLOOD, packet_in, event)

      
      #check if source ip is from h4 
      if (str(packet.payload.srcip) == '123.45.67.89'):
        #self.drop(self, packet, event)
        pass
      else:
        #pprint(packet_in,of.OFPP_FLOOD)
        #self.send(packet, 0, packet_in, event)
        #self.send(packet_in, 0,  packet_in, event)



        
        self.send(packet_in,65531, packet_in, event)

        #if packet does not work with 
        #self.send(packet_in,of.OFPP_FLOOD, packet_in, event)





        '''
        if (str(packet.payload.dstip) == '10.1.1.10'):
          self.send(packet, 0, packet_in, event)
        elif (str(packet.payload.dstip) == '10.2.2.20'):
          self.send(packet, 2, packet_in, event)
        elif (str(packet.payload.dstip) == '10.3.3.30'):
          self.send(packet, 3, packet_in, event)
        elif (str(packet.payload.dstip) == '10.5.5.50'):
         self.send(packet_in,65531, packet_in, event)
        '''


      pprint(vars(packet.payload))
        #else:
        #  drop(ip_packet)
    elif packet.find('icmp'):
      print("ICCCCCCCCCCCCCMMMMMMMMMMMMMMMMMMMMMMMP")
      if (str(packet.payload.srcip) == '123.45.67.89'):
        #self.drop(self, packet, event)
        pass
      else:
        self.send(packet_in,of.OFPP_FLOOD, packet_in, event)
      #pprint(vars(packet.payload))
    elif packet.find('arp'):
      print("ARP!!!!!!!!!!!!!!!!!!!!!!!!!1")
      self.send(packet,of.OFPP_FLOOD, packet_in, event)
      #pprint(vars(packet.payload))
    else:
      #drop(eth_packet)
      #pprint(vars(packet))
      self.send(packet,of.OFPP_FLOOD, packet_in, event)
      print("EXTRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
      #pprint(vars(packet.payload))

    
    

  '''
  def drop (self, packet, event):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 100
    msg.hard_timeout = 600
    msg.buffer_id = event.ofp.buffer_id
    msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
    self.connection.send(msg)
  '''

  def send (self, packet, dest_port, packet_in, event):
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 100
      msg.hard_timeout = 300
      msg.data = packet_in 

      #msg.data = event.ofp 
      #pprint(vars(packet))
      msg.buffer_id = event.ofp.buffer_id
      pprint("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
      print(dest_port)
      msg.actions.append(of.ofp_action_output(port = dest_port))
      self.connection.send(msg)



  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    print("---------------------------------------------------")
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid, event)


def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
