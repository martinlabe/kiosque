import requests
import pycountry


class ConnectionChecker:

    def __init__(self, country="Belgium", verbose=True):
        """
        Check if the VPN connection is working. Abort otherwise.
        This is just a security not to launch downloads if the VPN service crashed.

        Args:
            country: the country required for the connection
            verbose: print a message for every step in stdout if True
        Raises:
            Exception: if our connection is located outside the country
        """
        if verbose:
            print(f"## CONNECTION CHECKER")

        self.ip = ConnectionChecker.get_my_ip()
        self.country_code = ConnectionChecker.get_country_code(self.ip)
        self.country = ConnectionChecker.get_country(self.country_code)

        if verbose:
            print(f"### IP: {self.ip}")
            print(f"### COUNTRY: {self.country.flag} {self.country.name} ({self.country_code})")

        if self.country.name != country:
            raise Exception("VPN is not connected. Aborting.")

    @staticmethod
    def get_my_ip():
        """Return the ip address requesting ipify."""
        res = requests.get('https://api64.ipify.org?format=json')
        if res.status_code != 200:
            raise Exception(f"Impossible to find our ip address. Code {res.status_code}.")
        return res.json()["ip"]

    @staticmethod
    def get_country_code(ip):
        """Return the country code requesting ipinfo."""
        res = requests.get(f'https://ipinfo.io/{ip}/json')
        if res.status_code != 200:
            raise Exception(f"Impossible to find our country code. Code {res.status_code}.")
        return res.json()["country"]

    @staticmethod
    def get_country(country_code):
        """Return the country name using country code."""
        return pycountry.countries.get(alpha_2=country_code)
