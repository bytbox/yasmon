Overview
========
YASMon is system monitoring software designed to monitor both the
local system and an arbitrary number of remote systems.

YASMon can operate either in local mode - acting as a standard system
monitor for the computer on which it is running - or in remote mode,
providing information on an aribtrary number of computers running
YASMond (the YASMon server daemon).

Features
========
* Local monitoring on a system without a YASMond process
* Remote monitoring over an *unsecured* connection
* Viewing (both remote and local) of:

  * CPU usage for multiple processors
  * RAM usage
  * Filesystem usage
  * Uptime
  * Distribution information

* Library for use by other programs
* Qt4-based GUI

Security
========
Please note that all remote monitoring happens over an unsecured
connection, meaning that it is possibly for a large number of
eavesdroppers to see all data you can see on your screen (but not
modify anything), depending on your network connection (obviously, for
connections confined to a properly firewalled LAN or VPN, this is not
the case). Although this is not a problem for most installations (CPU
usage and similar information is usually not dangerous),
administrators should be conscious of this fact. This will be fixed in
future versions of YASMon (openning the way to more detailed
information viewing, as well as remote administration).

By default, YASMon functions on port 61874.

Changes
=======
For a list of changes in this and all previous versions of YASMon,
please see the ``NEWS`` file.

Bugs
====
Current bugs can be viewed in the `issue tracker
<http://github.com/bytbox/yasmon/issues>`__ on github. Bugs and
feature requests may be reported to the same place.

License
=======
YASMon is published under the GNU General Public License version 3 or,
at your option, any later version. In short, this license gives you
permission to use this software for any purpose, provided that you do
not change the license, and do not link it with any software under a
different license.

You can read the full text of the license in the ``COPYING`` file - if
you can find none, see http://www.gnu.org/licenses.

Author
======
YASMon was written by Scott Lawrence <bytbox@gmail.com>.
