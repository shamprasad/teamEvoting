#!/usr/bin/env python


class PhaseOneBlock:

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


class PhaseTwoBlock:

    def __init__(self, candidate, voter):
        self.candidate = candidate
        self.voter = voter

    def get_candidate(self):
        return self.candidate

    def get_voter(self):
        return self.voter


class PhaseThreeBlock:

    def __init__(self, tally):
        self.tally = tally

    def get_tally(self):
        return self.tally
