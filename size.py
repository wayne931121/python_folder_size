import os
from wcwidth import wcswidth
from tqdm import tqdm

# https://www.geeksforgeeks.org/how-to-get-size-of-folder-using-python/
# https://stackoverflow.com/questions/37335064/how-to-pad-and-align-unicode-strings-with-special-characters-in-python

def getSize(bytes_): # input is bytes.
    kb = bytes_/d
    if int(kb)==0: return "%5d bytes"%bytes_
    mb = kb/d
    if int(mb)==0: return "%5d KB"%kb
    gb = mb/d
    if int(gb)==0: return "%5d MB"%mb
    tb = gb/d
    if int(tb)==0: return "%5d GB"%gb
    return "%5d TB"%tb

# pbar.set_postfix_str("epoch %d, Total loss = %.7f"%(epoch, now_loss_value))
def update():
    global tmp; tmp += 1
    if tmp>=total_size_f:
        pbar.update(tmp); tmp = 0
def update_v(v):
    global tmp; tmp += v
    if tmp>=total_size_f:
        pbar.update(tmp); tmp = 0

def string(*args):
    s = 90-wcswidth(args[0])
    if s>0: return args[0]+" "*(s)+args[1]
    return args[0]+"\t"+args[1]

flag = 1

while flag:
    path = input("Please Input a Path: \n")
    try:
        os.listdir(path)
        flag = 0
    except:
        print("Please Input a Real Path.")
print("Counting...")
d = 1024
l = list(os.walk(path))
total_size = 1
align = "{0:　<70}\t{1}"
tmp = 1

for i in l:
    path_, folders_, files_ = i
    total_size += len(folders_)+len(files_)

print("Total to Scanning: %d, Start Scanning... (We will not scan folder or file that has been protected.)"%total_size)
pbar = tqdm(total = total_size, ncols = 100)
folders = l[0][1]
files = l[0][2]
result_folders = []
result_files = []
root_size = 0
total_size_f = total_size*0.1

for folder in folders:
    size = 0; update()
    try:
        for path_, dirs_, files_ in os.walk(os.path.join(path,folder)):
            update_v(len(dirs_))
            for f in files_:
                try:
                    update(); fp = os.path.join(path_, f); size += os.path.getsize(fp)
                except:
                    pass
        root_size += size; result_folders.append((size, string(folder, getSize(size))))
    except:
        pass

for file in files:
    update()
    try:
        fp = os.path.join(path, file); size = os.path.getsize(fp); root_size += size; result_files.append((size, string(file, getSize(size))))
    except:
        pass

result_folders.sort()
result_folders.reverse()
result_files.sort()
result_files.reverse()
pbar.update(tmp)
pbar.close()
print()

print(string("Root Folder (The folder you input):", "   Size:"))
print("_"*110, end="\n\n")
print(string("root", getSize(root_size)))
print("\n")

print(string("Folders:", "   Size:"))
print("_"*110, end="\n\n")
for e in result_folders:
    print(e[1])
print("\n")

print(string("Files:", "   Size:"))
print("_"*110, end="\n\n")
for e in result_files:
    print(e[1])
print()