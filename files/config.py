from pathlib import Path

BASE_PATH = Path(__file__).parent

# Path to the music files
FILES_PATH = (BASE_PATH / "../music/").resolve()

# Path to statistics file
STATS_PATH = (BASE_PATH / "./stats.json").resolve()

# Audio file formats allowed
FILE_FORMATS = (".mp3", ".MP3", ".wav", ".m4a")

# Skip folder content
SKIP_FOLDERS = []

DURATIONS = [1,2,4,7,11,16,25] # 25 is a flag for DURATIONS end
