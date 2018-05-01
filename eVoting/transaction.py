#!/usr/bin/env python


class PhaseOneTransaction:

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


class PhaseTwoTransaction:

    def __init__(self, candidate, voter):
        self.candidate = candidate
        self.voter = voter

    def get_candidate(self):
        return self.candidate

    def get_voter(self):
        return self.voter


class PhaseThreeTransaction:

    def __init__(self, tally, voter):
        self.tally = tally
        self.voter = voter

    def get_tally(self):
        return self.tally

    def get_voter(self):
        return self.voter
