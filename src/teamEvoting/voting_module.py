#!/usr/bin/env python

import sys
import glob
import cPickle as pickle
import os
from random import randint
from multiprocessing import Process, Lock
from threading import Thread, Event
import socket
import time
from select import select

from blockchain import Blockchain
from block import Block_Phase_One, Block_Phase_Two, Block_Phase_Three


DESIRED_VOTERS = ["Shane", "Ankur", "Sham"]
DESIRED_CANDIDATES = ["Shane", "Ankur", "Sham"]

# Select candidates
def phase_one(voter):
#
# def get_phase_one_blockchain():
#     # Find all saved phase one blockchains
#     blockchain_locks[0].acquire()
#     file_names = glob.glob("../blockchains/phase_one/blockchain*.pkl")
#     # If no phase one blockchains found
#     if len(file_names) == 0:
#         # Save blockchain to file with appended random number
#         return None
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
#             return None
#         # If blockchain is found with candidates matching desired candidates
#         else:
#             # Append desired candidates to blockchain
#             with open(largest_file_name, 'rb') as blockchain_file:
#                 blockchain = pickle.load(blockchain_file)
#     blockchain_locks[0].release()
#     voters = {}
#     for voter in DESIRED_VOTERS:
#         voters[voter] = False
#     for block in blockchain.get_chain():
#         voters[block.get_voter()] = True
#     for voter in voters:
#         if not voters[voter]:
#             return None
#     return blockchain
#
# # Vote for favorite candidate among desired candidates
# def phase_two():
#     # Find all saved phase one blockchains
#     file_names = glob.glob("../blockchains/phase_one/blockchain*.pkl")
#     # If no phase one blockchains found
#     # then print error and return from function
#     if len(file_names) == 0:
#         print "No candidates declared."
#         return
#     # If phase one blockchains found
#     else:
#         # Search for largest phase one blockchain
#         # Largest phase one blockchain is the chosen candidates
#         largest_chain_size = 0
#         largest_file_name = ""
#         # Cycle through all blockchains
#         for file_name in file_names:
#             with open(file_name, 'rb') as blockchain_file:
#                 blockchain = pickle.load(blockchain_file)
#                 # If blockchain is larger than prior blockchains
#                 # then save blockchain file name and chain length
#                 if blockchain.get_size() > largest_chain_size:
#                     largest_chain_size = blockchain.get_size()
#                     largest_file_name = file_name
#         # Load largest blockchain
#         with open(largest_file_name, 'rb') as blockchain_file:
#             blockchain = pickle.load(blockchain_file)
#             CHOSEN_CANDIDATES = blockchain.get_chain()[0].get_candidates()
#             # Print chosen candidates
#             for i, candidate in zip(range(1, len(CHOSEN_CANDIDATES) + 1), CHOSEN_CANDIDATES):
#                 print "({}) {}".format(i, candidate)
#             # User select candidate to vote for
#             candidate = input("Select candidate: ")
#             candidate = CHOSEN_CANDIDATES[candidate - 1]
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
#
# # Tally votes in largest phase two blockchain
# def phase_three():
#     # Find all saved phase two blockchains
#     file_names = glob.glob("../blockchains/phase_two/blockchain*.pkl")
#     # If no phase two blockchains found
#     # then print error and return from function
#     if len(file_names) == 0:
#         print "No votes performed."
#         return
#     # If phase two blockchains found
#     else:
#         # Search for largest phase two blockchain
#         # Largest phase two blockchain is the accepted blockchain
#         largest_chain_size = 0
#         largest_file_name = ""
#         # Cycle through all blockchains
#         for file_name in file_names:
#             with open(file_name, 'rb') as blockchain_file:
#                 blockchain = pickle.load(blockchain_file)
#                 # If blockchain larger than prior blockchains
#                 # then save blockchain file name and chain length
#                 if blockchain.get_size() > largest_chain_size:
#                     largest_chain_size = blockchain.get_size()
#                     largest_file_name = file_name
#         # Load largest blockchain
#         with open(largest_file_name, 'rb') as blockchain_file:
#             blockchain = pickle.load(blockchain_file)
#         # Tally all votes in the blockchain
#         tally = {}
#         for candidate in CHOSEN_CANDIDATES:
#             tally[candidate] = 0
#         for block in blockchain.get_chain():
#             tally[block.get_candidate()] += 1
#         block = Block_Phase_Three(tally)
#         # Find all phase three blockchains
#         file_names = glob.glob("../blockchains/phase_three/blockchain*.pkl")
#         # If no phase three blockchains found, create blockchain
#         if len(file_names) == 0:
#             blockchain = Blockchain(block)
#             # Save blockchain to file with appended random number
#             random_number = (randint(1000, 9999))
#             file_name = "../blockchains/phase_three/blockchain{}.pkl".format(random_number)
#             with open(file_name, 'wb') as blockchain_file:
#                 pickle.dump(blockchain, blockchain_file)
#         # If phase three blockchains found
#         else:
#             # Search for largest blockchain with matching tally
#             largest_chain_size = 0
#             largest_file_name = ""
#             # Cycle through all blockchains
#             for file_name in file_names:
#                 with open(file_name, 'rb') as blockchain_file:
#                     match = True
#                     blockchain = pickle.load(blockchain_file)
#                     # Cycle through each block in blockchain comparing tallies
#                     for block in blockchain.get_chain():
#                         for candidate in block.get_tally():
#                             if block.get_tally()[candidate] != tally[candidate]:
#                                 match = False
#                                 break
#                             for cand in tally:
#                                 if tally[cand] != block.get_tally()[cand]:
#                                     match = False
#                                     break
#                     # If tallies don't match
#                     # then move to next blockchain
#                     if match == False:
#                         match = True
#                     # If blockchain matches tally and is larger than prior
#                     # blockchain which matches tally
#                     elif blockchain.get_size() > largest_chain_size:
#                         largest_file_name = file_name
#                         largest_chain_size = blockchain.get_size()
#             # If no matching blockchains that match tally
#             if largest_chain_size == 0:
#                 # Create blockchain with tally
#                 blockchain = Blockchain(block)
#                 # Save blockchain to file with appended random number
#                 random_number = (randint(1000, 9999))
#                 file_name = "../blockchains/phase_three/blockchain{}.pkl".format(random_number)
#                 with open(file_name, 'wb') as blockchain_file:
#                     pickle.dump(blockchain, blockchain_file)
#             # If blockchain is found with matching tally
#             else:
#                 # Append tally to blockchain
#                 with open(largest_file_name, 'rb') as blockchain_file:
#                     blockchain = pickle.load(blockchain_file)
#                     blockchain.add_block(block)
#                 # Write blockchain to file
#                 with open(largest_file_name, 'wb') as blockchain_file:
#                     pickle.dump(blockchain, blockchain_file)
#     for block in blockchain.get_chain():
#         print block.get_tally()
#
# # Main function
# def main():
#         # Phase one
#         while True:
#             voter = raw_input("Enter voter's name: ")
#             if voter in DESIRED_VOTERS:
#                 blockchain = phase_one(voter)
#                 if blockchain:
#                     print "Phase one complete."
#                     print "Candidates:", blockchain.get_chain()[0].get_candidates()
#                     break
#             elif voter == "check":
#                 blockchain = get_phase_one_blockchain()
#                 if blockchain:
#                     print "Phase one complete."
#                     print "Candidates:", blockchain.get_chain()[0].get_candidates()
#                     break
#             else:
#                 print "Unauthorized voter."
#         # Wait for phase one to end
#         while True:
#             blockchain = get_phase_one_blockchain()
#             if blockchain:
#                 print "Phase one complete."
#                 print "Candidates:", blockchain.get_chain()[0].get_candidates()
#                 break
#             else:
#                 time.sleep(5)
#
#     except (KeyboardInterrupt, Exception), e:
#         print e
#         event.set()
#         bc_daemon_p.join()
#
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt, e:
#         event.set()
#         bc_daemon_p.join()
