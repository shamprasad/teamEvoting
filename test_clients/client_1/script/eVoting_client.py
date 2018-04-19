#!/usr/bin/env python

import os
import glob
from time import sleep

from eVoting.voting_modules import PhaseManager
from eVoting.network import Daemon


# Method for deleting all locally saved blockchains
def delete_blockchains():
    file_names = glob.glob("../.blockchains/phase_one/blockchain*.pkl")
    for file_name in file_names:
        os.remove(file_name)
    file_names = glob.glob("../.blockchains/phase_two/blockchain*.pkl")
    for file_name in file_names:
        os.remove(file_name)
    file_names = glob.glob("../.blockchains/phase_three/blockchain*.pkl")
    for file_name in file_names:
        os.remove(file_name)

def create_directories():
    if not os.path.exists(os.path.dirname("../.blockchains/phase_one/")):
        os.makedirs(os.path.dirname("../.blockchains/phase_one/"))
    if not os.path.exists(os.path.dirname("../.blockchains/phase_two/")):
        os.makedirs(os.path.dirname("../.blockchains/phase_two/"))
    if not os.path.exists(os.path.dirname("../.blockchains/phase_three/")):
        os.makedirs(os.path.dirname("../.blockchains/phase_three/"))

# Main method
def main():
    # Create directories if they don't exist
    create_directories()
    # Delete any existing blockchains
    delete_blockchains()
    # Start daemon for sharing blockchains with peers
    daemon = Daemon()
    daemon.start()
    # Initialize a phase objects
    phase_manager = PhaseManager(daemon.blockchain_locks)
    # Start phase one
    phase_manager.start_phase_one()
    print "Phase one complete!"
    # Start phase two
    phase_manager.start_phase_two()
    print "Phase two complete!"
    # Start phase three
    phase_manager.start_phase_three()
    print "Phase three complete!"

    while True:
        sleep(1)


# Method for handling direct script calls
if __name__ == '__main__':
    main()
