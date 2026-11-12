# Hash-Audit AI

Projet de cybersécurité et d'IA agentique pour l'audit des mécanismes de stockage des mots de passe.

## Fonctionnalités

- Jeu de données synthétique de 1 000 comptes.
- Analyse de MD5, SHA-256 salé et Argon2id.
- Six agents spécialisés et un orchestrateur.
- Audit de 25 fichiers Python synthétiques.
- Simulation d'attaque par dictionnaire.
- Comparaison d'Argon2id, scrypt, bcrypt et PBKDF2-SHA256.
- Gestion du pepper.
- Vérification facultative des mots de passe compromis avec Pwned Passwords et k-anonymity.
- Simulation statistique de migration sur 90 jours.

## Installation

Prérequis : Python 3.11 ou supérieur.

```powershell
python -m pip install -e ".[dev]"
```

## Tests

```powershell
python -m pytest -q
python -m pytest --cov=src/hash_audit --cov=app --cov-report=term-missing
```

Dernière référence locale : 66 tests réussis et 87 % de couverture, le 12 novembre 2026.

## Limites

Les données sont synthétiques. Les résultats obtenus sur 25 fichiers ne garantissent pas une détection parfaite en production. Les benchmarks dépendent du matériel. La migration est une simulation statistique. Une validation humaine reste nécessaire.

## Documentation

- [AUDIT.md](AUDIT.md)
- [SYSTEM_CARD.md](SYSTEM_CARD.md)
- [AI_USAGE.md](AI_USAGE.md)

## Licence

Licence MIT. Voir le fichier [LICENSE](LICENSE).

## Auteur

**Imelda Magué**

[GitHub](https://github.com/imeldamague)
