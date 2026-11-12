# Hash-Audit AI

Projet de cybers?curit? et d'IA agentique pour l'audit des m?canismes de stockage des mots de passe.

## Fonctionnalit?s

- Jeu de donn?es synth?tique de 1 000 comptes.
- Analyse MD5, SHA-256 sal? et Argon2id.
- Six agents sp?cialis?s et un orchestrateur.
- Audit de 25 fichiers Python synth?tiques.
- Attaque par dictionnaire.
- Comparaison Argon2id, scrypt, bcrypt et PBKDF2-SHA256.
- Gestion du pepper.
- V?rification facultative Pwned Passwords avec k-anonymity.
- Simulation statistique de migration sur 90 jours.

## Installation

Python 3.11 ou sup?rieur.

```powershell
python -m pip install -e ".[dev]"
```

## Tests

```powershell
python -m pytest -q
python -m pytest --cov=src/hash_audit --cov=app --cov-report=term-missing
```

Derni?re r?f?rence locale : 66 tests r?ussis et 87 % de couverture, le 12 novembre 2026.

## Limites

Les donn?es sont synth?tiques. Les r?sultats sur 25 fichiers ne garantissent pas une d?tection parfaite en production. Les benchmarks d?pendent du mat?riel. La migration est une simulation statistique. Une validation humaine reste n?cessaire.

## Documentation

- AUDIT.md
- SYSTEM_CARD.md
- AI_USAGE.md

## Auteur

Imelda Magu?
https://github.com/imeldamague
