#!/usr/bin/env python
# coding: utf-8

"""
Created on Mon May 29 13:35:57 2017
Edited on Thu Aug 31 10:01:23 2017

edit by Bertrand Guillaume

@Bar Yokhai c'est du bon travail
"""

# Entete type
__author__ = "Bar Yokhai"
__copyright__ = "NA"
__credits__ = ["Bar Yokhai", "Bertrand Guillaume"]
# Je suppose..
__license__ = "CC-BY-SA"
__version__ = "0.1"
__maintainer__ = "NA"
__email__ = "guillaume.bertrandpr@yahoo.fr"
__status__ = "NA"

#Programme en Python 2
# Ce script provient a la base de
# https://lilbigdataboy.wordpress.com/2017/05/28/surveiller-le-cours-du-bitcoin-avec-python/

# Il a ete modifie et commente dans le cadre d'un cours sur le Bitcoin (BERTRAND Guillaume)
# Les explications sont trivialisees dans le but de faciliter la comprehension.

# Le python est un language peu verbeux ==> pas de parentheses ou d'accolades inutiles
# Vous devez pretez une attention PARTIEiculiere a l'indentation qui peut causer des erreurs lors de l'execution du script

# PARTIE 0 * PARTIE 0 * PARTIE 0 * PARTIE 0 * PARTIE 0 * PARTIE 0 * PARTIE 0 * PARTIE 0 *

### Import de la configuration du stockage ###
from storageconf import *

### Utilisation d'un ensemble d'outils que l'on a developpe ###
from helpers import *

### Import des librairies ###

# Permet de faciliter l'emploi du json ==> encoder / decoder dans ce format
import json

# Utilisation du temps
import datetime

# Interaction avec le systeme d'exploitation
import os

# Pour l'enregistrement d'objet sur des fichiers = serialisation
#import cPickle as pickle
import _pickle as pickle

# Permet de creer des iterateurs ==> facilite le parcours de listes ou strucutres objets etc..
from itertools import compress


### * * * * * * * * * * * * * * * * * Parametres * * * * * * * * * * * * * * * * * ###
# Taux de variation du cours ici 0.10 = 10% = 10/100
#param_delta = 0.01
#Pour des raison de test - le cours varie peux
# A quel niveau de variation veut-on prevenir par l'envoi d'un mail
param_delta = 0.1

#Duree minimale entre deux mails
#2H!
#param_window_period = 7200
param_window_period=5

#Decalage horaire de ou l'on se situe
#2H soit UTC+2:00
param_utc_delay = 2 * 3600

# Date courante
today_date = datetime.datetime.now()

bitcoinRateStatus=""

### PARTIE 1 * PARTIE 1 * PARTIE 1 * PARTIE 1 * PARTIE 1 * PARTIE 1 * PARTIE 1 * PARTIE 1 * ###
# Renseigne les variables last_date et stored_values_list
# Obtenir tout les fichiers terminant par pkl dans le dossier FOLDER_NAME
files_list_complete = [os.path.join(FOLDER_NAME, f) for f in os.listdir(FOLDER_NAME) if f.endswith('.pkl')]
is_file = bool(files_list_complete)

# Si pas de fichiers
if not is_file:
    # On initialise la date
    last_date = datetime.datetime(2009, 1, 1)

    # On creer une "liste"
    stored_values_list = []

# Si il y'a des fichiers
if is_file:
    # Chemin du fichier le plus recent = nom du dossier de stockage + nom de fichier
    most_recent_file = FOLDER_NAME + PICKLE_LAST_DATE_NAME

    # Chemin du fichier ou sont stockees les valeurs = nom du dossier de stockage + nom du fichier
    stored_values_file = FOLDER_NAME + PICKLE_STORED_VALUES_NAME

    if most_recent_file in files_list_complete:
        # Mise a jour de la derniere date
        # On recupere le contenu du fichier le plus recent = on deserialise
        # rb --> r b ; r = read ; b = utile pour les OS ne traitant pas les fichiers textes differament
        # open ==> on ouvre le fichier
        # pickle.load on utilise la fonction load qui est dans pickle ==> Ainsi on charge la date qui est dans le fichier dans la variable
        last_date = pickle.load(open(most_recent_file, "rb"))
    else:
        # Donc, Si pas de fichiers recents
        last_date = datetime.datetime(2009, 1, 1)
        print((NO_MESSAGE_SEND))

    if stored_values_file in files_list_complete:
        # On charge les donnees qui sont dans le fichier dans la variable sous forme d'une liste
        stored_values_list = pickle.load(open(stored_values_file, "rb"))
    else:
        print((VERIFY_PICKLE_NAME))

