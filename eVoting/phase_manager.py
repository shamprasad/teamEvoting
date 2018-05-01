#!/usr/bin/env python

from time import sleep
import glob
import cPickle as pickle

from .transaction import (
    PhaseOneTransaction,
    PhaseTwoTransaction,
    PhaseThreeTransaction
)
from .block import Block
from .blockchain import Blockchain


class PhaseManager:

    def __init__(self, blockchain_locks):
        # Locks for controlling access to the blockchains
        self.blockchain_locks = blockchain_locks

        self.desired_voters = [x.lower() for x in ["Shane", "Ankur", "Sham"]]
        self.desired_candidates = [x.lower() for x in ["Shane", "Ankur", "Sham"]]
        # Voter
        self.voter = None
        # Selected candidate
        self.candidate = None
        # Phase one block and blockchain
        # Tally
        self.tally = None
        self.phase_one_transaction = None
        self.phase_one_blockchain = None
        self.phase_one_blockchain_file = None
        # Phase two block and blockchain
        self.phase_two_transaction = None
        self.phase_two_blockchain = None
        self.phase_two_blockchain_file = None
        # Phase three block and blockchain
        self.phase_three_transaction = None
        self.phase_three_blockchain = None
        self.phase_three_blockchain_file = None

#########################################
#######          Phase One       ########
#########################################

    # Method for processing phase one
    def start_phase_one(self):
        # Input voter's name
        self.input_voter_name()
        # Create transaction with desired candidates
        self.phase_one_transaction = PhaseOneTransaction(self.desired_candidates,
                                                         self.desired_voters,
                                                         self.voter)
        while True:
            # Get phase one blockchain from file
            self.get_phase_one_blockchain()
            # Check status of phase one completion
            status = self.check_phase_one_completion()
            # If voter has not appended the accepted blockchain
            # then append transaction to accepted blockchain
            # and save blockchain to file
            if status == "voter hasn't appended this blockchain":
                self.append_transaction_to_phase_one_blockchain()
                # Save phase one blockchain to file
                self.set_phase_one_blockchain()
            # If all desired voters have voted
            # then finish phase one
            # else get phase one blockchain
            elif status == "all voters have voted":
                return self.phase_one_blockchain.get_chain()[0].get_transactions()[0].get_candidates()
            # else wait then get phase one blockchain
            else:
                sleep(5)

    # Method for acquiring voter's name
    def input_voter_name(self):
        while True:
            # Get voter's name
            voter = raw_input("Enter voter's name: ")
            # If name is a desired voter
            # then save name
            if voter.lower() in self.desired_voters:
                self.voter = voter.lower()
                return
            # If name is not a desired voter
            # then ask again for voter's name
            else:
                print 'Voter not a desired voter.'
                continue

    # Method for loading the currently accepted phase one blockchain
    def get_phase_one_blockchain(self):
        # Find all saved phase one blockchains
        self.blockchain_locks[0].acquire()
        file_names = glob.glob("../.blockchains/phase_one/blockchain*.pkl")
        # If no phase one blockchains found
        if len(file_names) == 0:
            # Create phase one blockchain
            self.phase_one_blockchain = Blockchain()
            # Save accepted blockchain file name
            id = self.phase_one_blockchain.get_id()
            self.phase_one_blockchain_file = "../.blockchains/phase_one/blockchain{:04d}.pkl".format(id)
        # If blockchains are found
        else:
            # Search for largest blockchain with desired candidates
            largest_chain_work = 0
            largest_transactions_block = 0
            largest_file_name = ""
            # Cycle through all blockchains
            for file_name in file_names:
                # View blockchain
                with open(file_name, 'rb') as blockchain_file:
                    match = True
                    try:
                        blockchain = pickle.load(blockchain_file)
                    except EOFError, e:
                        continue
                # Cycle through each block in blockchain
                for block in blockchain.get_chain():
                    # Cylce through each transaction in block
                    for transaction in block.get_transactions():
                        # Compare candidates with desired candidates
                        for candidate in transaction.get_candidates():
                            if candidate not in self.desired_candidates or not match:
                                match = False
                                break
                        for candidate in self.desired_candidates:
                            if candidate not in transaction.get_candidates() or not match:
                                match = False
                                break
                        # Compare voters with desired voters
                        for voter in transaction.get_voters():
                            if voter not in self.desired_voters or not match:
                                match = False
                                break
                        for voter in self.desired_voters:
                            if voter not in transaction.get_voters() or not match:
                                match = False
                                break
                        # Verify voter is a desired voter
                        if transaction.get_voter() not in self.desired_voters:
                            match = False
                        # If voters/candidates and desired voters/desired
                        # then break out of transaction loop
                        if not match:
                            break
                    # If voters/candidates and desired voters/desired candidates
                    # then break out of block loop
                    if not match:
                        break
                # If voters/candidates and desired voters/desired
                # candidates don't match move to next blockchain
                if match == False:
                    match = True
                # If blockchain matches desired candidates and is larger than
                # or equal to prior blockchain which matches desired candidates
                # then save blockchain and blockchain file name
                elif blockchain.get_work() > largest_chain_work:
                    self.phase_one_blockchain_file = file_name
                    largest_chain_work = blockchain.get_work()
                    self.phase_one_blockchain = blockchain
                    largest_transactions_block = len(blockchain.get_transactions_block().get_transactions())
                elif blockchain.get_work() == largest_chain_work and \
                        len(blockchain.get_transactions_block().get_transactions()) >= largest_transactions_block:
                    self.phase_one_blockchain_file = file_name
                    largest_chain_work = blockchain.get_work()
                    self.phase_one_blockchain = blockchain
                    largest_transactions_block = len(blockchain.get_transactions_block().get_transactions())
            # If no blockchains with candidates that match desired candidates
            # then save new blockchain and new blockchain file name
            if largest_chain_work == 0 and largest_transactions_block == 0:
                # Create blockchain with desired candidates
                self.phase_one_blockchain = Blockchain()
                # Save accepted blockchain file name
                id = self.phase_one_blockchain.get_id()
                self.phase_one_blockchain_file = "../.blockchains/phase_one/blockchain{:04d}.pkl".format(id)
        self.blockchain_locks[0].release()

    # Method to check if phase one is complete
    def check_phase_one_completion(self):
        # Initialize data structure for checking if every desired voter is in
        # the accepted blockchain
        voters = {}
        # Add every desired voter to dictionary and set to false
        for voter in self.desired_voters:
            voters[voter] = False
        # Set true for every voter committed in blockchain
        for block in self.phase_one_blockchain.get_chain():
            for transaction in block.get_transactions():
                voters[transaction.get_voter()] = True
        # Set true for every voter in transaction
        for transaction in self.phase_one_blockchain.get_transactions_block().get_transactions():
            voters[transaction.get_voter()] = True
        # Verify voter has voted
        for voter in voters:
            if not voters[voter]:
                if voter == self.voter:
                    return "voter hasn't appended this blockchain"
        # Renew dictionary for other voters
        for voter in self.desired_voters:
            voters[voter] = False
        # Set true for every voter committed in blockchain
        for block in self.phase_one_blockchain.get_chain():
            for transaction in block.get_transactions():
                voters[transaction.get_voter()] = True
        # If every voter is true
        # then return true
        # else return false
        for voter in voters:
            if not voters[voter]:
                return "still waiting for another voter"
        return "all voters have voted"

    # Method to append block to blockchain
    def append_transaction_to_phase_one_blockchain(self):
        self.phase_one_blockchain.add_transaction(self.phase_one_transaction)

    # Save blockchain to file
    def set_phase_one_blockchain(self):
        self.blockchain_locks[0].acquire()
        with open(self.phase_one_blockchain_file, 'wb') as file_name:
            pickle.dump(self.phase_one_blockchain, file_name)
        self.blockchain_locks[0].release()

