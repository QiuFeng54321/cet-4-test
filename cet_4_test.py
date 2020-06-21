import json, io, random
f = io.open("E:/word_dict_cet4.json", "r")
word_dict = json.loads(f.read())

def random_test():
    while True:
        word = random.choice(list(word_dict.keys()))
        definition = word_dict[word]
        ans = input(word + ": ")
        print(word, ":", definition)
        if ans == "q":
            return None

random_test()