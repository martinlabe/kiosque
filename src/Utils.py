import time
import random


class Utils:
    """Class storing useful functions."""

    @staticmethod
    def random_sleep(alpha=2, beta=2):
        """Sleep randomly to avoid being detected as a robot."""
        time.sleep(alpha * random.random() + beta)

    @staticmethod
    def get_credentials(filename):
        """Load the credentials from a file."""
        file = open(filename, "r")
        email = file.readline().strip()
        password = file.readline().strip()
        return email, password

