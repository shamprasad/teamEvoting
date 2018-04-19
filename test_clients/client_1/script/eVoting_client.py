#!/usr/bin/env python

import os
import glob

from eVoting.voting_modules import (
    PhaseOne
    PhaseTwo
)
from eVoting.network import Daemon

import time

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

# Main method
def main():
    # Delete any existing blockchains
    delete_blockchains()
    # Start daemon for sharing blockchains with peers
    daemon_t = Daemon()
    daemon_t.start()
    # Initialize a phase objects
    phase_one = PhaseOne()
    phase_two = PhaseTwo()
    # Start phase one
    phase_one.start()
    # Start phase two
    phase_two.start()

    while True:
        try:
            print 'test2'
            time.sleep(1)
        except KeyboardInterrupt, e:
            daemon_t.event.set()
            print 'test11'
            break

# Method for handling direct script calls
if __name__ == '__main__':
    main()
