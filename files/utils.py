import os

all_songs = []
repeated = []
path = "../music/LDM/"

def remove_duplicates():
    for f in os.listdir(path):
        title = " ".join(f.split(" - ")[1:])
        if title in all_songs:
            repeated.append(f)
        else:
            all_songs.append(title)

    print("Found {} duplicated songs".format(len(repeated)))

    for f in repeated:
        os.remove(path+f)

def clean_titles():
    for f in os.listdir(path):
        # title = " - ".join(f.split(" - ")[1:])
        title = f.split(" - ")
        try:
            int(title[0])
            title = " - ".join(title[1:])
            os.rename(path+f, path+title)
        except:
            continue

clean_titles()
