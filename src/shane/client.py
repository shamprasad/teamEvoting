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

from blockchain import Blockchain
from block import Block_Phase_One, Block_Phase_Two, Block_Phase_Three


blockchain_locks = [Lock(), Lock(), Lock()]

DESIRED_VOTERS = ["Shane", "Ankur", "Sham"]

DESIRED_CANDIDATES = ["Shane", "Ankur", "Sham"]
CHOSEN_CANDIDATES = ["Shane", "Ankur", "Sham"]

BROADCAST_PORT = 4156

# Select candidates
def phase_one(voter):
    # Find all saved phase one blockchains
    file_names = glob.glob("../blockchains/phase_one/blockchain*.pkl")
    # Create block with desired candidates
    block = Block_Phase_One(DESIRED_CANDIDATES, DESIRED_VOTERS, voter)
    # If no phase one blockchains found
    if len(file_names) == 0:
        # Create blockchain with desired candidates
        blockchain = Blockchain(block)
        # Save blockchain to file with appended random number
        id = blockchain.get_id()
        file_name = "../blockchains/phase_one/blockchain{}.pkl".format(id)
        with open(file_name, 'wb') as blockchain_file:
            pickle.dump(blockchain, blockchain_file)
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
                    voter_dict[block.get_voter()] += 1
                    # Compare candidates with desired candidates
                    for candidate in block.get_candidates():
                        if candidate not in DESIRED_CANDIDATES or not match:
                            match = False
                            break
                    for candidate in DESIRED_CANDIDATES:
                        if candidate not in block.get_candidates() or not match:
                            match = False
                            break
                    # Compare voters with desired voters
                    for voter in block.get_voters():
                        if voter not in DESIRED_VOTERS or not match:
                            match = False
                            break
                    for voter in DESIRED_VOTERS:
                        if voter not in block.get_voters() or not match:
                            match = False
                            break
                    # Verify voter is a desired voter
                    if block.get_voter() not in DESIRED_VOTERS:
                        match = False
                    if not match:
                        break
                # If candidates don't match desired candidates,
                # then move to next blockchain
                if match == False:
                    match = True
                # If blockchain matches desired candidates and is larger than
                # prior blockchain which matches desired candidates
                elif blockchain.get_size() > largest_chain_size:
                    largest_file_name = file_name
                    largest_chain_size = blockchain.get_size()
        # If no blockchains with candidates that match desired candidates
        if largest_chain_size == 0:
            # Create blockchain with desired candidates
            blockchain = Blockchain(block)
            # Save blockchain to file with appended random number
            random_number = (randint(1000, 9999))
            file_name = "../blockchains/phase_one/blockchain{}.pkl".format(random_number)
            with open(file_name, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)
        # If blockchain is found with candidates matching desired candidates
        else:
            # Append desired candidates to blockchain
            with open(largest_file_name, 'rb') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                blockchain.add_block(block)
            # Write blockchain to file
            with open(largest_file_name, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)

# Vote for favorite candidate among desired candidates
def phase_two():
    # Find all saved phase one blockchains
    file_names = glob.glob("../blockchains/phase_one/blockchain*.pkl")
    # If no phase one blockchains found
    # then print error and return from function
    if len(file_names) == 0:
        print "No candidates declared."
        return
    # If phase one blockchains found
    else:
        # Search for largest phase one blockchain
        # Largest phase one blockchain is the chosen candidates
        largest_chain_size = 0
        largest_file_name = ""
        # Cycle through all blockchains
        for file_name in file_names:
            with open(file_name, 'rb') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                # If blockchain is larger than prior blockchains
                # then save blockchain file name and chain length
                if blockchain.get_size() > largest_chain_size:
                    largest_chain_size = blockchain.get_size()
                    largest_file_name = file_name
        # Load largest blockchain
        with open(largest_file_name, 'rb') as blockchain_file:
            blockchain = pickle.load(blockchain_file)
            CHOSEN_CANDIDATES = blockchain.get_chain()[0].get_candidates()
            # Print chosen candidates
            for i, candidate in zip(range(1, len(CHOSEN_CANDIDATES) + 1), CHOSEN_CANDIDATES):
                print "({}) {}".format(i, candidate)
            # User select candidate to vote for
            candidate = input("Select candidate: ")
            candidate = CHOSEN_CANDIDATES[candidate - 1]
            block = Block_Phase_Two(candidate)
        # Find all phase two blockchains
        file_names = glob.glob("../blockchains/phase_two/blockchain*.pkl")
        # If no phase two blockchains found, create blockchain
        if len(file_names) == 0:
            blockchain = Blockchain(block)
            # Save blockchain to file with appended random number
            random_number = (randint(1000, 9999))
            file_name = "../blockchains/phase_two/blockchain{}.pkl".format(random_number)
            with open(file_name, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)
        # If phase two blockchains found
        else:
            # Search for largest blockchain
            largest_chain_size = 0
            largest_file_name = ""
            # Cycle through all blockchains
            for file_name in file_names:
                with open(file_name, 'rb') as blockchain_file:
                    blockchain = pickle.load(blockchain_file)
                    # If blockchain is larger than prior blockchains
                    # then save blockchain file name and chain length
                    if blockchain.get_size() > largest_chain_size:
                        largest_file_name = file_name
                        largest_chain_size = blockchain.get_size()
            # Load largest blockchain, and append block
            with open(largest_file_name, 'rb') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                blockchain.add_block(block)
            # Write blockchain to file
            with open(largest_file_name, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)

