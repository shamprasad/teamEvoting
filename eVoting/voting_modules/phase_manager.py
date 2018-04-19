#!/usr/bin/env python

from time import sleep
import glob
import cPickle as pickle

from eVoting.data_structures import (
    PhaseOneBlock,
    PhaseTwoBlock,
    PhaseThreeBlock,
    Blockchain
)


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
        self.tally = {}
        self.phase_one_block = None
        self.phase_one_blockchain = None
        self.phase_one_blockchain_file = None
        # Phase two block and blockchain
        self.phase_two_block = None
        self.phase_two_blockchain = None
        self.phase_two_blockchain_file = None
        # Phase three block and blockchain
        self.phase_three_block= None
        self.phase_three_blockchain = None
        self.phase_three_blockchain_file = None

#########################################
#######          Phase One       ########
#########################################

    # Method for processing phase one
    def start_phase_one(self):
        # Input voter's name
        self.input_voter_name()
        # Create block with desired candidates
        self.phase_one_block = PhaseOneBlock(self.desired_candidates, self.desired_voters, self.voter)
        status = "voter hasn't appended this blockchain"
        # Get phase one blockchain from file
        self.get_phase_one_blockchain()
        while True:
            # If voter has not appended the accepted blockchain
            # then append block to accepted blockchain
            # and save blockchain to file
            if status == "voter hasn't appended this blockchain":
                self.append_block_to_phase_one_blockchain()
                # Save phase one blockchain to file
                self.set_phase_one_blockchain()
            # Check status of phase one completion
            status = self.check_phase_one_completion()
            # If all desired voters have voted
            # then finish phase one
            # else get phase one blockchain
            if status == "all voters have voted":
                return
            # else wait then get phase one blockchain
            else:
                sleep(5)
                self.get_phase_one_blockchain()

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
            # Create blockchain with desired candidates
            self.phase_one_blockchain = Blockchain()
            # Save accepted blockchain file name
            id = self.phase_one_blockchain.get_id()
            self.phase_one_blockchain_file = "../.blockchains/phase_one/blockchain{}.pkl".format(id)
        # If blockchains are found
        else:
            # Search for largest blockchain with desired candidates
            largest_chain_size = 0
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
                    # Compare candidates with desired candidates
                    for candidate in block.get_candidates():
                        if candidate not in self.desired_candidates or not match:
                            match = False
                            break
                    for candidate in self.desired_candidates:
                        if candidate not in block.get_candidates() or not match:
                            match = False
                            break
                    # Compare voters with desired voters
                    for voter in block.get_voters():
                        if voter not in self.desired_voters or not match:
                            match = False
                            break
                    for voter in self.desired_voters:
                        if voter not in block.get_voters() or not match:
                            match = False
                            break
                    # Verify voter is a desired voter
                    if block.get_voter() not in self.desired_voters:
                        match = False
                    if not match:
                        break
                # If candidates don't match desired candidates,
                # then move to next blockchain
                if match == False:
                    match = True
                # If blockchain matches desired candidates and is larger than
                # prior blockchain which matches desired candidates
                # then save blockchain and blockchain file name
                elif blockchain.get_size() > largest_chain_size:
                    self.phase_one_blockchain_file = file_name
                    largest_chain_size = blockchain.get_size()
                    self.phase_one_blockchain = blockchain
            # If no blockchains with candidates that match desired candidates
            # then save new blockchain and new blockchain file name
            if largest_chain_size == 0:
                # Create blockchain with desired candidates
                self.phase_one_blockchain = Blockchain()
                # Save accepted blockchain file name
                id = self.phase_one_blockchain.get_id()
                self.phase_one_blockchain_file = "../.blockchains/phase_one/blockchain{}.pkl".format(id)
        self.blockchain_locks[0].release()

    # Method to append block to blockchain
    def append_block_to_phase_one_blockchain(self):
        self.phase_one_blockchain.add_block(self.phase_one_block)

    # Save blockchain to file
    def set_phase_one_blockchain(self):
        self.blockchain_locks[0].acquire()
        with open(self.phase_one_blockchain_file, 'wb') as file_name:
            pickle.dump(self.phase_one_blockchain, file_name)
        self.blockchain_locks[0].release()

    # Method to check if phase one is complete
    def check_phase_one_completion(self):
        # Initialize data structure for checking if every desired voter is in
        # the accepted blockchain
        voters = {}
        # Add every desired voter to blockchain and set to false
        for voter in self.desired_voters:
            voters[voter] = False
        # Set true for every voter in blockchain
        for block in self.phase_one_blockchain.get_chain():
            voters[block.get_voter()] = True
        # If every voter is true
        # then return true
        # else return false
        for voter in voters:
            if not voters[voter]:
                if voter == self.voter:
                    return "voter hasn't appended this blockchain"
                else:
                    return "still waiting for another voter"
        return "all voters have voted"

