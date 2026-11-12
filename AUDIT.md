# Procédure d'audit et de reproductibilité

## 1. Préparer l'environnement

Depuis la racine du dépôt, sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install -e ".[dev]"
```

Python 3.11 ou supérieur est requis.

## 2. Exécuter les tests

```powershell
python -m pytest -q
python -m pytest --cov=src/hash_audit --cov=app --cov-report=term-missing
```

Une exécution de référence du 12 novembre 2026 a donné 66 tests réussis et 87 % de couverture. Ces résultats doivent être reconfirmés après modification du code.

## 3. Auditer le fichier de démonstration

```powershell
python -m hash_audit.cli audit app/demo.py
```

Examiner la sortie et la trace JSONL générée. Les détections doivent être interprétées comme des résultats d'analyse statique, et non comme une preuve exhaustive de vulnérabilité.

## 4. Générer et auditer les mutations

```powershell
python -m hash_audit.cli mutations --out data/mutations
python -m hash_audit.cli audit-batch --input data/mutations --out results/mutation_audit.json
```

Le jeu de test contient 25 fichiers synthétiques. Le résultat de référence a obtenu 25 correspondances sur 25 avec les catégories attendues. Cette mesure concerne uniquement ces fichiers contrôlés.

## 5. Générer le jeu de comptes

```powershell
python -m hash_audit.cli dataset --out results/accounts.json
```

Le jeu de données comprend 1 000 comptes synthétiques répartis entre MD5, SHA-256 salé et Argon2id.

## 6. Simuler la migration

```powershell
python -m hash_audit.cli migration --out results/migration.json
```

La simulation couvre 90 jours. Elle est statistique et ne réalise pas la migration effective de comptes ou d'empreintes.

## 7. Comparer les fonctions de hachage

Exécuter le module de benchmark prévu dans le projet et consulter le fichier `results/hash_benchmark.csv`. Les résultats dépendent du matériel, des paramètres et de l'environnement Python. Ils ne constituent pas des performances universelles.

## 8. Vérifier les résultats et les limites

Consulter les fichiers du dossier `results/`, les traces JSONL et les tests automatisés.

Ne jamais utiliser de vrais mots de passe dans les démonstrations. Toute conclusion de sécurité doit être vérifiée par une personne compétente.
