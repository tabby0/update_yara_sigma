import os
import sys
import shutil
import tempfile
import subprocess

def main(url_file):
    if not os.path.isfile(url_file):
        print(f"Le fichier {url_file} n'existe pas.")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as temp_dir:
        all_sigma_rules_dir = os.path.join(temp_dir, 'all_sigma_rules')
        os.makedirs(all_sigma_rules_dir, exist_ok=True)

        with open(url_file, 'r') as file:
            for url in file:
                url = url.strip()
                if not url or url.startswith('#'):
                    continue

                print(f"Clonage de l'URL : {url}")
                subprocess.run(['git', 'clone', url], cwd=temp_dir)

        print("Recherche des fichiers .yml et copie dans le répertoire all_sigma_rules/")
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.yml'):
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(all_sigma_rules_dir, file)
                    if src_file != dst_file:
                        shutil.copy(src_file, dst_file)

        print("Compression du répertoire all_sigma_rules/")
        shutil.make_archive('all_sigma_rules', 'zip', all_sigma_rules_dir)

    print("Opération terminée.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <fichier_urls>")
        sys.exit(1)

    main(sys.argv[1])
