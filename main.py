import sys

from src.ConnectionChecker import ConnectionChecker
from src.YggNewspapersInterface import YggNewspaperInterface
from test.YggNewspaperInterface import *

if __name__ == '__main__':

    # TEST
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_The_Economist()
            test_Le_Monde()
            test_Le_Monde_Diplomatique()
            test_Le_Canard_Enchaine()
            print("All the tests worked")
            exit(0)
        else:
            raise Exception("Wrong usage. Only --test can be passed as an argument")

    # MAIN
    print("# KIOSQUE")

    # check the VPN connection is working
    connection = ConnectionChecker(verbose=True, country="Belgium")

    opt = {
        "history": "downloads.txt",
        "credentials": "credentials.txt",
        "library": "/home/martin/Data/kiosque/Kiosque/",
    }

    # configure the connection to Ygg
    interface = YggNewspaperInterface(verbose=True, options=opt)

    medias = [
        "The Economist",
        "Le Canard Enchaîné",
        "Le Monde",
        "Le Monde Diplomatique",
    ]

    for media in medias:
        interface.requesting(media)

    print("# END")
