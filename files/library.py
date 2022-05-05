from os import walk
from .config import *

class Library:

    def __init__(self, files_path, file_formats):
        self.files_path = files_path
        self.file_formats = file_formats

    def load_library(self):
        song_files = []
        for root, dirs, files in walk(self.files_path):
            if root.split('/')[-1] in SKIP_FOLDERS:
                continue
            for name in files:
                try:
                    if name.endswith(self.file_formats):
                        song_files.append({
                            'path': f"{root}/{name}",
                            'title': "".join(name.split('.')[:-1])
                        })
                except Exception as e:
                    continue
        if len(song_files) == 0:
            print("No music found at {}".format(self.files_path))
            exit()
        self.songs = song_files

    def load_song(self):
        while True:
            try:
                song = library[randint(0, len(library)-1)]
                mixer.music.load(song['path'])
                return song['path'], song['title']
            except:
                continue
