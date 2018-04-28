Device WWN
==========

This package provide a simple way to manipulate Fibre Channel WWN in a
SAN Storage environment with decoding capabilities. Most of storage
manufacturers encodes some information in the WWN of their equipment
(serials numbers, directors names, etc.).

This package can extract these information for the following devices :

-  EMC Symmetrix DMX, VMAX and VMAX3
-  EMC VPLEX
-  NetApp FAS

**Pull requests are welcome ! :-)**

Create a WWN
------------

You can create your WWN objects with a dedicated factory method. The
return type will WWN or the specific type of the manufacturer (if
available) :

::

   >>> from devicewwn.factory import WWNFactory
   >>> factory = WWNFactory()
   >>> wwn1 = factory.create("10000000c9907a92")
   >>> wwn1
   <WWN(10:00:00:00:c9:90:7a:92)>
   >>>
   >>>
   >>> wwn2 = factory.create("50:00:09:72:08:13:49:AD")
   >>> wwn2
   <EmcVmaxWWN(50:00:09:72:08:13:49:ad)>

**You can use ‘:’ as separator (or not) between the bytes of your WWN**.
Example: 50000972081349AD or 50:00:09:72:08:13:49:ad are accepted

This package supports also the use of WWN objects called ‘Device WWN’
(compliant IEEE NAA6) used to identify a specific LUN in many devices.

::

   >>> from devicewwn.vendors.EMC.Symmetrix import EmcVmaxWWN
   >>> wwn = EmcVmaxWWN('6006048000018790064853594d353844')
   >>> wwn
   <EmcDmxWWN(60:06:04:80:00:01:87:90:06:48:53:59:4d:35:38:44)>
   >>>

Compare WWN
-----------

The comparison between WWN is also possible (even between an WWN object
and a string) :

::

   >>> from devicewwn.factory import WWNFactory
   >>> factory = WWNFactory()
   >>> wwn1 = factory.create('50000972081349AD')
   >>> wwn2 = factory.create('50000972081349AD')
   >>> wwn1 == wwn2
   True
   >>> wwn1 == '50000972081349AD'
   True
   >>>

Extract the information encoded in a WWN
----------------------------------------

Some manufacturers encode information in the WWNs of their equipments.
These information are not the same between manufacturers but,
generally, you can obtain the serial number of your device, a port or a
director port number (very useful to identify easily an equipment on
your network).

The property ‘decode’ of the WWN class is used to extract these
informations (if available)

::

   >>> from devicewwn.factory import WWNFactory
   >>> factory = WWNFactory()
   >>> wwn = factory.create('50000972081349AD')
   >>> wwn.decode
   'VMAX-20K S/N:HK192601234 Dir:12G Port:1'

The decode property can be also used with the WWNs NAA6 to obtain
specific informations (very useful with the Symmetrix arrays):

::

   >>> from devicewwn.vendors.EMC.Symmetrix import EmcVmaxWWN
   >>> wwn = EmcVmaxWWN('60000970000292605199533030384638')
   >>> wwn.decode
   'VMAX S/N:000292605199 HVE:08F8'
   >>>

Useful properties
-----------------

Another properties are available :

-  oui : extract the OUI (Organization Unique Identifier) of the WWN
-  wwn_nodots : display the WWN without ‘:’ in the string
-  wwn_to_binary : convert the WWN to binary form

::

   >>> wwn.oui
   '00:60:48'
   >>> wwn.wwn_nodots
   '5006048accc86a32'
   >>> wwn.wwn_to_binary
   '101000000000110000001001000101011001100110010000110101000110010'

License
-------

See LICENSE file for more information.
