#!/bin/bash

# Supprimer le fichier 'doc' de /usr/local/bin  REMPLACEZ "doc" par le nom que vous avez donné à votre script de lancement
if [[ -f "/usr/local/bin/doc" ]]; then
    sudo rm -f /usr/local/bin/doc
    echo "Le script 'doc' a été supprimé de /usr/local/bin."
else
    echo "Le script 'doc' n'existe pas dans /usr/local/bin."
fi

# Supprimer le répertoire 'doc4' de DoctorUbuntu_V8
if [[ -d "doc4" ]]; then
    sudo rm -rf "doc4"
    echo "Le répertoire 'doc4' a été supprimé de DoctorUbuntu_V8."
else
    echo "Le répertoire 'doc4' n'existe pas dans DoctorUbuntu_V8."
fi
