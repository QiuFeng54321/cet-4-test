import json, io, random, os, re, sys
import difflib
import requests

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

word_dict: dict = None
def change_word_dict():
    global word_dict
    word_dicts: list = list(filter(lambda x: x.startswith("word_dict_"), os.listdir()))
    for i in range(len(word_dicts)):
        print("[" + str(i + 1) + "]" + ": " + word_dicts[i])
    selection = input("Which word dictionary do you want to choose? [1-" + str(len(word_dicts)) + "/any[default=0]]: ")
    selection = int(selection) - 1 if selection.isdigit() else 0
    print("Chose " + word_dicts[selection])
    word_dict = json.loads(io.open(word_dicts[selection], "r").read())

if os.path.isfile("statistics.json"):
    statistics = json.loads(io.open("statistics.json", "r").read())

def get_exact_words(input_str):
    exact_words = difflib.get_close_matches(input_str, word_dict.keys())
    return exact_words

def get_definition_from_internet(words: list, max_try_time: int = -1):
    time_tried: int = 0
    while True:
        try:
            x = requests.post("https://definition.williamcraft.workers.dev/", timeout=20,
                              data=json.dumps(words))
            text = x.text
            x = json.loads(text)
            return x
            break
        except Exception as e:
            print(e)
            print("Try again...")
            time_tried += 1
            if time_tried >= max_try_time and max_try_time != -1:
                print("Try time exceeded", max_try_time)
                break
    return [None] * len(words)

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
            print("\t\t" + w.ljust(20) + ": " + str(t) + " time(s)")
        print("\tCorrect: ")
        for w, t in v["correct"].items():
            print("\t\t" + w.ljust(20) + ": " + str(t) + " time(s)")

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

replace_def = re.compile("\w+? definition, ")
def pretty_def(definition, show_example: bool = True, pretty_example: bool = True):
    import copy
    new_def: list = copy.copy(definition)
    new_def[0] = replace_def.sub("", new_def[0], 1)
    if show_example:
        if pretty_example:
            return new_def[0] + "\nExample: " + new_def[1]
    return new_def[0]

def multiple_choice_test_agent(inverse: bool = False):
    statistic_name = "multiple_choice_" + ("wd" if inverse else "dw")
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
                    statistics[statistic_name]["correct"][correct_word] = statistics[statistic_name]["correct"].get(correct_word, 0) + 1
                else:
                    print("No!")
                    statistics[statistic_name]["incorrect"][correct_word] = statistics[statistic_name]["incorrect"].get(correct_word, 0) + 1
            print(correct_word, ":", pretty_def(correct_definition))
    return agent

def lookup_words():
    while True:
        print_separation()
        word = input("Type a word or quit[word/q]: ").lower()
        if word.lower() == "q":
            break
        found = get_exact_words(word)
        if len(found) == 0:
            print("Vocab not in word dictionary...")
        print("Requested / Similar word(s):", ", ".join(found))
        print()
        exact_word_found: bool = False
        for w in found:
            if w.lower() == word:
                print("Exact word found: ")
                exact_word_found = True
            else:
                print("Similar word: ")
            print(w, ":", pretty_def(word_dict[w]))
            print()
        if not exact_word_found:
            print("The exact word you want to find does not exist in the word dictionary.")
            lookup = input("Do you want to look it up from the Internet? [any/y]: ")
            if lookup != "y":
                continue
            definitions = get_definition_from_internet([word], 5)
            if definitions[0] == None:
                print("Sorry. The definition also does not exist in dictionary.reference.com.....")
                continue
            definition: list = definitions[0].split(": ")
            if len(definition) < 2:
                definition.append("")
            print(word, ":", pretty_def(definition))

operations = {
    "NT" : ("Normal test", random_test),
    "MC" : ("Multiple choice(definition->words)", multiple_choice_test_agent(False)),
    "IMC": ("Multiple choice(word->definitions)", multiple_choice_test_agent(True)),
    "LW" : ("Lookup words", lookup_words),
    "S"  : ("Statistics", print_statistics),
    "RWD": ("Reselect word dict", change_word_dict), 
    "Q"  : ("Quit", quit)
}


def main():
    change_word_dict()
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