# Tally votes in largest phase two blockchain
def phase_three():
    # Find all saved phase two blockchains
    file_names = glob.glob("../blockchains/phase_two/blockchain*.pkl")
    # If no phase two blockchains found
    # then print error and return from function
    if len(file_names) == 0:
        print "No votes performed."
        return
    # If phase two blockchains found
    else:
        # Search for largest phase two blockchain
        # Largest phase two blockchain is the accepted blockchain
        largest_chain_size = 0
        largest_file_name = ""
        # Cycle through all blockchains
        for file_name in file_names:
            with open(file_name, 'rb') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                # If blockchain larger than prior blockchains
                # then save blockchain file name and chain length
                if blockchain.get_size() > largest_chain_size:
                    largest_chain_size = blockchain.get_size()
                    largest_file_name = file_name
        # Load largest blockchain
        with open(largest_file_name, 'rb') as blockchain_file:
            blockchain = pickle.load(blockchain_file)
        # Tally all votes in the blockchain
        tally = {}
        for candidate in CHOSEN_CANDIDATES:
            tally[candidate] = 0
        for block in blockchain.get_chain():
            tally[block.get_candidate()] += 1
        block = Block_Phase_Three(tally)
        # Find all phase three blockchains
        file_names = glob.glob("../blockchains/phase_three/blockchain*.pkl")
        # If no phase three blockchains found, create blockchain
        if len(file_names) == 0:
            blockchain = Blockchain(block)
            # Save blockchain to file with appended random number
            random_number = (randint(1000, 9999))
            file_name = "../blockchains/phase_three/blockchain{}.pkl".format(random_number)
            with open(file_name, 'wb') as blockchain_file:
                pickle.dump(blockchain, blockchain_file)
        # If phase three blockchains found
        else:
            # Search for largest blockchain with matching tally
            largest_chain_size = 0
            largest_file_name = ""
            # Cycle through all blockchains
            for file_name in file_names:
                with open(file_name, 'rb') as blockchain_file:
                    match = True
                    blockchain = pickle.load(blockchain_file)
                    # Cycle through each block in blockchain comparing tallies
                    for block in blockchain.get_chain():
                        for candidate in block.get_tally():
                            if block.get_tally()[candidate] != tally[candidate]:
                                match = False
                                break
                            for cand in tally:
                                if tally[cand] != block.get_tally()[cand]:
                                    match = False
                                    break
                    # If tallies don't match
                    # then move to next blockchain
                    if match == False:
                        match = True
                    # If blockchain matches tally and is larger than prior
                    # blockchain which matches tally
                    elif blockchain.get_size() > largest_chain_size:
                        largest_file_name = file_name
                        largest_chain_size = blockchain.get_size()
            # If no matching blockchains that match tally
            if largest_chain_size == 0:
                # Create blockchain with tally
                blockchain = Blockchain(block)
                # Save blockchain to file with appended random number
                random_number = (randint(1000, 9999))
                file_name = "../blockchains/phase_three/blockchain{}.pkl".format(random_number)
                with open(file_name, 'wb') as blockchain_file:
                    pickle.dump(blockchain, blockchain_file)
            # If blockchain is found with matching tally
            else:
                # Append tally to blockchain
                with open(largest_file_name, 'rb') as blockchain_file:
                    blockchain = pickle.load(blockchain_file)
                    blockchain.add_block(block)
                # Write blockchain to file
                with open(largest_file_name, 'wb') as blockchain_file:
                    pickle.dump(blockchain, blockchain_file)
    for block in blockchain.get_chain():
        print block.get_tally()

