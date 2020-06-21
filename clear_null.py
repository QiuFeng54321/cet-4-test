import json
import os
import io

f = io.open("E:/out.txt", "r")
j = json.loads(f.read())
word_dict = {}
for word in j:
    if len(word) > 1 and word[-1] is not None:
        word_dict[word[0]] = word[1].replace(word[0].capitalize() + " definition, ", '')
    else:
        print(word)
        # word_dict[word[0]] = None
word_dict["succession"] = "a number of people or things sharing a specified characteristic and following one after " \
                          "the other. "
word_dict["reservoir"] = "a large natural or artificial lake used as a source of water supply."
word_dict["systematic"] = "done or acting according to a fixed plan or system; methodical."

out = io.open("E:/word_dict_cet4.json", "w")
out.write(json.dumps(word_dict))
out.close()
