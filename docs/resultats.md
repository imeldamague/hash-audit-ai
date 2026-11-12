

# Résultats et performances



## Environnement de validation



Les résultats présentés correspondent à une exécution de référence du projet, réalisée le 12 novembre 2026.



## Tests automatisés



| Indicateur | Résultat |

|---|---:|

| Tests exécutés avec succès | 66 |

| Couverture de code | 87 % |



Ces résultats permettent de vérifier le comportement des composants couverts par les tests.



## Jeu de données synthétiques



Le projet utilise un ensemble de 1 000 comptes synthétiques pour illustrer l'analyse de différents mécanismes de stockage des mots de passe.



Les mécanismes étudiés comprennent notamment :



- MD5 ;

- SHA-256 avec sel ;

- Argon2id.



Aucun compte réel ni mot de passe personnel n'est nécessaire pour cette démonstration.



## Tests de détection



Le jeu de validation comprend 25 fichiers Python synthétiques présentant différentes pratiques de stockage.



Résultat de référence : 25 correspondances correctes sur 25 fichiers contrôlés.



Ce résultat concerne uniquement ce jeu de test construit pour le projet. Il ne représente pas un taux de précision généralisable à des applications réelles.



## Simulation de migration



Une simulation statistique sur 90 jours illustre l'évolution possible d'une migration vers Argon2id.



Elle ne réalise aucune modification réelle de comptes ou de bases de données.



## Interprétation



Les résultats démontrent le fonctionnement du prototype dans un environnement contrôlé.



Ils ne constituent pas une preuve de détection exhaustive ni une certification de sécurité.



---



[Retour à l'accueil](index.md)



