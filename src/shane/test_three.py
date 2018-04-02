from multiprocessing import Process, Lock




def main():
    a = 1
    b = 2
    print a
    print b

    def sum():
        return a+b

    print sum()

if __name__ == '__main__':
    main()
