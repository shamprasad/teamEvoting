#!/usr/bin/env python

import os
import glob

from teamEvoting import (
    voting_module,
    daemon
)

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
    # daemon_t = daemon.Daemon()
    # daemon_t.start()
    # Initiazlie a {PhaseManager}
    pm = voting_module.PhaseManager()
    # Start phase one
    pm.phase_one()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt, e:
            daemon_t.event.set()
            break

# Method for handling direct script calls
if __name__ == '__main__':
    main()
