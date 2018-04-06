from multiprocessing import Process, Lock
from blockchain import Blockchain

def main():
    return Blockchain(None)

if __name__ == '__main__':
    if main():
        print 'hello'
    else:
        print 'goodbye'
