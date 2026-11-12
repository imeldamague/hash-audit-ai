

# Installation



## Prérequis



Avant de commencer, installer :



- Python 3.11 ou une version supérieure.

- Git.

- PowerShell sous Windows ou un terminal sous Linux.



## 1. Récupérer le projet



```bash

git clone https://github.com/imeldamague/hash-audit-ai.git

cd hash-audit-ai

```



## 2. Créer un environnement virtuel



Sous Windows PowerShell :



```powershell

python -m venv .venv

.venv\\Scripts\\Activate.ps1

```



Sous Linux :



```bash

python3 -m venv .venv

source .venv/bin/activate

```



## 3. Installer les dépendances



```bash

python -m pip install --upgrade pip

pip install -e ".[dev]"

```



## 4. Vérifier l'installation



```bash

python -m pytest

```



Les tests permettent de vérifier le bon fonctionnement des composants du projet.



## 5. Lancer une première analyse



```bash

python -m hash_audit.cli audit app/demo.py

```



Cette commande lance un audit sur le fichier de démonstration fourni avec le projet.



## Ressources



- [Dépôt GitHub](https://github.com/imeldamague/hash-audit-ai)

- [Documentation Python](https://docs.python.org/3/)

- [Documentation Argon2](https://argon2-cffi.readthedocs.io/)



---



[Retour à l'accueil](index.md)



