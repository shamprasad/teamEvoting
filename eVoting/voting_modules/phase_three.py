#!/usr/bin/env python

from eVoting.data_structures import (
    PhaseThreeBlock,
    Blockchain
)


class PhaseThree:

    def __init__(self, phase_two, blockchain_locks):

        self.blockchain_locks = blockchain_locks
        
        self.phase_three_block = None

    # Method for processing phase three
    def start(self):
        # Create block with input vote
        self.phase_three_block = PhaseThreeBlock()
