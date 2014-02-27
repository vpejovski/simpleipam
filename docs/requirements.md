= Ipam solution =

This ipam application is an attempt to solve the issues with vm provisioning.
Orchestration engine should reach out to ipam application using rest like
api to acquire ip for specific vm.

It should pass host name and mac address to the application and optionally
network / subnet. ipam will return a single ip4 address.

ipam should store ip address, host name and mac address.

ipam should integrate with dhcp server and create a configuration for
server with ip reservations.

dhcp server should dynamically update dns server.

ipam should also provide an interface for manual reservation of ip's.
reservation record needs to store:
 - ip address
 - user name that made reservation
 - mac address of ff:ff:ff:ff:ff:ff (need to check if dhcp server will
 accept the reservation for this)