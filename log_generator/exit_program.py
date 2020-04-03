""" Exit program """
from log_generator.dateTime_handler import get_dateNow

import sys

# sortir du programme
def exitProgram():
    print("Sortie du programme : " + get_dateNow())
    sys.exit()