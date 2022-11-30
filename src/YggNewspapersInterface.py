import requests
import re
import dateparser
import datetime
import qbittorrent
from yggtorrentscraper import YggTorrentScraper

from .Utils import Utils

# the default options used by our program
# to modify them add yours directly in the main
DEFAULT_OPTIONS = {
    # files storing information
    "history": "downloads.txt",
    "credentials": "credentials.txt",
    # directory to store
    "magnet": "./magnet/",
    "library": "./library/",
    # qbittorrent server options
    "qbittorrent_server": "http://127.0.0.1:8080/",
    "qbittorrent_username": "admin",
    "qbittorrent_password": "adminadmin",
}


class YggNewspaperInterface:

    def __init__(self, verbose=True, options=None):
        """
        Create an object allowing the user to download the newspapers.

        Args:
            verbose: print a message for every step in stdout if True
            options: a dictionary allowing the user to overwrite the DEFAULT_OPTIONS.
        """
        self.verbose = verbose
        if self.verbose:
            print(f"## YGGNEWSPAPERINTERFACE")
        self.options = DEFAULT_OPTIONS | options
        self.history = self.options["history"]
        self.__username, self.__password = Utils.get_credentials(self.options["credentials"])

        Utils.random_sleep()
        self.scrapper = self.get_scrapper()

        Utils.random_sleep()
        self.__sign_in()

    def __sign_in(self):
        """
        Sign in YggTorrent.

        Raises:
            Exception: if the login failed.
        """
        if self.scrapper.login(self.__username, self.__password):
            if self.verbose:
                print("### login successfully to YggTorrent.")
        else:
            raise Exception(f"login failed with username ({self.__username}) and password ({self.__password}).")

    def is_in_history(self, url):
        """
        Check if the requested url is stored in the history of downloads.

        Args:
            url (str): the ygg url for the requested torrent
        Returns:
            bool: True if the url is stored, False otherwise
        """
        file = open(self.history, "r")
        lines = file.readlines()
        for line in lines:
            if url in line:
                return True
        return False

    def add_in_history(self, url):
        """
        Add the requested url in the history of downloads.

        Args:
            url (str): the ygg url for the requested torrent
        """
        file = open(self.history, "a")
        file.write(url + "\n")
        file.close()

    @staticmethod
    def get_scrapper():
        """Return a configured scraper object."""
        session = requests.session()
        return YggTorrentScraper(session)

    @staticmethod
    def print_torrent(infos):
        """Pretty-print of the main torrent infos."""
        print(f"###### uploaded:  {infos.uploaded_datetime}")
        print(f"###### size:      {infos.size}")
        print(f"###### completed: {infos.completed}")
        print(f"###### seeders:   {infos.seeders}")
        print(f"###### leechers:  {infos.leechers}")

    @staticmethod
    def get_request_for(media):
        """
        Return the request to use on YggTorrent to have the list of the most likely matching torrents.

        Args:
            media (str): the name of the newspaper
        Raises:
            Exception: if the media is not supported
        """
        if media == "The Economist":
            return "the economist europe du"
        elif media == "Le Canard Enchaîné":
            return "le canard enchaine"
        elif media == "Le Monde":
            return "le monde du"
        elif media == "Le Monde Diplomatique":
            return "le monde diplomatique"
        else:
            raise Exception("unknown media.")

    @staticmethod
    def parse(media, name):
        """
        Parse the date in the name of the torrent.

        Args:
            media (str): the name of the newspaper
            name (str): the name of the torrent
        Returns:
            datetime: the date parsed
        Raises:
            Exception: if the media is not supported
        """
        if media == "The Economist":
            res = re.search("[0-9]+[ \w]*20[0-9]{2}", name)
            return dateparser.parse(res[0], languages=["fr", "en"]) - datetime.timedelta(days=6)
        if media == "Le Canard Enchaîné":
            res = re.search("[0-9]+.*20[0-9]{2}", name)
            return dateparser.parse(res[0], languages=["fr", "en"])
        if media == "Le Monde":
            s = name[len("Le Monde du "):-len(" Pdf")]
            return dateparser.parse(s, languages=["fr", "en"])
        if media == "Le Monde Diplomatique":
            res = re.search("[ .]\w*.20[0-9]{2}", name)
            return dateparser.parse(res[0], languages=["fr", "en"]).replace(day=1)
        raise Exception("unknown media.")

    @staticmethod
    def match(media, name):
        """
        Returns if the torrent name belong to the newspaper convention used on YggTorrent.

        Args:
            media (str): the name of the newspaper
            name (str): the name of the torrent
        Returns:
            bool: True if matching, Else otherwise
        Raises:
            Exception: if the media is not supported
        """
        pattern = None
        if media == "The Economist":
            pattern = "^(the.economist.\(europe\).du.).+pdf"
        elif media == "Le Canard Enchaîné":
            pattern = "le canard encha[iî]n[eé].*pdf"
        elif media == "Le Monde":
            pattern = "^(le.monde.du.).+pdf"
        elif media == "Le Monde Diplomatique":
            pattern = "^(le.monde.diplomatique).+pdf"
        else:
            raise Exception("unknown media.")
        return re.match(pattern, name, re.IGNORECASE) is not None

    def download(self, url, infos, media):
        """
        Get the magnet file from YggTorrent and launch the download on qbittorrent.

        Args:
            url (str): the ygg url for the requested torrent
            infos (Torrent from YggTorrentScrapper): the torrent to download
            media (str): the name of the newspaper
        """
        # filename
        date_release = YggNewspaperInterface.parse(media, infos.name)
        filename = date_release.strftime('%Y-%m-%d') + f" {media}"

        # download the magnet
        Utils.random_sleep()
        self.scrapper.download_from_torrent_url(url, self.options["magnet"], filename)
        self.add_in_history(url)

        # download the torrent
        qb = qbittorrent.Client(self.options["qbittorrent_server"])
        qb.login(self.options["qbittorrent_username"], self.options["qbittorrent_password"])
        torrent_file = open(f"{self.options['magnet']}{filename}", "rb")
        qb.download_from_file(torrent_file, savepath=f"{self.options['library']}{filename}")

    def requesting(self, media):
        """
        Request the last torrent and launch download if matchs.

        Args:
            media (str): the name of the newspaper
        """
        if self.verbose:
            print(f"### requesting {media}")

        research = self.scrapper.search({
            "name": self.get_request_for(media),
            "sort": "publish_date",
            "order": "desc",
            "category": "2140",
            "sub_category": "2156"
        })

        limit = 9  # the maximum number of torrent to try before giving up
        for i in range(limit):
            Utils.random_sleep()
            infos = self.scrapper.extract_details(research[i])
            print(f"#### {infos.name}")

            if self.is_in_history(research[i]):
                if self.verbose:
                    print(f"##### already in history")
                break

            if self.match(media, infos.name):
                if self.verbose:
                    print(f"##### download launched")
                self.print_torrent(infos)
                self.download(research[i], infos, media)
            else:
                self.add_in_history(research[i])
                if self.verbose:
                    print(f"##### doesn't match")

            if i + 1 == limit:
                if self.verbose:
                    print(f"##### an error seems to have occur for {media} scrapping")
