#!/usr/bin/env python


class Block_Phase_One:

    def __init__(self, candidates):
        self.candidates = candidates

    def get_candidates(self):
        return self.candidates


class Block_Phase_Two:

    def __init__(self, candidate):
        self.candidate = candidate

    def get_candidate(self):
        return self.candidate

class Block_Phase_Three:

    def __init__(self, tally):
        self.tally = tally

    def get_tally(self):
        return self.tally
