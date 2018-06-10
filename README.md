# About

I wanted nice graphs in observium displaying the line voltage. The data is collected by the network ups tools (NUT) by calling `upsc ups@host input.voltage`.

net-snmps extend-directive isn't sufficient, as it creates subtables. Therefore, the pass_persist directive is used to override some lm-sensors-oids.

# Install

1. Modify the command in pass.py (l. 56-56), so that the input voltage is printed to stdout by the external programm.
2. Copy pass.py to /usr/local/bin
3. Add a pass_persist directive to your snmpd.conf or use this snmpd.conf, which is a minimal working example.
4. Restart snmpd - done!

5. If you're using observium, you probably need to rediscover the server. After that, there should be a Voltage-Tab in the 'Health-Section', displaying the input-voltage of your UPS. :)

Of course, this script could also be used to 'inject' other values in the snmp-output of a server. If this is your plan, be aware that the *Subtree*-Class needs a sorted table of OIDs. Also, it doesn't build a tree, but instead does string-matching. This is ok for a small amount of custom OIDs.
