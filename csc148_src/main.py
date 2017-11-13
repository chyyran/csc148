
def main():
    print("Hello World")
    pass

def my_unit(x: int):
    return x + 1

def testable_unit_test():
    assert my_unit(4) == 5
    assert my_unit(4) != 6

if __name__ == "__main__":
    main()