#########################################
#######          Phase Two       ########
#########################################

    # Method for processing phase two
    def start_phase_two(self):
        # Input vote
        self.input_vote()
        # Create transaction with desired candidate
        self.phase_two_transaction = PhaseTwoTransaction(self.candidate, self.voter)
        while True:
            # Get phase two blockchain from file
            self.get_phase_two_blockchain()
            # Check status of phase one completion
            status = self.check_phase_two_completion()
            # If voter has not appended the accepted blockchain
            # then append transaction to accepted blockchain
            # and save blockchain to file
            if status == "voter hasn't appended this blockchain":
                self.append_transaction_to_phase_two_blockchain()
                # Save phase two blockchain to file
                self.set_phase_two_blockchain()
            # If all desired voters have voted
            # then finish phase one
            # else get phase one blockchain
            elif status == "all voters have voted":
                return
            # else wait then get phase one blockchain
            else:
                sleep(5)

    # Method for acquiring vote
    def input_vote(self):
        while True:
            # Get vote
            candidate = raw_input("Enter vote: ")
            # If candidate is a desired candidate
            # then save candidate
            if candidate.lower() in self.desired_voters:
                self.candidate = candidate.lower()
                return
            # If name is not a desired candidate
            # then ask again for candidate
            else:
                print 'Candidate not a desired candidate.'
                continue

    # Method for loading the currently accepted phase two blockchain
    def get_phase_two_blockchain(self):
        # Find all saved phase two blockchains
        self.blockchain_locks[1].acquire()
        file_names = glob.glob("../.blockchains/phase_two/blockchain*.pkl")
        # If no phase two blockchains found
        if len(file_names) == 0:
            # Create blockchain with desired candidates
            self.phase_two_blockchain = Blockchain()
            # Save accepted blockchain file name
            id = self.phase_two_blockchain.get_id()
            self.phase_two_blockchain_file = "../.blockchains/phase_two/blockchain{:04d}.pkl".format(id)
        # If blockchains are found
        else:
            # Search for largest blockchain with desired candidates
            largest_chain_work = 0
            largest_transactions_block = 0
            largest_file_name = ""
            # Cycle through all blockchains
            for file_name in file_names:
                # View blockchain
                with open(file_name, 'rb') as blockchain_file:
                    try:
                        blockchain = pickle.load(blockchain_file)
                        # If blockchain is larger than or equal to prior blockchain
                        # then save blockchain and blockchain file name
                        if blockchain.get_work() > largest_chain_work:
                            self.phase_two_blockchain_file = file_name
                            largest_chain_work = blockchain.get_work()
                            self.phase_two_blockchain = blockchain
                        elif blockchain.get_work() == largest_chain_work and \
                                len(blockchain.get_transactions_block().get_transactions()) >= largest_transactions_block:
                            self.phase_two_blockchain_file = file_name
                            largest_chain_work = blockchain.get_work()
                            self.phase_two_blockchain = blockchain
                            largest_transactions_block = len(blockchain.get_transactions_block().get_transactions())
                    except EOFError, e:
                        pass
        self.blockchain_locks[1].release()

    # Method to check if phase two is complete
    def check_phase_two_completion(self):
        # Initialize data structure for checking if every desired voter is in
        # the accepted blockchain
        voters = {}
        # Add every desired voter to dictionary and set to false
        for voter in self.desired_voters:
            voters[voter] = False
        # Set true for every voter committed in blockchain
        for block in self.phase_two_blockchain.get_chain():
            for transaction in block.get_transactions():
                voters[transaction.get_voter()] = True
        # Set true for every voter in transaction
        for transaction in self.phase_two_blockchain.get_transactions_block().get_transactions():
            voters[transaction.get_voter()] = True
        # Verify voter has voted
        for voter in voters:
            if not voters[voter]:
                if voter == self.voter:
                    return "voter hasn't appended this blockchain"
        # Renew dictionary for other voters
        for voter in self.desired_voters:
            voters[voter] = False
        # Set true for every voter committed in blockchain
        for block in self.phase_two_blockchain.get_chain():
            for transaction in block.get_transactions():
                voters[transaction.get_voter()] = True
        # If every voter is true
        # then return true
        # else return false
        for voter in voters:
            if not voters[voter]:
                return "still waiting for another voter"
        return "all voters have voted"

    # Method to append transaction to blockchain
    def append_transaction_to_phase_two_blockchain(self):
        self.phase_two_blockchain.add_transaction(self.phase_two_transaction)

    # Save blockchain to file
    def set_phase_two_blockchain(self):
        self.blockchain_locks[1].acquire()
        with open(self.phase_two_blockchain_file, 'wb') as file_name:
            pickle.dump(self.phase_two_blockchain, file_name)
        self.blockchain_locks[1].release()

