import re
import requests
def find(x):
    srch=str(x)
    x=requests.get("https://definition.williamcraft.workers.dev/?word=" + srch)
    x=x.text
    print(x)
x=input("Enter word to find: ")
find(x)