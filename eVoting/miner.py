#!/usr/bin/env python

import glob
import cPickle as pickle
import hashlib
from time import time
from threading import Thread


class Miner:

    def __init__(self, blockchain_locks):
        # Locks for controlling access to the blockchains
        self.blockchain_locks = blockchain_locks
        # Initialize thread as daemon
        self.bc_miner_t = Thread(target=self.bc_mine)
        self.bc_miner_t.daemon = True

    # Start daemon thread
    def start(self):
        self.bc_miner_t.start()

    def bc_mine(self):
        while True:
            self.mine_phase_one_blockchains()
            self.mine_phase_two_blockchains()
            self.mine_phase_three_blockchains()

    def mine_phase_one_blockchains(self):
        self.blockchain_locks[0].acquire()
        filed_blockchains = glob.glob("../.blockchains/phase_one/blockchain*.pkl")
        for filed_blockchain in filed_blockchains:
            with open(filed_blockchain, 'rb') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                transactions_block = blockchain.get_transactions_block()
                if len(transactions_block.get_transactions()) > 0:
                    nonce = 0
                    transactions = pickle.dumps(transactions_block.get_transactions())
                    time1 = time()
                    while True:
                        curr_str = transactions + str(nonce)
                        hash = hashlib.sha1(curr_str).hexdigest()
                        if hash.startswith('000'):
                            transactions_block.set_nonce(nonce)
                            transactions_block.set_hash(hash)
                            blockchain_blocks = blockchain.get_chain()
                            if len(blockchain_blocks) == 0:
                                transactions_block.set_prev_hash(0)
                            else:
                                transactions_block.set_prev_hash(blockchain_blocks[-1].get_hash())
                            blockchain.transactions_to_chain()
                            blockchain.add_work(time() - time1)
                            break
                        else:
                            nonce += 1
            with open(filed_blockchain, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)
        self.blockchain_locks[0].release()

    def mine_phase_two_blockchains(self):
        self.blockchain_locks[1].acquire()
        filed_blockchains = glob.glob("../.blockchains/phase_two/blockchain*.pkl")
        for filed_blockchain in filed_blockchains:
            with open(filed_blockchain, 'rb+') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                transactions_block = blockchain.get_transactions_block()
                if len(transactions_block.get_transactions()) > 0:
                    nonce = 0
                    transactions = pickle.dumps(transactions_block.get_transactions())
                    time1 = time()
                    while True:
                        curr_str = transactions + str(nonce)
                        hash = hashlib.sha1(curr_str).hexdigest()
                        if hash.startswith('000'):
                            transactions_block.set_nonce(nonce)
                            transactions_block.set_hash(hash)
                            blockchain_blocks = blockchain.get_chain()
                            if len(blockchain_blocks) == 0:
                                transactions_block.set_prev_hash(0)
                            else:
                                transactions_block.set_prev_hash(blockchain_blocks[-1].get_hash())
                            blockchain.transactions_to_chain()
                            blockchain.add_work(time() - time1)
                            break
                        else:
                            nonce += 1
            with open(filed_blockchain, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)
        self.blockchain_locks[1].release()

    def mine_phase_three_blockchains(self):
        self.blockchain_locks[2].acquire()
        filed_blockchains = glob.glob("../.blockchains/phase_three/blockchain*.pkl")
        for filed_blockchain in filed_blockchains:
            with open(filed_blockchain, 'rb+') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                transactions_block = blockchain.get_transactions_block()
                if len(transactions_block.get_transactions()) > 0:
                    nonce = 0
                    transactions = pickle.dumps(transactions_block.get_transactions())
                    time1 = time()
                    while True:
                        curr_str = transactions + str(nonce)
                        hash = hashlib.sha1(curr_str).hexdigest()
                        if hash.startswith('000'):
                            transactions_block.set_nonce(nonce)
                            transactions_block.set_hash(hash)
                            blockchain_blocks = blockchain.get_chain()
                            if len(blockchain_blocks) == 0:
                                transactions_block.set_prev_hash(0)
                            else:
                                transactions_block.set_prev_hash(blockchain_blocks[-1].get_hash())
                            blockchain.transactions_to_chain()
                            blockchain.add_work(time() - time1)
                            break
                        else:
                            nonce += 1
            with open(filed_blockchain, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)
        self.blockchain_locks[2].release()
