#!/usr/bin/env python

from eVoting.data_structures import (
    PhaseOneBlock,
    Blockchain
)


class PhaseManager:

    def __init__(self):
        self.DESIRED_VOTERS = [x.lower() for x in ["Shane", "Ankur", "Sham"]]
        self.DESIRED_CANDIDATES = [x.lower() for x in ["Shane", "Ankur", "Sham"]]

        self.voter = None

        self.voted_in_phase_one = False
        self.phase_one_blockchain = None

    # # Method for processing phase one
    # def phase_one(self):
    #     # If voter has not voted yet
    #     if not self.voted_in_phase_one:
    #         self.get_voter()
    #         self.get_phase_one_blockchain()
    #
    # # Method for acquiring voter's name
    # def get_voter(self):
    #     while True:
    #         voter = raw_input("Enter voter's name: ")
    #         if voter.lower() in self.DESIRED_VOTERS:
    #             self.voter = voter
    #             return
    #         else:
    #             print 'Voter not a desired voter.'
    #             continue
    #
    # # Method for loading the currently accepted phase one blockchain
    # def get_phase_one_blockchain(self):
    #     # Find all saved phase one blockchains
    #     blockchain_locks[0].acquire()
    #     file_names = glob.glob("../blockchains/phase_one/blockchain*.pkl")
    #     # Create block with desired candidates
    #     block = Block_Phase_One(DESIRED_CANDIDATES, DESIRED_VOTERS, voter)
    #     # If no phase one blockchains found
    #     if len(file_names) == 0:
    #         # Create blockchain with desired candidates
    #         blockchain = Blockchain(block)
    #         # Save blockchain to file with appended random number
    #         ident = blockchain.get_id()
    #         file_name = "../blockchains/phase_one/blockchain{}.pkl".format(ident)
    #         with open(file_name, 'wb') as blockchain_file:
    #             pickle.dump(blockchain, blockchain_file)
    #     # If blockchains are found
    #     else:
    #         # Search for largest blockchain with desired candidates
    #         largest_chain_size = 0
    #         largest_file_name = ""
    #         # Cycle through all blockchains
    #         for file_name in file_names:
    #             # View blockchain
    #             with open(file_name, 'rb') as blockchain_file:
    #                 match = True
    #                 blockchain = pickle.load(blockchain_file)
    #                 # Cycle through each block in blockchain
    #                 for blck in blockchain.get_chain():
    #                     # Compare candidates with desired candidates
    #                     for candidate in blck.get_candidates():
    #                         if candidate not in DESIRED_CANDIDATES or not match:
    #                             match = False
    #                             break
    #                     for candidate in DESIRED_CANDIDATES:
    #                         if candidate not in blck.get_candidates() or not match:
    #                             match = False
    #                             break
    #                     # Compare voters with desired voters
    #                     for voter in blck.get_voters():
    #                         if voter not in DESIRED_VOTERS or not match:
    #                             match = False
    #                             break
    #                     for voter in DESIRED_VOTERS:
    #                         if voter not in blck.get_voters() or not match:
    #                             match = False
    #                             break
    #                     # Verify voter is a desired voter
    #                     if blck.get_voter() not in DESIRED_VOTERS:
    #                         match = False
    #                     if not match:
    #                         break
    #                 # If candidates don't match desired candidates,
    #                 # then move to next blockchain
    #                 if match == False:
    #                     match = True
    #                 # If blockchain matches desired candidates and is larger than
    #                 # prior blockchain which matches desired candidates
    #                 elif blockchain.get_size() > largest_chain_size:
    #                     largest_file_name = file_name
    #                     largest_chain_size = blockchain.get_size()
    #         # If no blockchains with candidates that match desired candidates
    #         if largest_chain_size == 0:
    #             # Create blockchain with desired candidates
    #             blockchain = Blockchain(block)
    #             # Save blockchain to file with appended random number
    #             random_number = (randint(1000, 9999))
    #             file_name = "../blockchains/phase_one/blockchain{}.pkl".format(random_number)
    #             with open(file_name, 'wb') as blockchain_file:
    #                 pickle.dump(blockchain, blockchain_file)
    #         # If blockchain is found with candidates matching desired candidates
    #         else:
    #             # Append desired candidates to blockchain
    #             with open(largest_file_name, 'rb') as blockchain_file:
    #                 blockchain = pickle.load(blockchain_file)
    #                 blockchain.add_block(block)
    #             # Write blockchain to file
    #             with open(largest_file_name, 'wb') as blockchain_file:
    #                 pickle.dump(blockchain, blockchain_file)
    #     blockchain_locks[0].release()
    #     voters = {}
    #     for voter in DESIRED_VOTERS:
    #         voters[voter] = False
    #     for block in blockchain.get_chain():
    #         voters[block.get_voter()] = True
    #     for voter in voters:
    #         if not voters[voter]:
    #             self.phase_one_blockchain = None
    #     self.phase_one_blockchain = blockchain
