#!/usr/bin/env python


from random import randint

class Blockchain:

    def __init__(self):
        self.id = randint(1000, 9999)
        self.size = 0
        self.chain = []

    def add_block(self, block):
        self.chain.append(block)
        self.size += 1

    def get_id(self):
        return self.id

    def get_size(self):
        return self.size

    def get_chain(self):
        return self.chain
