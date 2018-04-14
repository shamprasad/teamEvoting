#!/usr/bin/env python


class Block_Phase_One:

    def __init__(self, candidates, voters, voter):
        self.candidates = candidates
        self.voter = voter
        self.voters = voters

    def get_candidates(self):
        return self.candidates

    def get_voter(self):
        return self.voter

    def get_voters(self):
        return self.voters


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
