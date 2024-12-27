import os

level_images = dict()
list_file = [
    file for file in os.listdir("data") if file[-4:] == ".txt" and file[:5] == "level"
]

for i in list_file:
    level_images[i[:-4]] = i[:-4]+'.png'

for i in level_images:
    print(level_images[i])