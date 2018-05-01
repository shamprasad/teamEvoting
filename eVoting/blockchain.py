#!/usr/bin/env python

from random import randint

from .block import Block

class Blockchain:

    def __init__(self):
        self.id = randint(0, 9999)
        self.transactions_block = Block()
        self.chain = []
        self.work = 0

    def add_transaction(self, transaction):
        self.transactions_block.add_transaction(transaction)

    def transactions_to_chain(self):
        self.chain.append(self.transactions_block)
        self.transactions_block = Block()

    def get_id(self):
        return self.id

    def get_work(self):
        return self.work

    def get_transactions_block(self):
        return self.transactions_block

    def get_chain(self):
        return self.chain

    def add_work(self, work):
        self.work += work
