import os
import sys
import shutil
import tempfile
import zipfile
import subprocess
from urllib.parse import urlparse

def download_and_extract_zip(url, dest_dir):
    zip_path = os.path.join(dest_dir, os.path.basename(url))
    try:
        subprocess.run(['wget', '-q', url, '-O', zip_path], check=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        os.remove(zip_path)
        print(f"Dézippage du fichier: {os.path.basename(url)}")
    except subprocess.CalledProcessError:
        print(f"Erreur de téléchargement pour {url}")

def clone_git_repo(url, dest_dir):
    try:
        subprocess.run(['git', 'clone', url, dest_dir], check=True)
        print(f"Clonage du dépôt Git: {url}")
    except subprocess.CalledProcessError:
        print(f"Erreur de clonage pour {url}")

def main(urls_file):
    if not os.path.isfile(urls_file):
        print("Veuillez spécifier le fichier contenant les URLs.")
        sys.exit(1)

    temp_dir = tempfile.mkdtemp()
    all_yara_rules_dir = os.path.join(temp_dir, 'all_yara_rules')
    os.makedirs(all_yara_rules_dir, exist_ok=True)

    with open(urls_file, 'r') as file:
        for url in file:
            url = url.strip()
            if url:
                if url.endswith('.zip'):
                    print(f"Téléchargement du fichier ZIP: {url}")
                    download_and_extract_zip(url, temp_dir)
                else:
                    repo_dir = os.path.join(temp_dir, os.path.basename(urlparse(url).path))
                    clone_git_repo(url, repo_dir)

    print("Recherche des fichiers .yara, .yar, .rules, .rule dans le répertoire temporaire...")
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(('.yara', '.yar', '.rules', '.rule')):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(all_yara_rules_dir, file)
                if src_file != dest_file:
                    shutil.copy(src_file, dest_file)

    if os.listdir(all_yara_rules_dir):
        print("Tous les fichiers YARA, YAR, RULES, RULE ont été copiés dans le répertoire 'all_yara_rules'.")
    else:
        print("Aucun fichier YARA, YAR, RULES, RULE trouvé à copier.")

    archive_path = os.path.join(os.getcwd(), 'archive_yara.zip')
    shutil.make_archive(archive_path.replace('.zip', ''), 'zip', all_yara_rules_dir)
    if os.path.isfile(archive_path):
        print(f"L'archive '{archive_path}' a été créée avec succès.")
    else:
        print("Erreur lors de la création de l'archive.")

    shutil.rmtree(temp_dir)
    print("Nettoyage terminé.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_yara.py <urls_file>")
        sys.exit(1)
    main(sys.argv[1])
