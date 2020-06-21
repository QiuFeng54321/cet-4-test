import json, io, random, os

statistics = {
    "random_test": {
        "incorrect": {},
        "correct": {}
    },
    "multiple_choice_wd": {
        "incorrect": {},
        "correct": {}
    },
    "multiple_choice_dw": {
        "incorrect": {},
        "correct": {}
    }
}
if os.path.isfile("statistics.json"):
    statistics = json.loads(io.open("statistics.json", "r").read())

f = io.open("word_dict_cet4.json", "r")
word_dict = json.loads(f.read())

def quit():
    statistics_f = io.open("statistics.json", "w")
    statistics_f.write(json.dumps(statistics))
    statistics_f.close()
    exit()

def print_statistics():
    for k, v in statistics.items():
        print(k + ": ")
        print("\tIncorrect: ")
        for w, t in v["incorrect"].items():
            print("\t\t" + w.ljust(10) + ": " + t + " time(s)")
        print("\tCorrect: ")
        for w, t in v["correct"].items():
            print("\t\t" + w.ljust(10) + ": " + t + " time(s)")

def random_word():
    return random.choice(list(word_dict.keys()))

def random_words(k):
    return random.sample(list(word_dict.keys()), k)

def random_test():
    while True:
        word = random_word()
        definition = word_dict[word]
        ans = input(word + ": ")
        print(word, ":", pretty_def(definition, pretty_example = True))
        if ans == "q":
            return None
def print_separation():
    print()
    print('---------------------------------------')
    print()

def pretty_def(definition, show_example: bool = True, pretty_example: bool = True):
    if show_example:
        if pretty_example:
            return "\nExample: ".join(definition.split(":"))
        return definition
    return definition.split(":")[0]

def multiple_choice_test_agent(inverse: bool = False):
    def agent():
        while True:
            print_separation()
            confusing_words = random_words(4)
            correct_answer = random.randint(0, 3)
            correct_word = confusing_words[correct_answer]
            correct_definition = word_dict[correct_word]
            print(correct_word if inverse else pretty_def(correct_definition, False))
            for i in range(4):
                print(i + 1, pretty_def(word_dict[confusing_words[i]], show_example = False) if inverse else confusing_words[i])
            answer = input('What do you choose [1-4]')
            if answer == "q":
                break
            if answer.isdigit():
                answer = int(answer)
                if answer - 1 == correct_answer:
                    print("Correct!")
                else:
                    print("No!")
            print(correct_word, ":", pretty_def(correct_definition))
    return agent

operations = {
    "N" : ("Normal test", random_test),
    "M" : ("Multiple choice(definition->words)", multiple_choice_test_agent(False)),
    "IM": ("Multiple choice(word->definitions)", multiple_choice_test_agent(True)),
    "S" : ("Statistics", print_statistics),
    "Q" : ("Quit", quit)
}


def main():
    while True:
        print("Tests to take:")
        for k,v in operations.items():
            print(f"[{k.ljust(3)}]: {v[0]}")
        operation = input("What type of test do you want to take?")
        operation = operation.upper()
        if not operation in operations.keys():
            print("Not an option.")
            continue
        operation = operations[operation][1]
        operation()

main()
