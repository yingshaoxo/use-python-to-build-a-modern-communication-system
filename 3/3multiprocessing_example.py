from multiprocessing import Process


def my_function(x):
    print(x**2)


if __name__ == '__main__':
    p = Process(target=my_function, args=(3,))
    p.start()
    print("3 to the power of 2 is: ")
