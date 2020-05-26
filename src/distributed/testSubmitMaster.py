"""
Joshua Stough
W&L, Image Group
July 2011
This script tests the submitMaster and the JobDistributor. 
I'm going to ask for the execution of testScript, which is a
unix shell script that resolves the hostname and stuff like 
that, make sure we have everything working. 
[you@somewhere distributedPythonCode]$ python testSubmitMaster.py


 License: This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or (at your
 option) any later version. This program is distributed in the hope that it
 will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
 Public License for more details.
"""

from submitMaster import *
import os

#Generate some commands.
#The extra double quotes in this commented-out set created problems:  the host
#thought the command to execute was "./testScript 'testing'" with the quotes,
#but no such file or directory is found.
#commands = ["\"./testScript 'Testing Process number %i'" % (number) + "\" &> output%i.out" % (number) \
#            for number in range(4)]
#This became wrong when I stopped using shlex to split the command in
#JobDistributor.

"""
Get current dir, so we can we can cd to that in our command.
Again, as described in submitMaster and JobDistributor, it is
our responsibility to generate the line as it should be executed
on the host machines.
"""
curDir = os.path.abspath('.')
commands = ["cd %s; ./testScript 'Testing Process number %i'" % (curDir, number) + \
            " &> output%i.out" % (number) \
            for number in range(50)]

#for comm in commands:
#    print(comm)
processCommandsInParallel(commands)