# PARTIE 2 * PARTIE 2 * PARTIE 2 * PARTIE 2 * PARTIE 2 * PARTIE 2 * PARTIE 2 * PARTIE 2 *
# Si on a une valeur plus petite que <param_window_period> secondes
# On ne renvoie pas un mail pour eviter d'etre considere comme spammeur
if int((today_date - last_date).total_seconds()) < param_window_period:
    print((MAIL_ALREADY_SEND + last_date.strftime('%c')))

# Si on a une valeur plus grande que <param_window_period> secondes
# Alors on peut envoyer un mail
if int((today_date - last_date).total_seconds()) >= param_window_period:

    # Parfois le process de connexion au serveur est laborieux, on peut donc s'y reprendre a plusieurs fois
    # ATTENTION on boucle sur get
    ok = False
    while ok is not True:
        # Requeter l'API
        result = getApiData()
        the_page = result[0]
        ok = result[1]


    # Retrieving date and bitcoin price
    data = json.loads(the_page)
    bitcoin_price = data['bpi']['EUR']['rate_float']
    bitcoin_time = data['time']['updated']
    bitcoin_time = datetime.datetime.strptime(bitcoin_time, "%b %d, %Y %H:%M:%S %Z")
    bitcoin_time = bitcoin_time + datetime.timedelta(0, param_utc_delay)

    # Store the new price into the list
    stored_values_list.append((bitcoin_time, bitcoin_price))

    # Determiner une chute ou une hausse des cours
    time_list = [s[0] for s in stored_values_list]
    value_list = [s[1] for s in stored_values_list]
    index_max = value_list.index(max(value_list))

    # Variation en valeur
    biggest_delta_raw = round(max(value_list) - value_list[-1], 5)

    # Variation en pourcentage
    biggest_delta_pct=round(biggest_delta_raw / max(value_list), 6)

    # Modifie le message du bitcoin suivant la hausse ou la baisse
    bitcoinRateStatus = determineIncreaseOrDecreaseRate(biggest_delta_pct)

    # Permet de prendre on compte aussi la hausse du cours
    biggest_delta_pct = abs(biggest_delta_pct)

    # Date pour la valeur maximale
    biggest_date_max = time_list[index_max].strftime('%c')

    # Mettre les valeur dans un objet..
    res = (biggest_delta_raw, biggest_delta_pct, biggest_date_max)

    # Enlever les prix anciens de bitcoin
    recent_dates_list = [int((time_list[-1] - d).total_seconds()) <= param_window_period for d in time_list]
    stored_values_list = list(compress(stored_values_list, recent_dates_list))
    # w ==> Ecriture de la date courant dans le fichier PICKLE_STORED_VALUES_NAME
    pickle.dump(stored_values_list, open(FOLDER_NAME + PICKLE_STORED_VALUES_NAME, "wb"))

    displayVariationRate(biggest_delta_pct)

    # PARTIE 3 * PARTIE 3 * PARTIE 3 * PARTIE 3 * PARTIE 3 * PARTIE 3 * PARTIE 3 * PARTIE 3 *
    # S'il y a une grosse baisse on une grosse montee

    # Pour la hausse il suffit de mettre une valeur absolue
    if biggest_delta_pct > param_delta:

        # Envoi du mail de notification
        sendMail(bitcoin_price, res, bitcoinRateStatus)

        # Enregistrer la date
        pickle.dump(today_date, open(FOLDER_NAME + PICKLE_LAST_DATE_NAME, "wb"))
    else:
        print((NO_MESSAGE_SEND))




