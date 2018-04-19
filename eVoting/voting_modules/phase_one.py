#!/usr/bin/env python

from eVoting.voting_modules import (
    PhaseManager
)


class PhaseOne(PhaseManager):

    def __init__(self):
        PhaseManager__init__.(self)

    # Method for processing phase one
    def start(self):
        # Input voter's name
        self.input_voter_name()
        # Create block with desired candidates
        self.phase_one_block = PhaseOneBlock(self.DESIRED_CANDIDATES, self.DESIRED_VOTERS, self.voter)
        status = "voter hasn't appended this blockchain"
        while True:
            # Get phase one blockchain from file and append block to accepted
            # blockchain
            self.get_phase_one_blockchain()
            # Check status of phase one completion
            status = self.check_phase_one_completion()
            # If voter has not appended the accepted blockchain
            # then append block to accepted blockchain
            # and save blockchain to file
            if status == "voter hasn't appended this blockchain":
                self.append_block_to_blockchain()
                status = self.check_phase_one_completion()
                # Save phase one blockchain to file
                self.set_phase_one_blockchain()
            # Check status of phase one completion
            status = self.check_phase_one_completion()
            # If all desired voters have voted
            # then finish phase one
            if status == "all voters have voted":
                return

    # Method for acquiring voter's name
    def input_voter_name(self):
        while True:
            # Get voter's name
            voter = raw_input("Enter voter's name: ")
            # If name is a desired voter
            # then save name
            if voter.lower() in self.DESIRED_VOTERS:
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
        BLOCKCHAIN_LOCKS[0].acquire()
        file_names = glob.glob("../blockchains/phase_one/blockchain*.pkl")
        # If no phase one blockchains found
        if len(file_names) == 0:
            # Create blockchain with desired candidates
            self.phase_one_blockchain = Blockchain()
            # Save accepted blockchain file name
            id = blockchain.get_id()
            self.phase_one_blockchain_file = "../blockchains/phase_one/blockchain{}.pkl".format(id)
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
                    blockchain = pickle.load(blockchain_file)
                # Cycle through each block in blockchain
                for block in blockchain.get_chain():
                    # Compare candidates with desired candidates
                    for candidate in block.get_candidates():
                        if candidate not in self.DESIRED_CANDIDATES or not match:
                            match = False
                            break
                    for candidate in self.DESIRED_CANDIDATES:
                        if candidate not in block.get_candidates() or not match:
                            match = False
                            break
                    # Compare voters with desired voters
                    for voter in block.get_voters():
                        if voter not in self.DESIRED_VOTERS or not match:
                            match = False
                            break
                    for voter in self.DESIRED_VOTERS:
                        if voter not in block.get_voters() or not match:
                            match = False
                            break
                    # Verify voter is a desired voter
                    if block.get_voter() not in self.DESIRED_VOTERS:
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
            BLOCKCHAIN_LOCKS[0].release()
            # If no blockchains with candidates that match desired candidates
            # then save new blockchain and new blockchain file name
            if largest_chain_size == 0:
                # Create blockchain with desired candidates
                self.phase_one_blockchain = Blockchain()
                # Save accepted blockchain file name
                id = blockchain.get_id()
                self.phase_one_blockchain_file = "../blockchains/phase_one/blockchain{}.pkl".format(id)

    # Method to append block to bockchain
    def append_block_to_phase_one_blockchain(self):
        self.phase_one_blockchain.add_block(self.phase_one_block)

    # Save blockchain to file
    def set_phase_one_blockchain(self):
        with open(file_name, 'wb') as self.phase_one_blockchain_file:
            pickle.dump(self.phase_one_blockchain, file_name)

    # Method to check if phase one is complete
    def check_phase_one_completion(self):
        # Initialize data structure for checking if every desired voter is in
        # the accepted blockchain
        voters = {}
        # Add every desired voter to blockchain and set to false
        for voter in self.DESIRED_VOTERS:
            voters[self.voter] = False
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
            else:
                return "all voters have voted"
