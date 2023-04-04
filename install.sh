#!/bin/bash

# Changer le répertoire courant pour le répertoire d'installation
script_dir="$(dirname "$(readlink -f "$0")")"

env_path="$PATH"
if ! echo "$env_path" | grep -q "$script_dir"; then
    export PATH="$env_path:$script_dir"
    echo "The directory $script_dir has been added to the PATH environment variable."
else
    echo "The directory $script_dir is already in the PATH environment variable."
fi

shell="$SHELL"
rc_file=

if echo "$shell" | grep -q "bash"; then
    rc_file="$HOME/.bashrc"
elif echo "$shell" | grep -q "zsh"; then
    rc_file="$HOME/.zshrc"
else
    echo "Unknown shell $shell, alias not set."
    exit 0
fi

# Demander le nom à donner pour 'doc'
read -p "Entrez le nom à donner pour appler votre  'DoctorUbuntu': " user_doc_name

# Vérifier si le fichier existe
if [ -e /usr/local/bin/"$user_doc_name" ]; then
    echo "Le fichier /usr/local/bin/$user_doc_name existe déjà."
    
    # Demander la confirmation pour écraser le fichier
    while true; do
        read -p "Voulez-vous écraser le fichier existant ? (Oui/Non) " yn
        case $yn in
            [Oo]* ) 
                sudo rm /usr/local/bin/"$user_doc_name"
                echo "Le fichier /usr/local/bin/$user_doc_name a été supprimé."
                break
                ;;
            [Nn]* ) 
                echo "Le fichier n'a pas été écrasé. Veuillez choisir un autre nom."
                exit 0
                ;;
            * ) echo "Veuillez répondre Oui ou Non.";;
        esac
    done
fi
# Créer le fichier avec le nom choisi dans /usr/local/bin
sudo sh -c "echo '#!/bin/bash' > /usr/local/bin/$user_doc_name"
sudo sh -c "echo '' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo 'get_current_directory() {' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo '  # Récupérer le chemin absolu du répertoire courant' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo '  current_directory=\"\$(pwd)\"' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo '  echo \"\$current_directory\"' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo '}' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo '' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo 'current_directory=\$(get_current_directory)' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo '' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo 'echo \"Le répertoire courant est : \$current_directory\"' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo 'sleep 2' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo 'python3 \"$PWD/docubun5.py\" \"\$current_directory\"' >> /usr/local/bin/$user_doc_name"
sudo sh -c "echo 'exit 0' >> /usr/local/bin/$user_doc_name"

# Changer le propriétaire du fichier
sudo chown $USER:$USER /usr/local/bin/"$user_doc_name"

# Donner les permissions d'exécution au fichier
chmod +x /usr/local/bin/"$user_doc_name"

echo "Le script DoctorUbuntu a été ajouté à /usr/local/bin sous le nom de '$user_doc_name'."

# Rétablir le répertoire de travail d'origine
cd "$OLDPWD"

echo "Entrez votre clée API :"
read clee_api
echo $clee_api >> .api



sleep 2
# Exécuter l'installation avec sudo
sudo pip3 install virtualenv
python3 install.py
wait
