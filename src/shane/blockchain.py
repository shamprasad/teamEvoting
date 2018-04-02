#!/usr/bin/env python


from random import randint

class Blockchain:

    def __init__(self, block):
        self.id = randint(0, 10000)
        self.size = 1
        self.chain = [block]

    def add_block(self, block):
        self.chain.append(block)
        self.size += 1

    def get_id(self):
        return self.id

    def get_size(self):
        return self.size

    def get_chain(self):
        return self.chain
