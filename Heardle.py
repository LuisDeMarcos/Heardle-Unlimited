# IMPORTS ======================================================

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
from pygame import mixer
import files.functions as funcs
import files.config as conf
from files.library import Library

# START GAME ======================================================

def start(mixer, library, statistics):

        # Loads random song from the library and gets title (str)
        song, title = funcs.load_song(library)

        for duration in conf.DURATIONS[:-1]:
            print("Duration: {} seconds (ctrl+c to stop music)".format(duration))

            while True:
                # Play music until end or stopped via KeyboardInterrupt
                mixer.music.play()
                try:
                    time.sleep(duration)
                except KeyboardInterrupt:
                    pass
                mixer.music.stop()

                # User guess the song title
                guess = input('Your guess (leave empty for options):')
                answer = funcs.show_choices(library, guess)
                if answer == title:
                    print("Correct!")
                    statistics[str(duration)] += 1
                    return None
                elif answer == "*Replay":
                    continue
                elif answer == "*Surrender":
                    print("The song was: \n{}".format(title))
                    statistics["25"] += 1
                    return None
                elif answer == "*End Game":
                    return True
                else:
                    break
        statistics["25"] += 1
        print("The song was: \n{}".format(title))

def main():

    # Initialize mixer
    mixer.init()
    # Load music library
    library = Library(conf.FILES_PATH, conf.FILE_FORMATS)
    library.load_library()
    library = funcs.load_library()
    # Load/Initialize statistics
    stats = funcs.load_stats(conf.STATS_PATH)

    # Run until KeyboardInterrupt exception is received or game is ended
    while True:
        try:
            if not start(mixer, library, stats):
                print('\nAccuracy: {}\n'.format(funcs.calculate_accuracy(stats)))
            else:
                funcs.save_stats(conf.STATS_PATH, stats)
                break
        except KeyboardInterrupt:
            # Save statistics
            funcs.save_stats(conf.STATS_PATH, stats)
            break

if __name__ == '__main__':
    main()
    print("Goodbye!\n")
