from re import match,Match
from os import listdir,remove
from os.path import exists

l=listdir("imgs")
for file in l:
    rst:Match = match(r"序号\d+_(.+)_照片_.+",file)
    if rst is None:continue
    name=rst.group(1)
    if exists(f"imgs/{name}.png"):
        remove(f"imgs/{name}.png")