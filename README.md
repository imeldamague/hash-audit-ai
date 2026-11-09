# Hash-Audit AI - Sujet 2

Projet pédagogique de cryptographie appliquée et IA agentique. **État : prototype initial v0.1.0, NON conforme à toutes les exigences du sujet.**

## Installation Windows 11 (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
python -m hash_audit.cli audit app/demo.py
```

Si l'activation PowerShell est bloquée, utiliser directement `.\.venv\Scripts\python.exe` à la place de `python`.

## Autres commandes

```powershell
python -m hash_audit.cli dataset
python -m hash_audit.cli mutations
python -m hash_audit.cli migration
python app/demo.py
```

Les variantes MD5/SHA256 sont **volontairement vulnérables** et uniquement destinées à un laboratoire local. Ne jamais y saisir de vrais mots de passe.

## Architecture

Six agents distincts sont présents dans `src/hash_audit/agents.py`, avec un état partagé typé et une trace JSONL. **Ils sont pour l'instant déterministes** ; l'intégration des deux modèles LLM locaux et la vraie boucle de correction/vérification restent à développer.

## Écarts connus avec le cahier des charges

- Manquent : comparaison mesurée Argon2id/bcrypt/scrypt/PBKDF2, poivre hors base et rotation, attaque par dictionnaire chronométrée, politique NIST/ANSSI réelle, comparaison 3 configurations (sans LLM + deux LLM), robustesse aux erreurs et couverture >=70% vérifiée.
- Les 25 mutations sont des fixtures initiales et ne constituent pas encore 25 applications complètes évaluées.
- La migration 90 jours est une simulation de sessions et non une migration effective de 1000 empreintes.
- Manquent : reproductibilité intégrale `make reproduce`, dépendances verrouillées, CI complète, figures, rapport 12–20 pages, GitHub Pages, signature, DOI et vidéo.
- Ne pas présenter les métriques non mesurées comme des résultats expérimentaux.

## Publication

Créer un dépôt GitHub public `hash-audit-ai`, pousser progressivement le code, puis créer la release `v1.0.0` seulement après les tests et la vérification de tous les livrables. Ne jamais publier de secrets.