def get_blockchains(peer):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.settimeout(5)
    try:
        tcp_sock.connect(peer)
        tcp_sock.send('request blockchains')
        data = tcp_sock.recv(10240)
        bytes_recv = sys.getsizeof(data)
        # print bytes_recv
        tcp_sock.shutdown(socket.SHUT_RDWR)
        tcp_sock.close()
    except (socket.timeout, socket.error), e:
        return
    # Deserialize blockchains into dictionary
    try:
        new_blockchains = pickle.loads(data)
    except pickle.UnpicklingError:
        pass
    # Acquire lock on phase one blockchains
    blockchain_locks[0].acquire()
    filed_blockchains = glob.glob("../blockchains/phase_one/blockchain*.pkl")
    # For each blockchain received from peer
    for new_blockchain in new_blockchains['phase_one'][:]:
        # For each blockchain saved locally
        for filed_blockchain in filed_blockchains:
            # Boolean for determining to replace local blockchain
            save = False
            with open(filed_blockchain, 'rb') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                # If blockchains have same id
                if new_blockchain.get_id() == blockchain.get_id():
                    # Remove blockchain from dictionary
                    new_blockchains['phase_one'].remove(new_blockchain)
                    # If new blockchain is larger than local blockchain
                    # Then set boolean to replace local blockchain
                    if new_blockchain.get_size() > blockchain.get_size():
                        save = True
            # If boolean is set to replace local blockchain
            # Then replace local blockchain with new blockchain
            if save:
                with open(filed_blockchain, 'wb') as blockchain_file:
                    pickle.dump(new_blockchain, blockchain_file)
                save = False
    # Save all new phase one blockchains
    for new_blockchain in new_blockchains['phase_one']:
        id = new_blockchain.get_id()
        file_name = "../blockchains/phase_one/blockchain{}.pkl".format(id)
        with open(file_name, 'wb') as blockchain_file:
            pickle.dump(new_blockchain, blockchain_file)
    # Release lock on phase one blockchains
    blockchain_locks[0].release()
    # Acquire lock on phase two blockchains
    blockchain_locks[1].acquire()
    filed_blockchains = glob.glob("../blockchains/phase_two/blockchain*.pkl")
    # For each blockchain received from peer
    for new_blockchain in new_blockchains['phase_two'][:]:
        # For each blockchain saved locally
        for filed_blockchain in filed_blockchains:
            # Boolean for determining to replace local blockchain
            save = False
            with open(filed_blockchain, 'rb') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                # If blockchains have same id
                if new_blockchain.get_id() == blockchain.get_id():
                    # Remove blockchain from dictionary
                    new_blockchains['phase_two'].remove(new_blockchain)
                    # If new blockchain is larger than local blockchain
                    # Then set boolean to replace local blockchain
                    if new_blockchain.get_size() > blockchain.get_size():
                        save = True
            # If boolean is set to replace local blockchain
            # Then replace local blockchain with new blockchain
            if save:
                with open(filed_blockchain, 'wb') as blockchain_file:
                    pickle.dump(new_blockchain, blockchain_file)
                save = False
    # Save all new phase two blockchains
    for new_blockchain in new_blockchains['phase_two']:
        id = new_blockchain.get_id()
        file_name = "../blockchains/phase_two/blockchain{}.pkl".format(id)
        with open(file_name, 'wb') as blockchain_file:
            pickle.dump(new_blockchain, blockchain_file)
    # Release lock on phase two blockchains
    blockchain_locks[1].release()
    # Acquire lock on phase three blockchains
    blockchain_locks[2].acquire()
    filed_blockchains = glob.glob("../blockchains/phase_three/blockchain*.pkl")
    # For each blockchain received from peer
    for new_blockchain in new_blockchains['phase_three'][:]:
        # For each blockchain saved locally
        for filed_blockchain in filed_blockchains:
            # Boolean for determining to replace local blockchain
            save = False
            with open(filed_blockchain, 'rb') as blockchain_file:
                blockchain = pickle.load(blockchain_file)
                # If blockchains have same id
                if new_blockchain.get_id() == blockchain.get_id():
                    # Remove blockchain from dictionary
                    new_blockchains['phase_three'].remove(new_blockchain)
                    # If new blockchain is larger than local blockchain
                    # Then set boolean to replace local blockchain
                    if new_blockchain.get_size() > blockchain.get_size():
                        save = True
            # If boolean is set to replace local blockchain
            # Then replace local blockchain with new blockchain
            if save:
                with open(filed_blockchain, 'wb') as blockchain_file:
                    pickle.dump(new_blockchain, blockchain_file)
                save = False
    # Save all new phase three blockchains
    for new_blockchain in new_blockchains['phase_three']:
        id = new_blockchain.get_id()
        file_name = "../blockchains/phase_three/blockchain{}.pkl".format(id)
        with open(file_name, 'wb') as blockchain_file:
            pickle.dump(new_blockchain, blockchain_file)
    # Release lock on phase three blockchains
    blockchain_locks[2].release()

