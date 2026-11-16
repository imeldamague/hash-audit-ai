
# Résultats et performances

Cette page présente les résultats obtenus lors des expérimentations de Hash-Audit AI dans un environnement contrôlé.

## Environnement de validation

Les résultats correspondent à une exécution de référence réalisée le 12 novembre 2026.

## Tests automatisés

| Indicateur | Résultat |
|---|---:|
| Tests exécutés avec succès | 66 |
| Couverture de code | 87 % |

Ces résultats permettent de vérifier le comportement des composants couverts par les tests automatisés.

## Jeu de données synthétiques

Le projet utilise un ensemble de 1 000 comptes synthétiques pour illustrer l'analyse de différents mécanismes de stockage des mots de passe.

Les mécanismes étudiés comprennent :

- MD5 ;
- SHA-256 avec sel ;
- Argon2id.

Aucun compte réel ni mot de passe personnel n'est nécessaire pour cette démonstration.

## Tests de détection

Le jeu de validation comprend 25 fichiers Python synthétiques présentant différentes pratiques de stockage des mots de passe.

Résultat de référence : 25 correspondances correctes sur 25 fichiers contrôlés.

Ce résultat concerne exclusivement le jeu de test construit pour le projet. Il ne représente pas un taux de précision généralisable à des applications réelles.

## Simulation de migration

Une simulation statistique sur 90 jours illustre l'évolution possible d'une migration vers Argon2id.

Cette simulation ne réalise aucune modification réelle de comptes ou de bases de données.

## Interprétation des résultats

Les expérimentations démontrent le fonctionnement du prototype dans un environnement contrôlé.

Elles ne constituent pas une preuve de détection exhaustive, une certification de sécurité ou une validation de performances en environnement de production.

---

[Retour à l'accueil](index.md)