#########################################
#######          Phase Two       ########
#########################################

    # Method for processing phase two
    def start_phase_two(self):
        # Input vote
        self.input_vote()
        # Create block with desired candidate
        self.phase_two_block = PhaseTwoBlock(self.candidate, self.voter)
        status = "voter hasn't appended this blockchain"
        # Get phase two blockchain from file
        self.get_phase_two_blockchain()
        while True:
            # If voter has not appended the accepted blockchain
            # then append block to accepted blockchain
            # and save blockchain to file
            if status == "voter hasn't appended this blockchain":
                self.append_block_to_phase_two_blockchain()
                # Save phase two blockchain to file
                self.set_phase_two_blockchain()
            # Check status of phase one completion
            status = self.check_phase_two_completion()
            # If all desired voters have voted
            # then finish phase one
            # else get phase one blockchain
            if status == "all voters have voted":
                return
            # else wait then get phase one blockchain
            else:
                sleep(5)
                self.get_phase_two_blockchain()

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
            self.phase_two_blockchain_file = "../.blockchains/phase_two/blockchain{}.pkl".format(id)
        # If blockchains are found
        else:
            # Search for largest blockchain with desired candidates
            largest_chain_size = 0
            largest_file_name = ""
            # Cycle through all blockchains
            for file_name in file_names:
                # View blockchain
                with open(file_name, 'rb') as blockchain_file:
                    try:
                        blockchain = pickle.load(blockchain_file)
                        # If blockchain is larger than prior blockchain
                        # then save blockchain and blockchain file name
                        if blockchain.get_size() > largest_chain_size:
                            self.phase_two_blockchain_file = file_name
                            largest_chain_size = blockchain.get_size()
                            self.phase_two_blockchain = blockchain
                    except EOFError, e:
                        pass
        self.blockchain_locks[1].release()

    # Method to append block to blockchain
    def append_block_to_phase_two_blockchain(self):
        self.phase_two_blockchain.add_block(self.phase_two_block)

    # Save blockchain to file
    def set_phase_two_blockchain(self):
        self.blockchain_locks[1].acquire()
        with open(self.phase_two_blockchain_file, 'wb') as file_name:
            pickle.dump(self.phase_two_blockchain, file_name)
        self.blockchain_locks[1].release()

    # Method to check if phase two is complete
    def check_phase_two_completion(self):
        # Initialize data structure for checking if every desired voter is in
        # the accepted blockchain
        voters = {}
        # Add every desired voter to blockchain and set to false
        for voter in self.desired_voters:
            voters[voter] = False
        # Set true for every voter in blockchain
        for block in self.phase_two_blockchain.get_chain():
            voters[block.get_voter()] = True
        # If every voter is true
        # then return true
        # else return false
        for voter in voters:
            if not voters[voter]:
                if voter == self.voter:
                    return "voter hasn't appended this blockchain"
                else:
                    return "still waiting for another voter"
        return "all voters have voted"

