"""
Joshua Stough
CS112, Fundamentals of Programming II (Python)

A built-in list-based queue.

 License: This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or (at your
 option) any later version. This program is distributed in the hope that it
 will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
 Public License for more details.
"""


class listQueue(object):
    def __init__(self, size = 1):
        self.data = list(range(size))
        self.f = 0
        self.b = 0
        self.size = size
        self.length = 0

    def enqueue(self, item):
        self.data[self.b] = item
        self.b += 1
        self.b %= self.size

        self.length += 1

        if self.f == self.b:  #Can't add any more.
            self.expand()


    def dequeue(self):
        t = self.data[self.f]
        self.f += 1
        self.f %= self.size
        
        self.length -= 1

        if self.length < self.size/4.0 and self.length > 2:
            #Have 4x more space than required. The length > 2 check is just
            #that I don't care if there are 2 elements in the queue and 8 spaces
            #in the list.
            self.contract()

        return t

    def peek(self):
        return self.data[self.f]

    def expand(self):
        #This only gets called when f == b.
        temp = list(self.data[self.f:] + self.data[:self.b] + list(range(self.size)))
        #Make sure the state is valid.
        self.data = temp
        self.f = 0
        self.b = self.length
        self.size *= 2

    def contract(self):
        #Happens only when the length 1/4 of the size
        if self.f <= self.b:
            temp = list(self.data[self.f:self.b] + list(range(self.length)))
        else:
            temp = list(self.data[self.f:] + self.data[:self.b] + list(range(self.length)))
        self.data = temp
        self.size = 2*self.length
        self.f = 0
        self.b = self.length

    def __str__(self):
        if self.f <= self.b:
            return str(self.data[self.f:self.b])
        else:
            return str(self.data[self.f:] + self.data[:self.b])

    def __len__(self):
        return self.length

    def isEmpty(self):
        return len(self) == 0
    

    

    
