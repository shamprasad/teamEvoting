import hashlib as hasher
import datetime as date
from pprint import pprint

class Block:
  def __init__(self, index, voter, votee, timestamp, data, previous_hash):
    self.__index = index
    self.__voter = voter
    self.__votee = votee
    self.__timestamp = timestamp
    self.__data = data
    self.__previous_hash = previous_hash
    self.__hash = self.hash_block()
    self.encrypt()

  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.__index) +
               str(self.__voter) +
               str(self.__timestamp) +
               str(self.__data) +
               str(self.__previous_hash))
    return sha.hexdigest()

  def encrypt(self):
    sha = hasher.sha256()
    sha.update(str(self.__voter) + str(10))
    self.__voter = sha.hexdigest()
    sha = hasher.sha256()
    sha.update(str(self.__votee) + str(10))
    self.__votee = sha.hexdigest()

  def verify_voter(self, voter):
    sha = hasher.sha256()
    sha.update(str(voter) + str(10))
    print sha.hexdigest()

  def verify_votee(self, votee):
    sha = hasher.sha256()
    sha.update(str(votee) + str(10))
    print sha.hexdigest()

  def get_index(self):
      return self.__index

  def get_voter(self):
      return self.__voter

  def get_votee(self):
      return self.__votee

  def get_timestamp(self):
      return self.__timestamp

  def get_data(self):
      return self.__data

  def get_previous_hash(self):
      return self.__previous_hash

  def get_hash(self):
      return self.__hash

def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, "Genesis", "Genesis", date.datetime.now(), "Genesis Block", "0")

def next_block(last_block, voter, votee):
  this_index = last_block.get_index() + 1
  this_timestamp = date.datetime.now()
  this_data = "Hey! I'm block " + str(this_index)
  this_hash = last_block.get_hash()
  return Block(this_index, voter, votee, this_timestamp, this_data, this_hash)

if __name__ == "__main__":
    # Create the blockchain and add the genesis block
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]

    # How many blocks should we add to the chain
    # after the genesis block
    num_of_blocks_to_add = 4

    # Add blocks to the chain
    for i in range(0, num_of_blocks_to_add):
      block_to_add = next_block(previous_block, "voter's name", "votee's name")
      blockchain.append(block_to_add)
      previous_block = block_to_add

    for i in range(0, num_of_blocks_to_add):
      pprint(vars(blockchain[i]))
      blockchain[i].verify_voter("Genesis")
      blockchain[i].verify_votee("Genesis")
