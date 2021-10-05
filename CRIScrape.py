import os
import configparser
import requests
from lxml import html
from colorama import Fore


def main():
    config = configparser.ConfigParser()
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

    if not os.path.exists("Italia"):
        os.makedirs("Italia")
    if not os.path.exists("Sicilia"):
        os.makedirs("Sicilia")

    print(Fore.CYAN + "CRI Courses Scraper | Coded by Block2Paz")
    print(Fore.LIGHTCYAN_EX + "Website: vcardone.it")
    print(Fore.LIGHTCYAN_EX + "Version: 2.0\n" + Fore.RESET)

    print(Fore.LIGHTGREEN_EX + "--------- SELECT AN OPTION ---------")
    print(Fore.RED + "[1] " + Fore.LIGHTRED_EX + "All Italy Courses")
    print(Fore.RED + "[2] " + Fore.LIGHTRED_EX + "Only Sicily Courses")
    print(Fore.RED + "[0] " + Fore.LIGHTRED_EX + "EXIT" + Fore.RESET)

    while True:
        select = input(Fore.YELLOW + "\n[WAITING] -> ")

        if not os.path.exists('config.ini'):
            print(Fore.RESET + "\nCreating config file..")
            email = input(" » Enter GAIA email: ")
            passwd = input(" » Enter GAIA password: ")
            config['LOGIN'] = {'email': email, 'passwd': passwd}
            config['MAIN'] = {'lastfinalid': '1'}
            config.write(open('config.ini', 'w'))
        else:
            config.read('config.ini')
            email = config['LOGIN']['email']
            passwd = config['LOGIN']['passwd']

        if select == "1" or select == "2":
            lastid = config['MAIN']['lastfinalid']
            startid = input(Fore.RESET + "\nInitial course ID (Last final ID: " + lastid + "): ")
            endid = input("Final course ID: ")

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

            print("\nStarting...\n")

            while int(startid) <= int(endid):
                urlcrse = 'https://gaia.cri.it/aspirante/corso-base/' + str(startid)
                res = client.get(urlcrse, headers=dict(referer=urlgn))
                if res.url == "https://gaia.cri.it/errore/permessi/":
                    print(Fore.RED + "\n[ERROR] Login failed, check your credentials in the config.ini file!" + Fore.RESET)
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
                            print(Fore.GREEN + "[SUCCESS] SICILIA " + str(startid) + " " + snamec[0] + Fore.RESET)
                            if sstato[2].strip() == "Annullato" or sstato[2].strip() == "Terminato" or sstato[3].strip() == "Annullato" or sstato[3].strip() == "Terminato":
                                f = open("Sicilia/corsi_non_attivi.txt", "a")
                                f.write("ID: " + str(startid) + " | Titolo: " + snamec[0] + " | Inizio: " + sstart[0] + " | Fine: " + send[0] + "\n")
                                f.close()
                            elif sstato[2].strip() == "In preparazione" or sstato[3].strip() == "In preparazione":
                                f = open("Sicilia/corsi_attivi.txt", "a")
                                f.write("ID: " + str(startid) + " | Titolo: " + snamec[0] + " | Inizio: " + sstart[0] + " | Fine: " + send[0] + "\n")
                                f.close()
                            elif sstato[2].strip() == "Attivo" or sstato[3].strip() == "Attivo":
                                f = open("Sicilia/corsi_attivi.txt", "a")
                                f.write("ID: " + str(startid) + " | Titolo: " + snamec[0] + " | Inizio: " + sstart[0] + " | Fine: " + send[0] + "\n")
                                f.close()
                            else:
                                print(Fore.RED + "[ERROR] " + str(startid) + " - Open issue on github!" + Fore.RESET)

                            break
                elif scomitato:
                    print(Fore.GREEN + "[SUCCESS] " + str(startid) + " " + snamec[0] + Fore.RESET)
                    if sstato[2].strip() == "Annullato" or sstato[2].strip() == "Terminato" or sstato[3].strip() == "Annullato" or sstato[3].strip() == "Terminato":
                        f = open("Italia/corsi_non_attivi.txt", "a")
                        f.write("ID: " + str(startid) + " | Titolo: " + snamec[0] + " | Inizio: " + sstart[0] + " | Fine: " + send[0] + "\n")
                        f.close()
                    elif sstato[2].strip() == "In preparazione" or sstato[3].strip() == "In preparazione":
                        f = open("Italia/corsi_attivi.txt", "a")
                        f.write("ID: " + str(startid) + " | Titolo: " + snamec[0] + " | Inizio: " + sstart[0] + " | Fine: " + send[0] + "\n")
                        f.close()
                    elif sstato[2].strip() == "Attivo" or sstato[3].strip() == "Attivo":
                        f = open("Italia/corsi_attivi.txt", "a")
                        f.write("ID: " + str(startid) + " | Titolo: " + snamec[0] + " | Inizio: " + sstart[0] + " | Fine: " + send[0] + "\n")
                        f.close()
                    else:
                        print(Fore.RED + "[ERROR] " + str(startid) + " - Open issue on github!" + Fore.RESET)
                else:
                    print(Fore.RED + "[ERROR] " + str(startid) + " - Accesso Negato!" + Fore.RESET)

                config['MAIN'] = {'lastfinalid': startid}
                config.write(open('config.ini', 'w'))

                startid = int(startid) + 1
            break
        elif select == "0":
            exit()
        else:
            print(Fore.RED + "ERROR: Invalid selection!" + Fore.RESET)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
