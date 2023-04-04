#!/usr/bin/env python3
import readline #gestion du prompt utilisateur dans python


import openai
import os
import subprocess
from prompt_toolkit import prompt

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import time
import re
import shlex
import signal
import sys

#parametre passé du repertoire courant du shell 
current_working_directory = sys.argv[1]
print(current_working_directory)



# Récupérer le répertoire parent de docubun5.py
parent_directory = os.path.dirname(os.path.abspath(__file__))

def load_api():
    # Concaténer le nom du fichier .api avec le chemin du répertoire parent
    api_file_path = os.path.join(parent_directory, '.api')

    # Ouvrir le fichier .api
    with open(api_file_path, "r") as f:
        keyapi = f.read().strip()

        return keyapi
    
openai.api_key = load_api()

def printfx(message):
    for c in message:
        #print(c, end='', flush=True)
        #print(c,end='') #no flush in tkinter
        print("\033[31m" + c+ "\033[0m" ,end='',flush=True) #green
        time.sleep(0.01)
        #            print("\033[32m  humhum... \033[0m\n")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')        

clear_console()

#########################################
##########   GTP  #######################

## analyse des mots 

def find_words(text, words):
    for word in words:
        if word in text:
            return True
    return False

#######################################
###############interaction API GPT 

INIT = 0
promptinit = ""
promptuser = ""


#dans cette version de DoctorUbuntu le chargemnt de prompt exterieur n est pas activé
#les prompts sont initialisés dans la declaration chat_gpt(prompt) et comment_on_command(command)
def INIT_prompt():
    global promptinit, promptuser
    ## chatgement prompt initial contexte
    if not os.path.exists( parent_directory + "/prompt.txt"):
        printfx("<<<<<<<<PAS DE PROMPT>>>>>>>>>>")
        with open(parent_directory + "/prompt.txt", "w") as f:
            f.write("")

    with open(parent_directory + "/prompt.txt", "r") as f:
        promptinit = f.read()

    ##chargt prompt des demande user
    if not os.path.exists(parent_directory + "/promptbashCommandes.txt"):
        printfx("<<<<<<<<PAS DE PROMPT 2 >>>>>>>>>>")
        with open(parent_directory + "/promptbashCommandes.txt", "w") as f:
            f.write("")
    with open(parent_directory + "/promptbashCommandes.txt", "r") as f:
        promptuser = f.read()
    
    # Remplacer les retours à la ligne par "\n"
    promptinit = promptinit.replace("\\n", "\n")
    promptuser = promptuser.replace("\\n", "\n")

    return promptinit, promptuser

INIT_prompt()





def chat_gpt(prompt):
    #mise en route 
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt= "oublies toute instruction précédente. maintenant, Sous ubuntu 22 LTS gnome-shell version 42.5 , je suis dans le dossier courant où je veux executer la commande,  Donnez-moi la commande pour " + prompt + " ?  repond en formatant ta reponse comme cela :  pas de commentaires, ne met surtout pas de balise, seulement au format texte , extrait seulement la commande, s il y a plusieurs commandes ajoutes les dans le script .  merci.", #prompt-bashCommandes.txt
            max_tokens=150,  # Ajustez le nombre de tokens pour limiter la longueur de la réponse
            n=1,
            stop=None,
            temperature=0.3,  # Diminuez la température pour rendre la réponse plus déterministe
        )          
        if response.choices[0].text.strip() in ["This content may violate our content policy","","''" ]:
            printfx("warning lisez la content policy ")
            return response.choices[0].text.strip()
        else:
             
            
            return response.choices[0].text.strip()
    except openai.error.OpenAIError as error:
        printfx("OpenAI API Error: "+ str(error))
        return None

#tableau de valeur pour securiser les commandes proposées au moment de l execution
valid_bash_commands = [
    ".", ":", "[[", "alias", "bg", "bind", "break", "builtin", "case", "cd", "command",
    "compgen", "complete", "continue", "declare", "dirs", "disown", "echo", "enable",
    "eval", "exec", "exit", "export", "false", "fc", "fg", "getopts", "hash", "help",
    "history", "if", "jobs", "kill", "let", "local", "logout", "mapfile", "popd",
    "printf", "pushd", "pwd", "read", "readonly", "return", "set", "shift", "shopt",
    "source", "suspend", "test", "time", "times", "trap", "true", "type", "typeset",
    "ulimit", "umask", "unalias", "unbound", "unicode_start", "unicode_stop", "unfunction",
    "unhash", "unlimit", "unset", "until", "wait", "while",
    "mkdir", "rm", "touch", "chown", "chmod", "grep", "sed", "awk", "find",
    "ps", "killall", "ls", "cat", "less", "more", "head", "tail", "cp", "mv", "tar",
    "gzip", "gunzip", "ssh", "scp", "rsync", "curl", "wget", "ping", "ifconfig",
    "route", "traceroute", "netstat", "lsof", "top", "df", "du", "free", "iostat",
    "vmstat", "sar", "awk", "sort", "uniq", "cut", "paste", "awk", "join", "diff",
    "patch", "tar", "gzip", "bzip2", "zip", "unzip", "dd", "parted", "mount", "umount",
    "mkfs", "fsck", "chroot", "ldconfig", "strace", "ltrace", "valgrind", "gdb",
    "make", "gcc", "g++", "perl", "python", "ruby", "php", "java", "scala", "hadoop",
    "hive", "pig", "spark", "hbase", "mongodb", "redis", "nginx", "apache", "tomcat",
    "mysql", "postgresql", "sqlite", "oracle", "ldap", "git", "svn",
    "||", "&&", "|", "&","wget","snap","synaptic","nautilus"
]