def send_blockchains(tcp_client_sock):
    # Prepare dictionary for sending blockchains
    blockchains = {'phase_one': [],
                   'phase_two': [],
                   'phase_three': []}
    # Acquire lock on phase one blockchains
    blockchain_locks[0].acquire()
    # Load all phase one blockchains into dictionary
    phase_one_bc = glob.glob("../blockchains/phase_one/blockchain*.pkl")
    if len(phase_one_bc) > 0:
        for bc in phase_one_bc:
            with open(bc, 'rb') as blockchain_file:
                blockchains['phase_one'].append(pickle.load(blockchain_file))
    # Release lock on phase one blockchains
    blockchain_locks[0].release()
    # Acquire lock on phase two blockchains
    blockchain_locks[1].acquire()
    # Load all phase two blockchains into dictionary
    phase_two_bc = glob.glob("../blockchains/phase_two/blockchain*.pkl")
    if len(phase_two_bc) > 0:
        for bc in phase_two_bc:
            with open(bc, 'rb') as blockchain_file:
                blockchains['phase_two'].append(pickle.load(blockchain_file))
    # Release lock on phase two blockchains
    blockchain_locks[1].release()
    # Acquire lock on phase three blockchains
    blockchain_locks[2].acquire()
    # Load all phase three blockchains into dictionary
    phase_three_bc = glob.glob("../blockchains/phase_three/blockchain*.pkl")
    if len(phase_three_bc) > 0:
        for bc in phase_three_bc:
            with open(bc, 'rb') as blockchain_file:
                blockchains['phase_three'].append(pickle.load(blockchain_file))
    # Release lock on phase three blockchains
    blockchain_locks[2].release()
    # Send blockchains to peer who requested
    try:
        bytes_sent = tcp_client_sock.send(pickle.dumps(blockchains))
        # print bytes_sent
    except socket.error, e:
        pass

def sync_peers(peers, tcp_server_addr):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.settimeout(5)
    try:
        tcp_sock.connect(('localhost', 4156))
        msg = pickle.dumps(['request peers', tcp_server_addr])
        tcp_sock.send(msg)
        data = tcp_sock.recv(1024)
        for peer in peers[:]:
            peers.remove(peer)
        for peer in pickle.loads(data):
            peers.append(peer)
    except socket.timeout, e:
        pass
    print peers

def client_handler(tcp_client_sock):
    data = tcp_client_sock.recv(1024)
    if data == 'request blockchains':
        send_blockchains(tcp_client_sock)
    elif data == 'hello peer':
        tcp_client_sock.send('hello peer')
    tcp_client_sock.shutdown(socket.SHUT_RDWR)
    tcp_client_sock.close()

# Daemon for finding peers
def bc_daemon(event):
    peers = []
    threads = []
    tcp_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_sock.settimeout(5)
    tcp_server_sock.bind(('localhost', randint(10000, 19999)))
    tcp_server_addr = tcp_server_sock.getsockname()
    tcp_server_sock.listen(5)

    timer = time.time()

    while True:
        try:
            tcp_client_sock, client_addr = tcp_server_sock.accept()
            threads.append(Thread(target=client_handler,
                                  args=(tcp_client_sock,)))
            threads[-1].start()
        except socket.timeout, e:
            pass

        if timer+5 <= time.time():
            timer += 5
            threads.append(Thread(target=sync_peers, args=(peers,
                                                           tcp_server_addr)))
            threads[-1].start()
            for peer in peers[:]:
                if peer != tcp_server_addr:
                    threads.append(Thread(target=get_blockchains,
                                          args=(peer,)))
                    threads[-1].start()

            for thread in threads[:]:
                if not thread.is_alive():
                    threads.remove(thread)

        if event.is_set():
            for thread in threads:
                thread.join()
            return

# Main function
def main():
    try:
        event = Event()
        # Start daemon process for updating most recent blockchains from peers
        bc_daemon_p = Thread(target=bc_daemon, args=(event,))
        bc_daemon_p.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event.set()
        bc_daemon_p.join()
        return

if __name__ == '__main__':
    main()
    # phase_one()
    # phase_two()
    # phase_three()
