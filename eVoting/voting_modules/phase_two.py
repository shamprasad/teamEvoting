#!/usr/bin/env python

from eVoting.voting_modules import (
    PhaseManager
)


class PhaseTwo(PhaseManager):

    def __init__(self):
        PhaseManager__init__.(self)

    # Method for processing phase two
    def start(self):
        # Input voter's vote
        self.input_vote()
        # Create block with input vote
        self.phase_two_block = PhaseTwoBlock()

    # Method for inputing voter's vote
    def input_vote(self):
        while True:
            for i, candidate in zip(range(len(self.DESIRED_CANDIDATES)), self.DESIRED_CANDIDATES):
                print "({}) {}".format(i+1, candidate)
            # User select candidate to vote for
            candidate = input("Select candidate: ")
            candidate = self.DESIRED_CANDIDATES[candidate - 1]
            if candidate.lower() in self.DESIRED_CANDIDATES:
                self.candidate = voter.lower()
                return
            else:
                print 'Selection not an accepted candidate.'
                continue






#             block = Block_Phase_Two(candidate)
#         # Find all phase two blockchains
#         file_names = glob.glob("../blockchains/phase_two/blockchain*.pkl")
#         # If no phase two blockchains found, create blockchain
#         if len(file_names) == 0:
#             blockchain = Blockchain(block)
#             # Save blockchain to file with appended random number
#             random_number = (randint(1000, 9999))
#             file_name = "../blockchains/phase_two/blockchain{}.pkl".format(random_number)
#             with open(file_name, 'wb') as blockchain_file:
#                 pickle.dump(blockchain, blockchain_file)
#         # If phase two blockchains found
#         else:
#             # Search for largest blockchain
#             largest_chain_size = 0
#             largest_file_name = ""
#             # Cycle through all blockchains
#             for file_name in file_names:
#                 with open(file_name, 'rb') as blockchain_file:
#                     blockchain = pickle.load(blockchain_file)
#                     # If blockchain is larger than prior blockchains
#                     # then save blockchain file name and chain length
#                     if blockchain.get_size() > largest_chain_size:
#                         largest_file_name = file_name
#                         largest_chain_size = blockchain.get_size()
#             # Load largest blockchain, and append block
#             with open(largest_file_name, 'rb') as blockchain_file:
#                 blockchain = pickle.load(blockchain_file)
#                 blockchain.add_block(block)
#             # Write blockchain to file
#             with open(largest_file_name, 'wb') as blockchain_file:
#                 pickle.dump(blockchain, blockchain_file)
