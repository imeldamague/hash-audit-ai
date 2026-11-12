# Hash-Audit AI

**Système d'intelligence artificielle multi-agents pour l'audit de sécurité des mécanismes de hachage et de stockage des mots de passe.**

## Présentation

Hash-Audit AI est un projet de cybersécurité et d'IA agentique conçu pour analyser les pratiques de stockage des mots de passe, détecter des mécanismes de hachage faibles et proposer des recommandations de sécurisation.

## Fonctionnalités

- Jeu de données synthétique de 1 000 comptes.
- Analyse de MD5, SHA-256 salé et Argon2id.
- Architecture composée de six agents spécialisés et d'un orchestrateur.
- Audit de 25 fichiers Python synthétiques.
- Simulation d'attaque par dictionnaire.
- Comparaison d'Argon2id, scrypt, bcrypt et PBKDF2-SHA256.
- Gestion du pepper.
- Vérification facultative des mots de passe compromis avec Pwned Passwords et le mécanisme k-anonymity.
- Simulation statistique d'une migration sur 90 jours.

## Installation

**Prérequis :** Python 3.11 ou version supérieure.

```bash
python -m pip install -e ".[dev]"
