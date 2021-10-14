"""
This work is licensed under a GNU General Public License v3.0 License.
Discord: Block2Paz#4884 | Website: vcardone.it | Email: serpt@vcardone.it
"""

import configparser
import requests
from lxml import html
from printy import printy, inputy


def usr():

    config = configparser.ConfigParser()
    config.read('config.ini')
    email = config['LOGIN']['email']
    passwd = config['LOGIN']['passwd']
    lastid = config['USERS']['lastfinalid']

    startid = inputy("\nInitial volunteer ID (Last final ID: " + lastid + "): ")
    endid = inputy("Final volunteer ID: ")

    urlgn = "https://gaia.cri.it/login/"

    headers = {
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
           'referer': 'https://gaia.cri.it/login/',
    }

    client = requests.session()
    client.get(urlgn, headers=headers)
    csrftoken = client.cookies['csrftoken']

    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'jorvik_login_view-current_step': 'auth',
        'auth-username': email,
        'auth-password': passwd,
        'next': '',
    }

    res = client.post(urlgn, data=payload, headers=headers)

    printy("\nStarting...\n")

    while int(startid) <= int(endid):
        urlsr = 'https://gaia.cri.it/profilo/' + str(startid)
        res = client.get(urlsr, headers=dict(referer=urlgn))
        if res.url == "https://gaia.cri.it/errore/permessi/":
            printy("\nERROR - Login failed, check your credentials in the config.ini file!", "r")
            break

        page = html.fromstring(res.content)
        nomev = page.xpath("/html/body/div[2]/h2/text()")
        scomitato = page.xpath("/html/body/div[2]/div/div[2]/div/div[2]/ul/li/a/text()")

        if len(nomev) < 1:
            printy("ERROR - " + str(startid) + " Pagina non trovata", "r")
        elif len(scomitato) < 1:
            printy("SUCCESS | " + str(startid) + " " + nomev[0], "n")
            f = open("GAIAUsers/without_role.txt", "a")
            f.write("ID: " + str(startid) + " | Name: " + nomev[0] + "\n")
            f.close()
        else:
            printy("SUCCESS | " + str(startid) + " " + nomev[0], "n")
            f = open("GAIAUsers/volunteers.txt", "a")
            f.write("ID: " + str(startid) + " | Name: " + nomev[0] + " | " + scomitato[0] + "\n")
            f.close()

        config['USERS'] = {'lastfinalid': startid}
        config.write(open('config.ini', 'w'))
        startid = int(startid) + 1


if __name__ == "__main__":
    try:
        usr()
    except KeyboardInterrupt:
        exit()
