import json, io, random, os, re
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
if os.path.isfile("statistics.json"):
    statistics = json.loads(io.open("statistics.json", "r").read())

f = io.open("word_dict_cet4.json", "r")
word_dict: dict = json.loads(f.read())

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
            if time_tried > max_try_time and max_try_time != -1:
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
            print("\t\t" + w.ljust(10) + ": " + str(t) + " time(s)")
        print("\tCorrect: ")
        for w, t in v["correct"].items():
            print("\t\t" + w.ljust(10) + ": " + str(t) + " time(s)")

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
    new_def: str = copy.copy(definition)
    new_def = replace_def.sub("", new_def, 1)
    if show_example:
        if pretty_example:
            return "\nExample: ".join(new_def.split(":"))
        return new_def
    return new_def.split(":")[0]

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
        word = input("Type a word or quit[word/q]: ")
        if word.lower() == "q":
            break
        found = get_exact_words(word)
        if len(found) == 0:
            print("Vocab not in word dictionary...")
        print("Requested / Similar word(s):", ", ".join(found))
        print()
        for w in found:
            if w == word:
                print("Exact word found: ")
            else:
                print("Similar word: ")
            print(w, ":", pretty_def(word_dict[w]))
            print()
        if word not in found:
            print("The exact word you want to find does not exist in the word dictionary.")
            lookup = input("Do you want to loop it up from the Internet? [any/y]: ")
            if lookup != "y":
                continue
            definitions = get_definition_from_internet([word], 5)
            if definitions[0] == None:
                print("Sorry. The definition also does not exist in dictionary.reference.com.....")
                continue
            print(word, ":", pretty_def(definitions[0]))

operations = {
    "N" : ("Normal test", random_test),
    "M" : ("Multiple choice(definition->words)", multiple_choice_test_agent(False)),
    "IM": ("Multiple choice(word->definitions)", multiple_choice_test_agent(True)),
    "L" : ("Lookup words", lookup_words),
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
