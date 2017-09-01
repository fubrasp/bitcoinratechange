#!/usr/bin/env python
# coding: utf-8

# Messages utilisateur
MESSAGE_SEND="Message envoye."
NO_MESSAGE_SEND="Aucun message envoye."
VERIFY_PICKLE_NAME="Verifier le nom de pickle_stored_values_name ."
MAIL_ALREADY_SEND="Nous avons deja envoye un mail recamment.\n on evite de spammer."
BITCOIN_VARIATION="VARIATION DERNIERE MINUTE"

MAIL_ERROR="1/ Verifiez votre connexion internet. \n2/ Verifiez que le port 587 n'est pas bloque.\n3/git comm Verifiez que les applications moins securisees sont autorisees par votre fournisseur mail.\n"
API_ERROR="Erreur avec l'API"

# Source de donnees
API_PATH="https://api.coindesk.com/v1/bpi/currentprice.json"

# Mail pour prevenir
SUBJECT="[BITCOIN] - prix du bitcoin a la "
BODY_MESSAGE="Le cours du bitcoin a "