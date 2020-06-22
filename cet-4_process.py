import json
import os
import io

f = io.open("out.txt", "r")
j = json.loads(f.read())
word_dict = {}
for word in j:
    if len(word) > 1 and word[-1] is not None:
        definition = word[1].replace(word[0].capitalize() + " definition, ", "").split(": ")
        example = definition[1] if len(definition) > 1 else ""
        definition = definition[0]

        word_dict[word[0]] = [definition, example]
    else:
        print(word)
        # word_dict[word[0]] = None
word_dict["succession"] = ["a number of people or things sharing a specified characteristic and following one after " \
                          "the other. ", ""]
word_dict["reservoir"] = ["a large natural or artificial lake used as a source of water supply.", ""]
word_dict["systematic"] = ["done or acting according to a fixed plan or system; methodical.", ""]

out = io.open("word_dict_cet4.json", "w")
out.write(json.dumps(word_dict))
out.close()
