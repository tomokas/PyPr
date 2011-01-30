import pypr

if __name__ == "__main__":
    # Remember to change the key!
    mypypr = pypr.Pypr("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                        
    try:
        mypypr.add(0, "PyPr Test", "Test", "Hi!")
    except pypr.PyprError as e:
        print(e.message)