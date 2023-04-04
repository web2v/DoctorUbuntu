import os
import subprocess
import virtualenv

current_directory = os.path.abspath(os.path.dirname(__file__))
venv_dir = os.path.join(current_directory, 'doc4')

# Vérifier si le répertoire de l'environnement virtuel existe déjà
if not os.path.isdir(venv_dir):
    # Créer l'environnement virtuel si le répertoire n'existe pas
    virtualenv.cli_run([venv_dir])
    subprocess.run(['chmod', '-R', '755', venv_dir])
    subprocess.run([os.path.join(venv_dir, 'bin', 'python'), '-m', 'pip', 'install', 'openai'])
    subprocess.run([os.path.join(venv_dir, 'bin', 'python'), '-m', 'pip', 'install', 'prompt_toolkit'])
    subprocess.run([os.path.join(venv_dir, 'bin', 'python'), '-m', 'pip', 'install', 'prompt_toolkit', 'readline'])

activate_script = os.path.join(venv_dir, 'bin/activate_this.py')
