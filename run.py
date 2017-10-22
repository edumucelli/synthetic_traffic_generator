import generator
import sys
from os import path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        number_of_synthetic_users = int(sys.argv[1])
    else:
        number_of_synthetic_users = generator.NUMBER_OF_SYNTHETIC_USERS

    print "[+] Generating %d synthetic users and their respective hourly traffic" % number_of_synthetic_users
    print "[+] Per-user synthetic traffic will be stored in '%s'" % path.join('.', generator.USERS_DIRECTORY,
                                                                              generator.SYNTHETIC_DIRECTORY)
    generator.generate_synthethic_users_and_traffic(number_of_synthetic_users)
