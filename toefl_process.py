#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io, os, json

source_f = io.open("toefl.txt", "r")

source = source_f.read()
entries = [
    entry.split('\t')
    for entry in source.split("\n")
][:-1]

word_dict = {}

for entry in entries:
    word_dict[entry[0]] = entry[1:]

out_f = io.open("word_dict_toefl.json", "w")
out_f.write(json.dumps(word_dict))

