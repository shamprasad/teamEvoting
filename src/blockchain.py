#!/usr/bin/env python

import glob
import hashlib as hasher
import csv
from random import randint


CANDIDATES = ["Shane Lockwood", "Ankur Jain", "Sham Prasad"]

class Phase_One_Block:

    def __init__(self, candidates, previous_hash):
        self.candidates = candidates
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.candidates) +
                   str(self.previous_hash))
        return sha.hexdigest()

    def get_candidates(self):
        return self.candidates

    def get_previous_hash(self):
        return self.previous_hash

    def get_hash(self):
        return self.hash


# class Phase_Two_Block:
#
#     def __init__(self, voter, votee, previous_hash):
#         self.index
#         self.voter = voter
#         self.votee = votee
#         self.previous_hash
#         self.hash
#
# class Phase_Three_Block:
#
#     def __init__(self, voter, votee, previous_hash):
#         self.index
#         self.voter = voter
#         self.votee = votee
#         self.previous_hash
#         self.hash

def phase_one():
    block = Phase_One_Block(CANDIDATES, "0")
    file_names = glob.glob("../blockchains/phase_one/blockchain*.csv")
    if len(file_names) == 0:
        random_number = (randint(1000, 9999))
        file_name ="../blockchains/phase_one/blockchain{}.csv".format(random_number)
        with open(file_name, "wb") as phase_one_file:
            writer = csv.writer(phase_one_file)
            to_write = []
            for candidate in block.get_candidates():
                to_write.append(candidate)
            to_write.append("end candidates")
            to_write.append(block.get_previous_hash())
            to_write.append(block.get_hash())
            writer.writerow(to_write)
    else:
        largest_row_count = 0
        largest_file_name = ""
        wrong_candidates = False
        for file_name in file_names:
            row_counter = 0
            for row in csv.reader(open(file_name, "rb")):
                for index in row:
                    print index


        #         if row != CANDIDATES:
        #             wrong_candidates = True
        #             break
        #         row_counter += 1
        #     if wrong_candidates == True:
        #         wrong_candidates = False
        #     elif row_counter > largest_row_count:
        #         largest_row_count = row_counter
        #         largest_file_name = file_name
        # if largest_file_name != "":
        #     with open(largest_file_name, "ab") as phase_one_file:
        #         writer = csv.writer(phase_one_file)
        #         writer.writerow(block.get_candidates())
        # else:
        #     random_number = (randint(1000, 9999))
        #     file_name ="../blockchains/phase_one/blockchain{}.csv".format(random_number)
        #     with open(file_name, "wb") as phase_one_file:
        #         writer = csv.writer(phase_one_file)
        #         to_write = block.get_candidates()
        #         to_write.append(block.get_previous_hash())
        #         to_write.append(block.get_hash())
        #         writer.writerow(to_write)

def phase_two():
    pass

def phase_three():
    pass

if __name__ == '__main__':
    phase_one()
    # file_names = glob.glob("../blockchains/*")
    # print file_names