#########################################
######          Phase Three       #######
#########################################

    # Method for processing phase three
    def start_phase_three(self):
        # Tally votes from phase two blockchain
        self.tally_votes()
        # Create transaction with tally
        self.phase_three_transaction = PhaseThreeTransaction(self.tally, self.voter)
        while True:
            # Get phase three blockchain from file
            self.get_phase_three_blockchain()
            # Check status of phase three completion
            status = self.check_phase_three_completion()
            # If voter has not appended the accepted blockchain
            # then append block to accepted blockchain
            # and save blockchain to file
            if status == "voter hasn't appended this blockchain":
                self.append_block_to_phase_three_blockchain()
                # Save phase three blockchain to file
                self.set_phase_three_blockchain()
            # If all desired voters have voted
            # then finish phase one
            # else get phase one blockchain
            elif status == "all voters have voted":
                return self.phase_three_blockchain.get_chain()[0].get_transactions()[0].get_tally()
            # else wait then get phase three blockchain
            # wait to allow time for the blockchains to be shared among peers
            else:
                sleep(5)

    # Tally the votes in the accepted phase two blockchain
    def tally_votes(self):
        # Initialize dictionary with 0 votes for each candidate
        self.tally = {}
        for candidate in self.desired_candidates:
            self.tally[candidate] = 0
        # Tally votes for each candidate
        for block in self.phase_two_blockchain.get_chain():
            for transaction in block.get_transactions():
                self.tally[transaction.get_candidate()] += 1

    # Method for loading the currently accepted phase three blockchain
    def get_phase_three_blockchain(self):
        # Find all saved phase three blockchains
        self.blockchain_locks[2].acquire()
        file_names = glob.glob("../.blockchains/phase_three/blockchain*.pkl")
        # If no phase three blockchains found
        if len(file_names) == 0:
            # Create phase three blockchain
            self.phase_three_blockchain = Blockchain()
            # Save accepted blockchain file name
            id = self.phase_three_blockchain.get_id()
            self.phase_three_blockchain_file = "../.blockchains/phase_three/blockchain{:04d}.pkl".format(id)
        # If blockchains are found
        else:
            # Search for largest blockchain with same tally
            largest_chain_work = 0
            largest_transactions_block = 0
            largest_file_name = ""
            # Cycle through all blockchains
            for file_name in file_names:
                # View blockchain
                with open(file_name, 'rb') as blockchain_file:
                    match = True
                    try:
                        blockchain = pickle.load(blockchain_file)
                    except EOFError, e:
                        continue
                # Cycle through each block in blockchain
                for block in blockchain.get_chain():
                    # Cycle through each transaction in block
                    for transaction in block.get_transactions():
                        # Verify all accepted candidates exist in tally
                        for candidate in transaction.get_tally():
                            if candidate not in self.desired_candidates:
                                match = False
                                break
                            # Verify candidate has the same tally as local tally
                            if self.tally[candidate] != transaction.get_tally()[candidate]:
                                match = False
                                break
                        # Verify voter is a desired voter
                        if transaction.get_voter() not in self.desired_voters:
                            match = False
                        # If voters/tally and desired voters/tally
                        # then break out of transaction loop
                        if not match:
                            break
                    # If tally isn't a match with local tally
                    # then stop verifying blockchain
                    if not match:
                        break
                # If candidates don't match desired candidates,
                # then move to next blockchain
                if match == False:
                    match = True
                # If blockchain matches tally and is larger than or equal to
                # prior blockchain which matches tally
                # then save blockchain and blockchain file name
                elif blockchain.get_work() > largest_chain_work:
                    self.phase_three_blockchain_file = file_name
                    largest_chain_work = blockchain.get_work()
                    self.phase_three_blockchain = blockchain
                elif blockchain.get_work() == largest_chain_work and \
                        len(blockchain.get_transactions_block().get_transactions()) >= largest_transactions_block:
                    self.phase_three_blockchain_file = file_name
                    largest_chain_work = blockchain.get_work()
                    self.phase_three_blockchain = blockchain
                    largest_transactions_block = len(blockchain.get_transactions_block().get_transactions())
            # If no blockchains with tally that match local tally
            # then save new blockchain and new blockchain file name
            if largest_chain_work == 0:
                # Create phase three blockchain
                self.phase_three_blockchain = Blockchain()
                # Save accepted blockchain file name
                id = self.phase_three_blockchain.get_id()
                self.phase_three_blockchain_file = "../.blockchains/phase_three/blockchain{:04d}.pkl".format(id)
        self.blockchain_locks[2].release()

    # Method to check if phase three is complete
    def check_phase_three_completion(self):
        # Initialize data structure for checking if every desired voter is in
        # the accepted blockchain
        voters = {}
        # Add every desired voter to dictionary and set to false
        for voter in self.desired_voters:
            voters[voter] = False
        # Set true for every voter committed in blockchain
        for block in self.phase_three_blockchain.get_chain():
            for transaction in block.get_transactions():
                voters[transaction.get_voter()] = True
        # Set true for every voter in transaction
        for transaction in self.phase_three_blockchain.get_transactions_block().get_transactions():
            voters[transaction.get_voter()] = True
        # Verify voter has voted
        for voter in voters:
            if not voters[voter]:
                if voter == self.voter:
                    return "voter hasn't appended this blockchain"
        # Renew dictionary for other voters
        for voter in self.desired_voters:
            voters[voter] = False
        # Set true for every voter committed in blockchain
        for block in self.phase_three_blockchain.get_chain():
            for transaction in block.get_transactions():
                voters[transaction.get_voter()] = True
        # If every voter is true
        # then return true
        # else return false
        for voter in voters:
            if not voters[voter]:
                return "still waiting for another voter"
        return "all voters have voted"

    # Method to append block to blockchain
    def append_block_to_phase_three_blockchain(self):
        self.phase_three_blockchain.add_transaction(self.phase_three_transaction)

    # Save blockchain to file
    def set_phase_three_blockchain(self):
        self.blockchain_locks[2].acquire()
        with open(self.phase_three_blockchain_file, 'wb') as file_name:
            pickle.dump(self.phase_three_blockchain, file_name)
        self.blockchain_locks[2].release()
