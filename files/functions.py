from os import walk
import re
from random import randint
import inquirer
from pygame import mixer
from .config import *
import numpy as np
import json

# PROCESSING & MATCHING ======================================================

translate = lambda x: x.translate(x.maketrans("áàäéèëíìïòóöùúüÀÁÄÈÉËÌÍÏÒÓÖÙÚÜ",
                                            "aaaeeeiiiooouuuAAAEEEIIIOOOUUU"))

def process_text(text):
    # Remove tildes and accents, lower and remove contractions
    text = translate(text).lower().replace("'", "")
    # Remove special characters
    return re.sub('[^A-Za-z0-9]+', ' ', text)

def is_match(ref, guess):
    # Process strings before comparing, then split
    ref = process_text(ref).split()
    guess = process_text(guess).split()
    # Check if all words in guess are contained in reference

    if len([x for x in guess if any([1 for y in ref if x in y])]) == len(guess):
        return True
    return False

def matching_titles(library, guess):
    return [x['title'] for x in library if is_match(x['title'], guess)]

def show_choices(library, guess):
    if guess:
        choices = matching_titles(library, guess)
    else:
        choices = []
    questions = [
      inquirer.List('title',
                    message="Choose between the options",
                    choices=choices + ['*Replay', '*Skip', '*Surrender', '*End Game'],
                ),
    ]
    return inquirer.prompt(questions)["title"]

# DATA LOAD ======================================================

def load_library():
    song_files = []
    for root, dirs, files in walk(FILES_PATH):
        if root.split('/')[-1] in SKIP_FOLDERS:
            continue
        for name in files:
            try:
                if name.endswith(FILE_FORMATS):
                    song_files.append({
                        'path': f"{root}/{name}",
                        'title': "".join(name.split('.')[:-1])
                    })
            except Exception as e:
                continue
    if len(song_files) == 0:
        print("No music found at {}".format(FILES_PATH))
        exit()
    return song_files

def load_song(library):
    while True:
        try:
            song = library[randint(0, len(library)-1)]
            mixer.music.load(song['path'])
            return song['path'], song['title']
        except:
            continue

# STATS ############################################

def calculate_accuracy(stats):
    def calculate_score(x):
        return ((x-25)**2)/5.76

    acc = sum([[calculate_score(int(x[0])) for y in range(x[1])] for x in stats.items()], [])
    return round(np.mean(acc), 2)

def load_stats(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return dict.fromkeys([str(x) for x in DURATIONS], 0)

def save_stats(path, stats):
    with open(path, "w") as f:
        f.write(json.dumps(stats))