appautorisée = [
    "firefox",
    "google-chrome",
    "chromium",
    "opera",
    "nautilus",
    "gedit",
    "atom",
    "subl",
    "code",
    "pycharm",
    "gimp",
    "inkscape",
    "vlc",
    "totem",
    "mpv",
    "thunderbird",
    "evolution",
    "discord",
    "slack",
    "zoom",
    "teams",
    "skype",
    "whatsapp",
    "telegram",
    "signal",
    "slack",
    "microsoft-edge",
    "brave",
    "tor-browser",
    "wireshark",
    "virtualbox",
    "docker",
    "git",
    "ssh",
    "ping",
    "traceroute",
    "wget",
    "curl",
    "scp",
    "rsync",
    "sshfs",
    "netcat",
    "nmap",
    "tcpdump",
    "aircrack-ng",
    "john",
    "hashcat",
    "hydra",
    "sqlmap",
    "metasploit",
    "bettercap",
    "apt",
    "dpkg",
    "systemctl",
    "journalctl",
    "lsblk",
    "mount",
    "umount",
    "df",
    "du",
    "ps",
    "top",
    "htop",
    "ifconfig",
    "ip",
    "route",
    "netstat",
    "lsof",
    "ss",
    "iptables",
    "ufw",
    "chown",
    "chmod",
    "chgrp",
    "useradd",
    "userdel",
    "usermod",
    "groupadd",
    "groupdel",
    "groupmod",
    "passwd",
    "adduser",
    "deluser",
    "moduser",
    "addgroup",
    "delgroup",
    "modgroup",
    "visudo",
    "crontab",
    "at",
    "systemd-analyze",
    "systemd-cgls",
    "systemd-cat",
    "systemd-delta",
    "systemd-detect-virt",
    "systemd-escape",
    "systemd-hwdb",
    "systemd-id128",
    "systemd-inhibit",
    "systemd-mount",
    "systemd-notify",
    "systemd-nspawn",
    "systemd-path",
    "systemd-resolve",
    "systemd-run",
    "systemd-socket-activate",
    "systemd-stdio-bridge",
    "systemd-tmpfiles",
    "systemd-tty-ask-password-agent",
    "systemd-umount",
]


def est_commande_bash_valide_et_secure(gptmessage):
    """Analyse les lignes de réponse en tant que commandes Bash et les filtre en conséquence"""
    lines = gptmessage.split('\n')
    valid_lines = []
    for line in lines:
        try:
            # Analyse la ligne en tant que commande Bash
            tokens = shlex.split(line)
            if len(tokens) > 0 or tokens[0] in valid_bash_commands or tokens[0] in appautorisée:
                # La ligne est une commande Bash valide
                valid_lines.append(line)                
            else:
                time.sleep(0.1)
                # La ligne n'est pas une commande Bash valide
                #print(f"La ligne suivante n'est pas une commande Bash valide : {line}")
        except Exception as e:
            time.sleep(0.1)
            # La ligne n'est pas une commande Bash valide
            #print(f"La ligne suivante n'est pas une commande Bash valide : {line}")
    # Renvoie les lignes de réponse valides sous forme de chaîne de caractères
    return '\n'.join(valid_lines)


def WriteReponse(prompt):
    # Exemple d'utilisation de la fonction process_gpt_response
    response1 = chat_gpt(prompt)

    filtered_response = est_commande_bash_valide_et_secure(response1)
    #print(f"Réponse filtrée : {filtered_response}")
    prescriptions_file_path = parent_directory + "/Doctor-prescription.txt"

    
    # Écriture de la commande dans un fichier texte séparé si elle est valide
    with open(prescriptions_file_path, "a") as commandes_file:
        commandes_file.write(filtered_response + "\n")
    return filtered_response

            
#retour explicatif de la commande proposée au premier appel de gpt on fait donc un deuxieme appel à gpt
def comment_on_command(command):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Expliques moi et commentez en français précisement la commande suivante : " + command,
        max_tokens=180,
        n=1,
        stop=None,
        temperature=0.4,
    )
    #printfx("..?whois ")
    return response.choices[0].text.strip()


# Récupérer le répertoire courant passé en argument
if len(sys.argv) > 1:
    current_working_directory = sys.argv[1]
else:
    current_working_directory = os.getcwd()


