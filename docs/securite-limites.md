# Sécurité et limites



## Nature du projet



Hash-Audit AI est un prototype pédagogique local destiné à l'apprentissage et à la démonstration de mécanismes d'audit du stockage des mots de passe.



Il ne constitue ni un outil de certification ni un remplacement d'un audit de sécurité professionnel.



## Données utilisées



Le projet utilise des données synthétiques pour ses démonstrations et ses tests.



Il est recommandé de ne jamais fournir de véritables mots de passe, secrets ou données personnelles dans les fichiers soumis à l'analyse.



## Analyse des fichiers



Les fichiers soumis à l'audit ne doivent pas être exécutés simplement parce qu'ils sont analysés.



L'analyse statique présente des limites et peut produire :



- Des faux positifs : une pratique est signalée alors qu'elle n'est pas réellement vulnérable.

- Des faux négatifs : une pratique faible n'est pas détectée.



## Utilisation des modèles d'IA



L'intégration d'Ollama est facultative.



Les réponses des modèles locaux ne constituent pas une validation indépendante de la sécurité des résultats.



Toute recommandation générée doit être vérifiée par une personne compétente.



## Vérification des correctifs



Les recommandations et les éventuels correctifs proposés ne doivent jamais être appliqués automatiquement sans revue, tests et validation humaine.



## Vérification de mots de passe compromis



L'intégration facultative de Pwned Passwords utilise le principe de k-anonymat.



Seul un préfixe de hash SHA-1 est transmis au service, et cette fonctionnalité est désactivée par défaut dans la démonstration.



## Responsabilité



L'utilisation de Hash-Audit AI doit rester encadrée et respecter les règles de confidentialité, les autorisations d'analyse et les bonnes pratiques de cybersécurité.



---



[Retour à l'accueil](index.md)



