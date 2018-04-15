#!/usr/bin/env python

from threading import (
    Thread,
    Event,
    Lock,
)
import socket
from time import time
from random import randint
import cPickle as pickle
import glob

from .server import (
    HEARTBEAT_TIMER,
    SERVER_ADDRESS
)

class Daemon:
    # Initialize daemon
    def __init__(self):
        self.event = Event()
        self.heartbeat = HEARTBEAT_TIMER/10.
        # Locks for controlling access to the saved blockchains
        self.blockchain_locks = [Lock(), Lock(), Lock()]
        # Lock for controlling access to the peers list
        self.peers_lock = Lock()
        # Stores known peers' addresses
        self.peers = []
        # Initialize server tcp socket
        self.server_tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_tcp_sock.settimeout(5)
        self.server_tcp_sock.bind(('localhost', randint(10000, 19999)))
        self.server_tcp_addr = self.server_tcp_sock.getsockname()
        self.server_tcp_sock.listen(5)
        # Initialize thread as daemon
        self.bc_daemon_t = Thread(target=self.bc_daemon)

    def start(self):
        self.bc_daemon_t.start()

    # Daemon for finding peers
    def bc_daemon(self):
        # Acquire peers from saved peers and server
        self.acquire_initial_peers()
        # Request blockchains from peers
        self.peers_lock.acquire()
        peers = self.peers[:]
        self.peers_lock.release()
        for peer in peers:
            # If peer is not self
            # then request blockchains from peer
            if peer != self.server_tcp_addr:
                Thread(target=self.get_blockchains,
                       args=(peer,)).start()
        # Timer for controlling heartbeats
        timer = time()
        # Iterate through sending blockchains to peer, requesting blockchains
        # from peers, and requesting peers from the server
        while True:
            print 'test1'
            # Listen for peers
            # If peer pings, call client_handler to handle the request
            try:
                client_tcp_sock, client_addr = self.server_tcp_sock.accept()
                Thread(target=self.client_handler,
                       args=(client_tcp_sock,)).start()
            # If no peer pings, handle timeout exception
            except socket.timeout, e:
                pass
            print 'test3'
            # Iterate once per heartbeat
            if timer+self.heartbeat <= time():
                timer += self.heartbeat
                # Request peers from server
                Thread(target=self.sync_peers).start()
                # Cycle through peers
                print 'test24'
                self.peers_lock.acquire()
                print 'test25'
                peers = self.peers[:]
                print 'test26'
                self.peers_lock.release()
                print 'test27'
                for peer in peers:
                    # If peer is not self
                    # then request blockchains from peer
                    if peer != self.server_tcp_addr:
                        Thread(target=self.get_blockchains,
                               args=(peer,)).start()
            print 'test4'
            # Set event to kill all threads
            print self.event.is_set()
            if self.event.is_set():
                print 'test5'
                return

    # Method for acquiring peers from file and server
    def acquire_initial_peers(self):
        print 'test6'
        # Request peers from server
        self.sync_peers()
        # Load peers saved to file
        file_name = glob.glob("../.peers.pkl")
        if len(file_name) == 0:
            return
        with open(file_name, 'rb') as peers_file:
            file_peers = pickle.load(peers_file)
            self.peers_lock.acquire()
            for peer in file_peers[:]:
                if peer in self.peers:
                    try:
                        file_peers.remove(peer)
                    except ValueError, e:
                        pass
            # Append peers saved in file to those received from server
            self.peers.append(file_peers)
            self.peers_lock.release()

    # Method for requesting peers from server
    def sync_peers(self):
        print 'test7'
        # Initialize client tcp socket
        client_tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_tcp_sock.settimeout(5)
        # If server is active and responds
        try:
            print 'test12'
            # Connect and send request for peers
            client_tcp_sock.connect(SERVER_ADDRESS)
            print 'test21'
            msg = pickle.dumps(['request peers', self.server_tcp_addr])
            print 'test22'
            client_tcp_sock.send(msg)
            print 'test23'
            data = client_tcp_sock.recv(1024)
            # Save all new peers
            print 'test20'
            self.peers_lock.acquire()
            print 'test13'
            for peer in pickle.loads(data):
                print 'test14'
                if peer not in self.peers:
                    print 'test15'
                    self.peers.append(peer)
            print 'test16'
            self.peers_lock.release()
            print 'test17'
        # If server does not respond
        # then do nothing
        except socket.timeout, e:
            print 'test18'
            pass
        # Shutdown and close the client tcp socket
        client_tcp_sock.shutdown(socket.SHUT_RDWR)
        client_tcp_sock.close()
        print 'test19'

    def get_blockchains(self, peer):
        print 'test8'
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sock.settimeout(5)
        try:
            tcp_sock.connect(peer)
            msg = ('request blockchains', self.server_tcp_addr)
            msg = pickle.dumps(msg)
            tcp_sock.send(msg)
            data = tcp_sock.recv(10240)
            tcp_sock.shutdown(socket.SHUT_RDWR)
            tcp_sock.close()
        except (socket.timeout, socket.error), e:
            try:
                self.peers_lock.acquire()
                self.peers.remove(peer)
                self.peers_lock.release()
            except ValueError, e:
                pass
            return
        # Deserialize blockchains into dictionary
        try:
            new_blockchains = pickle.loads(data)
        except pickle.UnpicklingError:
            return
        # Acquire lock on phase one blockchains
        self.blockchain_locks[0].acquire()
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
        self.blockchain_locks[0].release()
        # Acquire lock on phase two blockchains
        self.blockchain_locks[1].acquire()
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
        self.blockchain_locks[1].release()
        # Acquire lock on phase three blockchains
        self.blockchain_locks[2].acquire()
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
        self.blockchain_locks[2].release()

    # Method for handling peer requests
    def client_handler(self, client_tcp_sock):
        print 'test9'
        # Store data sent from peer
        data = client_tcp_sock.recv(1024)
        data = pickle.loads(data)
        # If peer requests blockchains
        # Then call method to send the blockchains
        if data[0] == 'request blockchains':
            self.peers_lock.acquire()
            if data[1] not in self.peers:
                self.peers.append(data[1])
            self.peers_lock.release()
            self.send_blockchains(client_tcp_sock)
        # Close client socket
        client_tcp_sock.close()

    # Method for sending blockchains to the passed address
    def send_blockchains(self, client_tcp_sock):
        print 'test10'
        # Prepare dictionary for sending blockchains
        blockchains = {'phase_one': [],
                       'phase_two': [],
                       'phase_three': []}
        # Acquire lock on phase one blockchains
        self.blockchain_locks[0].acquire()
        # Load all phase one blockchains into dictionary
        phase_one_bc = glob.glob("../blockchains/phase_one/blockchain*.pkl")
        if len(phase_one_bc) > 0:
            for bc in phase_one_bc:
                with open(bc, 'rb') as blockchain_file:
                    blockchains['phase_one'].append(pickle.load(blockchain_file))
        # Release lock on phase one blockchains
        self.blockchain_locks[0].release()
        # Acquire lock on phase two blockchains
        self.blockchain_locks[1].acquire()
        # Load all phase two blockchains into dictionary
        phase_two_bc = glob.glob("../blockchains/phase_two/blockchain*.pkl")
        if len(phase_two_bc) > 0:
            for bc in phase_two_bc:
                with open(bc, 'rb') as blockchain_file:
                    blockchains['phase_two'].append(pickle.load(blockchain_file))
        # Release lock on phase two blockchains
        self.blockchain_locks[1].release()
        # Acquire lock on phase three blockchains
        self.blockchain_locks[2].acquire()
        # Load all phase three blockchains into dictionary
        phase_three_bc = glob.glob("../blockchains/phase_three/blockchain*.pkl")
        if len(phase_three_bc) > 0:
            for bc in phase_three_bc:
                with open(bc, 'rb') as blockchain_file:
                    blockchains['phase_three'].append(pickle.load(blockchain_file))
        # Release lock on phase three blockchains
        self.blockchain_locks[2].release()
        # Send blockchains to peer who requested
        try:
            bytes_sent = client_tcp_sock.send(pickle.dumps(blockchains))
            # print bytes_sent
        except socket.error, e:
            pass
