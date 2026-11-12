

# Fonctionnement du projet



## Principe général



Hash-Audit AI analyse les pratiques de stockage des mots de passe à partir de fichiers source et de jeux de données synthétiques.



L'objectif est d'identifier les mécanismes de hachage utilisés, d'évaluer les risques et de proposer des pistes d'amélioration.



## Analyse d'un fichier source



La commande suivante permet d'analyser un fichier :



```bash

python -m hash_audit.cli audit app/demo.py

```



Le système examine les éléments détectés et produit des résultats d'audit.



## Génération de fichiers de test



```bash

python -m hash_audit.cli mutations --out data/mutations

```



Cette commande génère des fichiers Python synthétiques contenant différentes pratiques de stockage de mots de passe.



## Audit en lot



```bash

python -m hash_audit.cli audit-batch --input data/mutations --out results/mutation_audit.json

```



Cette commande permet d'analyser plusieurs fichiers et de regrouper les résultats dans un fichier JSON.



## Génération d'un jeu de données



```bash

python -m hash_audit.cli dataset --out results/accounts.json

```



Le projet utilise un jeu de données synthétiques pour illustrer l'analyse de différents mécanismes de hachage.



## Simulation de migration



```bash

python -m hash_audit.cli migration --out results/migration.json

```



Cette fonctionnalité illustre une simulation statistique de migration vers des mécanismes de stockage plus robustes sur une période de 90 jours.



Il ne s'agit pas d'une migration réelle de comptes utilisateurs.



## Traçabilité



Les opérations sont accompagnées de traces permettant de suivre les traitements et de faciliter l'analyse des résultats.



---



[Retour à l'accueil](index.md)



