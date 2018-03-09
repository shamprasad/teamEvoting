#!/usr/bin/env python


class Block_Phase_One:

    def __init__(self, candidates):
        self.candidates = candidates

    def get_candidates(self):
        return self.candidates


class Block_Phase_Two:

    def __init__(self, voter, candidate):
        self.voter = voter
        self.candidate = candidate

    def get_voter(self):
        return self.voter

    def get_candidate(self):
        return self.candidate

class Block_Phase_Three:

    def __init__(self):
        pass
