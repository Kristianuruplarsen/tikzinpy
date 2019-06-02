
import os

# This just removes all files that are from building the latex documents
dircont = os.listdir()
for item in dircont:
    if item.endswith(('.log', '.aux', '.gz', '.fdb_latexmk', '.fls')):
        os.remove(item)

dircont2 = os.listdir('temp')
for item in dircont2:
    if item.endswith(('.log', '.aux', '.gz', '.fdb_latexmk', '.fls')):
        os.remove(os.path.join('temp', item))