import json, io, random
f = io.open("word_dict_cet4.json", "r")
word_dict = json.loads(f.read())

def random_word():
    return random.choice(list(word_dict.keys()))

def random_test():
    while True:
        word = random_word()
        definition = word_dict[word]
        ans = input(word + ": ")
        print(word, ":", definition)
        if ans == "q":
            return None

def multiple_choice_test():
    while True:
        print()
        print("-------------------------------------------")
        print()
        confusing_words = [random_word() for i in range(4)]
        correct_answer = random.randint(0, 3)
        correct_word = confusing_words[correct_answer]
        correct_definition = word_dict[correct_word]
        print(correct_definition.split(':')[0]) # We don't want the example sentence with the correct word along.
        for i in range(4):
            print(i + 1, ":", confusing_words[i])
        answer = input("What do you choose [1-4]: ")
        if answer == "q":
            break
        if answer.isdigit():
            answer = int(answer)
            if answer - 1 == correct_answer:
                print("Correct!")
            else:
                print("No!")
        print(correct_word, ":", correct_definition)


multiple_choice_test()
