#!/usr/bin/env python

from eVoting.data_structures import (
    PhaseOneBlock,
    PhaseTwoBlock,
    Blockchain
)
from eVoting.network import (
    BLOCKCHAIN_LOCKS
)


class PhaseManager:

    def __init__(self):
        self.DESIRED_VOTERS = [x.lower() for x in ["Shane", "Ankur", "Sham"]]
        self.DESIRED_CANDIDATES = [x.lower() for x in ["Shane", "Ankur", "Sham"]]

        self.voter = None
        self.candidate = None

        self.phase_one_block = None
        self.phase_one_blockchain = None
        self.phase_one_blockchain_file = None

        self.phase_two_block = None
        self.phase_two_blockchain = None
        self.phase_two_blockchain_file = None

        self.phase_three_block= None
        self.phase_three_blockchain = None
        self.phase_three_blockchain_file = None
