import datetime
from src.YggNewspapersInterface import YggNewspaperInterface

"""Test the match and parse functions."""


def test_The_Economist():
    """
    Test if the function match and parse are working on some entries.
    Note: The date can be overlapping two months
    """
    # the easy case
    name = "The Economist (Europe) du 22-28 octobre 2022 [PDF] EN "
    assert YggNewspaperInterface.match("The Economist", name)
    assert YggNewspaperInterface.parse("The Economist", name) == datetime.datetime(day=22, month=10, year=2022)
    # when the date are overlapping different months
    name = "The Economist (Europe) du 29 octobre - 4 novembre 2022 [PDF] EN "
    assert YggNewspaperInterface.match("The Economist", name)
    assert YggNewspaperInterface.parse("The Economist", name) == datetime.datetime(day=29, month=10, year=2022)


def test_Le_Monde():
    """
    Test if the function match and parse are working on some entries.
    Note: Some torrents are packing several days existing independently, only single should match
    """
    name = "Le Monde du 03 Novembre 2022 Pdf"
    assert YggNewspaperInterface.match("Le Monde", name)
    assert YggNewspaperInterface.parse("Le Monde", name) == datetime.datetime(day=3, month=11, year=2022)


def test_Le_Monde_Diplomatique():
    """
    Test if the function match and parse are working on some entries.
    Note: Those torrents are released through different extensions, only PDF should match
    """
    # wrong format here
    name = "Le.Monde.Diplomatique.N824.Novembre.2022.FRENCH.AZW3-MarT"
    assert not YggNewspaperInterface.match("Le Monde Diplomatique", name)
    # easy case
    name = "Le.Monde.Diplomatique.N824.Novembre.2022.FRENCH.PDF-MarT"
    assert YggNewspaperInterface.match("Le Monde Diplomatique", name)
    assert YggNewspaperInterface.parse("Le Monde Diplomatique", name) == datetime.datetime(day=1, month=11, year=2022)


def test_Le_Canard_Enchaine():
    """
    Test if the function match and parse are working on some entries.
    Note: Different naming conventions are used and here the accents can be changing
    """
    name = "Le Canard enchaîné - 2 Mars 2022 Cbr"
    assert not YggNewspaperInterface.match("Le Canard Enchaîné", name)

    name = "Le canard enchainé du Mercredi 10 Aout 2022 Pdf"
    assert YggNewspaperInterface.match("Le Canard Enchaîné", name)
    assert YggNewspaperInterface.parse("Le Canard Enchaîné", name) == datetime.datetime(day=10, month=8, year=2022)
