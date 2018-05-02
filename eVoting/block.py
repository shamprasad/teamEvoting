#!/usr/bin/env python


class Block:

    def __init__(self):
        self.transactions = []
        self.hash = 0
        self.prev_hash = 0
        self.nonce = None

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def get_hash(self):
        return self.hash

    def get_prev_hash(self):
        return self.prev_hash

    def set_hash(self, hash):
        self.hash = hash

    def set_prev_hash(self, hash):
        self.prev_hash = hash

    def set_nonce(self, nonce):
        self.nonce = nonce