#on va executer un script localement 
def execute_script(script):
    print("\033[33m >>scriptsending...\n \033[0m")
    current_working_directory = os.environ.get("PWD")
    print("dossier courant : "+ current_working_directory)
    temp_script_path = os.path.join(current_working_directory, "temp_script.sh")

    with open(temp_script_path, "w") as script_file:
        script_file.write("#!/bin/bash\n")
        script_file.write("cd {}\n".format(current_working_directory))
        script_file.write(script)

    prescriptions_file_path = parent_directory + "/Doctor-prescription.txt"
    os.chmod(temp_script_path, 0o755)

    # Définir un gestionnaire de signaux pour intercepter SIGINT et SIGTERM
    def signal_handler(sig, frame):
        print("Signal {} intercepté, attente de la fin de l'exécution du script...".format(sig))
        # Rétablir les gestionnaires de signal par défaut pour SIGTERM et SIGINT
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Utilisation de subprocess pour exécuter dans le même terminal
    subprocess.run(["./temp_script.sh"], cwd=current_working_directory)

    # Écriture de la commande dans un fichier texte séparé car elle est exécutée
    with open(prescriptions_file_path, "a") as commandes_file:
        commandes_file.write(script + "\n")

    os.remove(temp_script_path)
    printfx("\n Les commandes ont été exécutées avec succès. ")
    time.sleep(3)

##################################################################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#################################################################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#######################   MAIN   APPLICATION INTERFAce
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#from prompt_toolkit import prompt


#on veut donner une valeur par default qui est la commande a éditer si l user le souhaite
def readlinecommande(command):
    commandedit = prompt(' ->: ', default=command)
    print("\033[32m" + commandedit + "\033[0m\n")
    return commandedit

######################################################
###################################################
###################"" M  A  I  N """""""">>>>>>>>>>>>>>>>>>>>>>
if __name__ == "__main__":
    width = os.get_terminal_size().columns
    printfx("_"*width)

    print("Bienvenue dans l'assistant : ") 
    printfx("ChatGPT CLI DocteurUbuntu ! V8 \n")
    session = PromptSession(history=InMemoryHistory(), auto_suggest=AutoSuggestFromHistory())
    ####flag hitory dans fichier
    aff=False
    while True:
        printfx("\n Entrez votre demande : 'qq' pour quitter  \n")
        user_input = session.prompt(".... : \n")
        if user_input.lower() in ["quit", "exit", "qq"]:
            printfx("Au revoir! \n ")
            break

        
            ##fisrt AI call
            ################################################################AI CALL
        command = WriteReponse(user_input)
        printfx("...doctor say : ")
        if command is not None:
            print("\033[32m  humhum... \033[0m\n")
        else:
            command = "?"
        
        motinterdits = "sudo"
        if motinterdits in command:
            printfx("\n La commande proposée peu présenter un risque mais la voici: \n")
            #print("\033[31m" + command + "\033[0m\n")
            safe_command = False            
        else:

            printfx("Commande safe proposée : \n")
            safe_command = True
            #printfx("doc is ready! \n ")
            
        print("\033[32m" + command + "\033[0m\n")
        ##################################################################
        ########################################## 2ieme aPPEL IA comment
        comment = comment_on_command(command)
        printfx("Explication: ")
        print(comment)
        ################### explication affichée
        ### traitement des instructions utilisateur 
        aff= False # variable de non repetition d affichage d infos redondantes, en fin de def
        if safe_command == False :
            print("\033[33m Force doctor to valid? O/n: \033[0m")
            securAsk = input("-> ")
            if securAsk.lower() in ["oui","o","y","yep"]:
                secur = True
                print("\033[31m êtes-vous sûr ? O/n :  \033[0m ")
                confirm = input("-> ")
            else:
                if securAsk.lower() in ["quit", "exit", "qq"]:
                    printfx("Au revoir! \n ")
                    break 
                secur = False
                confirm = "n"          
        else:
            secur = True
            printfx("\n Voulez-vous exécuter les commandes suggérées ? \n (e)diter, (Oui/Non) : \n")        
            print("\033[32m" + command + "\033[0m\n")
            confirm = input() # input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> INPUT 2
        ## edition ou execution ou annulation ou quit 
        if confirm.lower() in ["qq","quit","exit"]:#>>>>>>>>>>>>>>>>>> quit
            printfx("Au revoir! \n ")
            break
        if confirm.lower() in ["oui", "o"] and secur:
            execute_script(command) #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #printfx("\n Les commandes ont été exécutées avec succès. ")
        #######    edition commande    #####
        if confirm.lower() in ["e"] and secur:#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EDITION DEMANDEE
            printfx("\nCommande en cours d'édition: \n")
            
            # Remplacer la commande par la saisie de l'utilisateur
            command = readlinecommande(command)
            #print("command filtrée" + command)
            # Proposer de vérifier la commande
            comment = comment_on_command(command)
            print(comment)            
            printfx("\n Voulez-vous exécuter cette commande éditée ? (Oui/Non) : ")
            confirm_edit = input()
            if confirm_edit.lower() in ["oui", "o"]:
                execute_script(command)#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #printfx("\n Les commandes ont été exécutées avec succès. ")            
           
        if confirm.lower() not in ["oui", "o"]:#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AUCUNES COMMANDES EXECUTEES
            printfx("\n ---->> Les commandes n'ont pas été exécutées.")
            


