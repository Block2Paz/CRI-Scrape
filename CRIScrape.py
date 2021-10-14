"""
This work is licensed under a GNU General Public License v3.0 License.
Discord: Block2Paz#4884 | Website: vcardone.it | Email: serpt@vcardone.it
"""

import os
import users
import courses
import configparser
from printy import printy, inputy


def main():
    config = configparser.ConfigParser()

    if not os.path.exists("Courses/Italy"):
        os.makedirs("Courses/Italy")
    if not os.path.exists("Courses/Sicily"):
        os.makedirs("Courses/Sicily")
    if not os.path.exists("GAIAUsers"):
        os.makedirs("GAIAUsers")

    printy("CRI Scraper | Coded by Block2Paz", "c")
    printy("Website: vcardone.it", "c>")
    printy("Discord: Block2Paz#4884", "c>")
    printy("Version: 1.1\n", "c>")

    printy("———————— SELECT AN OPTION ————————", "y>")
    printy(" 1 » Italy Courses", "r>")
    printy(" 2 » Sicily Courses", "r>")
    printy(" 3 » Users registered on GAIA", "r>")
    printy(" 0 » EXIT", "r>")

    while True:
        select = inputy("\nWAITING » ", "y>")

        if not os.path.exists('config.ini'):
            printy("\nCreating config file..")
            email = inputy(" » Enter GAIA email: ")
            passwd = inputy(" » Enter GAIA password: ")
            config['LOGIN'] = {'email': email, 'passwd': passwd}
            config['COURSES'] = {'lastfinalid': '1'}
            config['USERS'] = {'lastfinalid': '1'}
            config.write(open('config.ini', 'w'))

        if select == "1" or select == "2":
            courses.crsi(select)
            break
        elif select == "3":
            users.usr()
            break
        elif select == "0":
            exit()
        else:
            printy("ERROR: Invalid selection!", "r")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
