# Procédure d'audit — provisoire

1. Installer Python 3.11+ et les dépendances.
2. Exécuter `python -m pytest -q`.
3. Exécuter `python -m hash_audit.cli audit app/demo.py`.
4. Vérifier les six entrées de trace dans `traces/latest.jsonl`.
5. Vérifier que la sortie identifie le MD5 de démonstration.

La procédure de reproductibilité complète demandée par le professeur reste à construire.
