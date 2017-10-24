

class Test:
    def __init__(self, *args, **kwargs):
        self.test = "Test return"
        print(kwargs["kayla"])
        print("kayla" in kwargs.keys())
        print(kwargs)
        
    def log(self):
        return self.test

if __name__ == "__main__":
    lol = Test(adam="Adam", kayla="Kayla")
    dict = {}

    dict["lol"] = "one"
    dict["lol"] = "two"

    print(dict["lol"])