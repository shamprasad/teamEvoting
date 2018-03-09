#!/usr/bin/env python


class Blockchain:

    def __init__(self, block):
        self.size = 1
        self.chain = [block]

    def add_block(self, block):
        self.chain.append(block)
        self.size += 1

    def get_size(self):
        return self.size

    def get_chain(self):
        return self.chain
