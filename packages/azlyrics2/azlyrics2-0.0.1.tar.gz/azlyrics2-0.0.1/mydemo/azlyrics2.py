import sys, argparse
from azlyrics import Azlyrics, Cache

class DstiLyrics(Azlyrics):
    """This class extends the azlyrics module
    In this module we can:
        - add new methods/functionalities
        - change behavior of inherited methods

    """


    def __init__(self, artist, song_title):
        super().__init__(artist, song_title)

    def fetch_words(self, lyrics_list):
        """Fetch a list of words from a list of sentences.

            Args:
                lyrics_list: List of string from lyrics.

            Retrurn:
                A list of string containing the words from
                the text document.
        """

        words = []
        for line in lyrics_list:
            line_words = line.split()
            for word in line_words:
                words.append(word)

        return words


def run():
    parser = argparse.ArgumentParser(description="Fetch lyric from azlyric")
    parser.add_argument("artist", metavar="Artist", type=str)
    parser.add_argument("song_title", metavar="Song", type=str)
    parser.add_argument("-s", "--save", metavar="path", help="Save to the file", default=False, dest="path")
    args = parser.parse_args()

    c = Cache()
    az = DstiLyrics(args.artist, args.song_title)
    cache_key = '_'.join(az.normalize_artist_music())

    lyrics = c.get(cache_key)
    if lyrics is None:
        lyrics = az.format_lyrics(az.get_lyrics())
        c.add(cache_key, lyrics)
    if args.path:
        az.save_lyrics_to_file(args.path, lyrics)
    else:
        print(az.format_title())
        print(lyrics)

if __name__ == "__main__":
    run()