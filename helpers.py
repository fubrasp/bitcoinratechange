#!/usr/bin/env python
# coding: utf-8

### Import des constantes ###
from constantes import *

### Import de la configuration du mail emmeteur ###
from mailconf import *

# Envoi de mail (cf. smtp)
import smtplib

# Pour la notion de mail en elle-meme (Objet encapsulant tout : emetteur, recepteur, contenu, ..)
from email.mime.multipart import MIMEMultipart

# Pour le message du mail
from email.mime.text import MIMEText

# Permet d'interagir avec des adresses comme www.google.com
from urllib.request import urlopen
from urllib.request import Request

import ssl

# Deconseille simple - https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
ssl._create_default_https_context = ssl._create_unverified_context


def sendMail(bitcoin_price, res, bitcoinRateStatus):
    # Definition des acteurs
    fromaddr = EXPEDITEUR
    toaddr = DESTINATAIRE

    # Utilisation de l'objet pour modeliser le mail
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = SUBJECT + bitcoinRateStatus + "!!!"
    body = BODY_MESSAGE + bitcoinRateStatus + ":" + str(
        bitcoin_price) + " EUR, soit " + str(res[1] * 100) + "% le " + str(
        res[2])
    msg.attach(MIMEText(body, 'plain'))

    # Connexion au serveur via SMTP au port 587
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    # Utilisation de starttls ==> prendre une connexion non chiffre et la mettre a jour vers une connexion chiffree
    server.starttls()

    # Authentification sur le seveur ==> comme quand on se connecte
    server.login(fromaddr, MY_PASSWORD)
    text = msg.as_string()

    # Envoi du mail
    server.sendmail(fromaddr, toaddr, text)
    print((MESSAGE_SEND))
    server.quit()

def getApiData():
    try:
        # On obtient l'information d'une api
        # ==> il ne faut pas s'amuser a requeter comme un fou sinon il vous bloque votre ip
        # Et par consequent il n'est plus possible d'utiliser cette source de donnees
        url = API_PATH
        # GET sur l'URL donnee
        request = Request(url)
        response = urlopen(request)

        # Affichage de la reponse
        the_page = response.read()

        ok = True
    except Exception as e:
        print((e))
        print((API_ERROR))
        the_page=""
        ok = False

    return [the_page, ok]

def determineIncreaseOrDecreaseRate(biggest_delta_pct):
    if biggest_delta_pct < 0:
        bitcoinRateStatus = "baisse"
    else:
        bitcoinRateStatus = "hausse"
    return bitcoinRateStatus

def displayVariationRate(biggest_delta_pct):
    print((BITCOIN_VARIATION))
    print((biggest_delta_pct))