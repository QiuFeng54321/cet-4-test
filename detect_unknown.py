#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/cet-4-test/detect_unknown.py           #
# Project: /Users/Shared/williamye/program/cet-4-test                          #
# Created Date: Monday, June 22nd 2020, 11:52:04 am                            #
# Author : Qiufeng54321                                                        #
# Email : williamcraft@163.com                                                 #
#                                                                              #
# Copyright (C) 2020  Qiufeng54321                                             #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
# You should have received a copy of the GNU General Public License            #
# along with this program.  If not, see <https://www.gnu.org/licenses/>.       #
# -----                                                                        #
# Description:                                                                 #
#                                                                              #
#                                                                              #
*------------------------------------------------------------------------------*
'''


import os, io, json, re
import requests

f = io.open("word_dict_cet4.json", "r")
word_dict = json.loads(f.read())
f.close()

dict_not_found = re.compile("\w+? definition at Dictionary.com, a free online dictionary with pronunciation, synonyms and translation. Look it up now!\">")
dict_not_found_list = []
chunk = []
words_per_chunk = 15

for word, definition in word_dict.items():
    if dict_not_found.match(definition):
        print(word, "has an improper definition")
        if len(chunk) >= words_per_chunk:
            dict_not_found_list.append(chunk)
            chunk = []
        chunk.append(word)

for chunk in dict_not_found_list:
    print("Chunk:", json.dumps(chunk))
    while True:
        try:
            x = requests.post("https://definition.williamcraft.workers.dev/", timeout=20,
                              data=json.dumps(chunk))
            text = x.text
            x = json.loads(text)
            for i in range(len(x)):
                # actual_i = to_be_searched_i[index + i]
                # str_list[actual_i].append(x[i])
                print(chunk[i], ":", x[i])
            break
        except Exception as e:
            print(e)
            print("Try again...")
            pass
