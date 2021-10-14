"""
This work is licensed under a GNU General Public License v3.0 License.
Discord: Block2Paz#4884 | Website: vcardone.it | Email: serpt@vcardone.it
"""

import configparser
import requests
from lxml import html
from printy import printy, inputy


def crsi(select):
    comsicilia = ["Comitato del Tirreno-Nebrodi", "Comitato di Acireale", "Comitato di Agrigento", "Comitato di Alcamo",
                  "Comitato di Avola", "Comitato di Barcellona Pozzo di Gotto", "Comitato di Caltagirone",
                  "Comitato di Caltanissetta", "Comitato di Campofelice di Roccella", "Comitato di Castelvetrano",
                  "Comitato di Catania", "Comitato di Enna", "Comitato di Fiumefreddo di Sicilia",
                  "Comitato di Francofonte", "Comitato di Gela", "Comitato di Lampedusa e Linosa",
                  "Comitato di Marsala", "Comitato di Mascalucia", "Comitato di Mazara Del Vallo",
                  "Comitato di Messina", "Comitato di Milazzo - Isole Eolie", "Comitato di Mussomeli",
                  "Comitato di Nicosia", "Comitato di Noto", "Comitato di Pachino / Portopalo", "Comitato di Palermo",
                  "Comitato di Pantelleria", "Comitato di Ragusa", "Comitato di Roccalumera e Taormina",
                  "Comitato di San Salvatore di Fitalia", "Comitato di Scordia", "Comitato di Siracusa",
                  "Comitato di Trapani", "Comitato di Troina", "Comitato di Valle dell'Halaesa",
                  "Comitato di Viagrande", "Comitato Floridia - ODV", "Comitato Jonico-etneo"]

    config = configparser.ConfigParser()
    config.read('config.ini')
    email = config['LOGIN']['email']
    passwd = config['LOGIN']['passwd']
    lastid = config['COURSES']['lastfinalid']

    startid = inputy("\nInitial course ID (Last final ID: " + lastid + "): ")
    endid = inputy("Final course ID: ")

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
        urlcrse = 'https://gaia.cri.it/aspirante/corso-base/' + str(startid)
        res = client.get(urlcrse, headers=dict(referer=urlgn))
        if res.url == "https://gaia.cri.it/errore/permessi/":
            printy("\nERROR - Login failed, check your credentials in the config.ini file!", "r")
            break

        page = html.fromstring(res.content)
        scomitato = page.xpath("/html/body/div[2]/div[2]/div[3]/div[3]/div[2]/div/div[2]/strong/a/text()")
        snamec = page.xpath("/html/body/div[2]/div[2]/div[3]/h4[1]/text()")
        sstart = page.xpath("/html/body/div[2]/div[2]/div[3]/div[3]/div[3]/div/div[2]/text()")
        send = page.xpath("/html/body/div[2]/div[2]/div[3]/div[3]/div[4]/div/div[2]/text()")
        sstato = page.xpath("/html/body/div[2]/div[2]/div[3]/h4[2]/text()")

        if select == "2" and scomitato:
            for i in range(38):
                if scomitato[0] == comsicilia[i]:
                    printy("SUCCESS SICILY | " + str(startid) + " " + snamec[0], "n")
                    if sstato[2].strip() == "Annullato" or sstato[2].strip() == "Terminato" or sstato[3].strip() == "Annullato" or sstato[3].strip() == "Terminato":
                        f = open("Courses/Sicily/inactive_courses.txt", "a")
                        f.write("ID: " + str(startid) + " | Title: " + snamec[0] + " | Start: " + sstart[0] + " | End: " + send[0] + "\n")
                        f.close()
                    elif sstato[2].strip() == "In preparazione" or sstato[3].strip() == "In preparazione":
                        f = open("Courses/Sicily/active_courses.txt", "a")
                        f.write("ID: " + str(startid) + " | Title: " + snamec[0] + " | Start: " + sstart[0] + " | End: " + send[0] + "\n")
                        f.close()
                    elif sstato[2].strip() == "Attivo" or sstato[3].strip() == "Attivo":
                        f = open("Courses/Sicily/active_courses.txt", "a")
                        f.write("ID: " + str(startid) + " | Title: " + snamec[0] + " | Start: " + sstart[0] + " | End: " + send[0] + "\n")
                        f.close()
                    else:
                        printy("ERROR - " + str(startid) + " - Open issue on github!", "r")

                    break
        elif scomitato:
            printy("SUCCESS | " + str(startid) + " " + snamec[0], "n")
            if sstato[2].strip() == "Annullato" or sstato[2].strip() == "Terminato" or sstato[3].strip() == "Annullato" or sstato[3].strip() == "Terminato":
                f = open("Courses/Italy/inactive_courses.txt", "a")
                f.write("ID: " + str(startid) + " | Title: " + snamec[0] + " | Start: " + sstart[0] + " | End: " + send[0] + "\n")
                f.close()
            elif sstato[2].strip() == "In preparazione" or sstato[3].strip() == "In preparazione":
                f = open("Courses/Italy/active_courses.txt", "a")
                f.write("ID: " + str(startid) + " | Title: " + snamec[0] + " | Start: " + sstart[0] + " | End: " + send[0] + "\n")
                f.close()
            elif sstato[2].strip() == "Attivo" or sstato[3].strip() == "Attivo":
                f = open("Courses/Italy/active_courses.txt", "a")
                f.write("ID: " + str(startid) + " | Title: " + snamec[0] + " | Start: " + sstart[0] + " | End: " + send[0] + "\n")
                f.close()
            else:
                printy("ERROR - " + str(startid) + " - Open issue on github!", "r")
        else:
            printy("ERROR - " + str(startid) + " - Accesso Negato!", "r")

        config['COURSES'] = {'lastfinalid': startid}
        config.write(open('config.ini', 'w'))
        startid = int(startid) + 1


if __name__ == "__main__":
    try:
        crsi()
    except KeyboardInterrupt:
        exit()