#########################################
######          Phase Three       #######
#########################################

    # Method for processing phase three
    def start_phase_three(self):
        # Input voter's name
        self.tally_votes()
        # Create block with desired candidates
        self.phase_three_block = PhaseThreeBlock(self.tally, self.voter)
        status = "voter hasn't appended this blockchain"
        # Get phase one blockchain from file
        self.get_phase_three_blockchain()
        while True:
            # If voter has not appended the accepted blockchain
            # then append block to accepted blockchain
            # and save blockchain to file
            if status == "voter hasn't appended this blockchain":
                self.append_block_to_phase_three_blockchain()
                # Save phase one blockchain to file
                self.set_phase_three_blockchain()
            # Check status of phase one completion
            status = self.check_phase_three_completion()
            # If all desired voters have voted
            # then finish phase one
            # else get phase one blockchain
            if status == "all voters have voted":
                return
            # else wait then get phase one blockchain
            else:
                sleep(5)
                self.get_phase_three_blockchain()

    # Tally the votes in the accepted phase two blockchain
    def tally_votes(self):
        for candidate in self.desired_candidates:
            tally[candidate] = 0
        for block in self.phase_two_blockchain:
            tally[block.get_candidate] += 1

    # Method for loading the currently accepted phase three blockchain
    def get_phase_three_blockchain(self):
        # Find all saved phase three blockchains
        self.blockchain_locks[2].acquire()
        file_names = glob.glob("../.blockchains/phase_three/blockchain*.pkl")
        # If no phase one blockchains found
        if len(file_names) == 0:
            # Create blockchain with desired candidates
            self.phase_three_blockchain = Blockchain()
            # Save accepted blockchain file name
            id = self.phase_three_blockchain.get_id()
            self.phase_three_blockchain_file = "../.blockchains/phase_three/blockchain{}.pkl".format(id)
        # If blockchains are found
        else:
            # Search for largest blockchain with desired candidates
            largest_chain_size = 0
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
                    # Verify all accepted candidates exist in tally
                    for candidate in block.get_tally():
                        if candidate not in self.desired_candidates:
                            match = False
                            break
                        # Verify candidate has the same tally
                        elif tally[candidate] != block.get_tally[candidate]:
                            match = False
                            break
                    if not match:
                        break
                # If candidates don't match desired candidates,
                # then move to next blockchain
                if match == False:
                    match = True
                # If blockchain matches desired candidates and is larger than
                # prior blockchain which matches desired candidates
                # then save blockchain and blockchain file name
                elif blockchain.get_size() > largest_chain_size:
                    self.phase_three_blockchain_file = file_name
                    largest_chain_size = blockchain.get_size()
                    self.phase_three_blockchain = blockchain
            # If no blockchains with candidates that match desired candidates
            # or no blockchains with tallies that match own tally
            # then save new blockchain and new blockchain file name
            if largest_chain_size == 0:
                # Create blockchain with desired candidates
                self.phase_three_blockchain = Blockchain()
                # Save accepted blockchain file name
                id = self.phase_three_blockchain.get_id()
                self.phase_one_blockchain_file = "../.blockchains/phase_three/blockchain{}.pkl".format(id)
        self.blockchain_locks[2].release()

    # Method to append block to blockchain
    def append_block_to_phase_three_blockchain(self):
        self.phase_three_blockchain.add_block(self.phase_three_block)

    # Save blockchain to file
    def set_phase_three_blockchain(self):
        self.blockchain_locks[1].acquire()
        with open(self.phase_two_blockchain_file, 'wb') as file_name:
            pickle.dump(self.phase_two_blockchain, file_name)
        self.blockchain_locks[1].release()

    # Method to check if phase three is complete
    def check_phase_three_completion(self):
        # Initialize data structure for checking if every desired voter is in
        # the accepted blockchain
        voters = {}
        # Add every desired voter to blockchain and set to false
        for voter in self.desired_voters:
            voters[voter] = False
        # Set true for every voter in blockchain
        for block in self.phase_three_blockchain.get_chain():
            voters[block.get_voter()] = True
        # If every voter is true
        # then return true
        # else return false
        for voter in voters:
            if not voters[voter]:
                if voter == self.voter:
                    return "voter hasn't appended this blockchain"
                else:
                    return "still waiting for another voter"
        return "all voters have voted"
