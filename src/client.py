#!/usr/bin/env python

import glob
import cPickle as pickle
import os
from random import randint

from blockchain import Blockchain
from block import Block_Phase_One, Block_Phase_Two, Block_Phase_Three


CANDIDATES = ["Shane Lockwood", "Ankur Jain", "Sham Prasad"]

def phase_one():

    blockchain = 0
    # Find all saved blockchains
    file_names = glob.glob("../blockchains/phase_one/blockchain*.pkl")
    # If no blockchains found
    if len(file_names) == 0:
        # Create blockchain with desired candidates
        block = Block_Phase_One(CANDIDATES)
        blockchain = Blockchain(block)
        random_number = (randint(1000, 9999))
        file_name = "../blockchains/phase_one/blockchain{}.pkl".format(random_number)
        # Write blockchain to file
        with open(file_name, 'wb') as blockchain_file:
            pickle.dump(blockchain, blockchain_file)
    # If blockchains are found
    else:
        largest_chain_size = 0
        largest_file_name = ""
        # Cycle through all blockchains
        for file_name in file_names:
            # Load blockchain
            with open(file_name, 'rb') as blockchain_file:
                match = True
                blockchain = pickle.load(blockchain_file)
                # Cycle through each block in blockchain
                for block in blockchain.get_chain():
                    # If candidates don't match desired candidates,
                    # move to next blockchain
                    for candidate in block.get_candidates():
                        if candidate not in CANDIDATES:
                            match = False
                            break
                        for cand in CANDIDATES:
                            if cand not in block.get_candidates():
                                match = False
                                break
                # Move to next blockchain
                if match == False:
                    match = True
                # If blockchain matches candidates and is larger than prior
                elif blockchain.get_size() > largest_chain_size:
                    largest_file_name = file_name
                    largest_chain_size = blockchain.get_size()
        # If no matching blockchains
        if largest_chain_size == 0:
            # Create blockchain with desired candidates
            block = Block_Phase_One(CANDIDATES)
            blockchain = Blockchain(block)
            random_number = (randint(1000, 9999))
            file_name = "../blockchains/phase_one/blockchain{}.pkl".format(random_number)
            # Write blockchain to file
            with open(file_name, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)
        # If matching blockchain is found
        else:
            # Append desired candidates to blockchain
            with open(largest_file_name, 'rb') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                block = Block_Phase_One(CANDIDATES)
                blockchain.add_block(block)
            # Write blockchain to file
            with open(largest_file_name, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)
    print blockchain.get_size()

if __name__ == '__main__':
    phase_one()
