# System Card — Hash-Audit AI

## Présentation

Hash-Audit AI est un prototype pédagogique local d'audit des mécanismes de stockage des mots de passe. Il analyse du code source, identifie des schémas de hachage et illustre les risques associés aux algorithmes rapides ou mal configurés.

## Usages prévus

- Apprentissage de la sécurité du stockage des mots de passe.
- Démonstration de l'identification de schémas MD5, SHA-256 et Argon2id.
- Comparaison de fonctions adaptées au stockage des mots de passe.
- Expérimentation d'une architecture multi-agents.
- Analyse de fichiers synthétiques et reproductibles.
- Illustration d'une migration progressive vers Argon2id.

## Architecture et fonctionnement

Le projet comporte six agents spécialisés coordonnés par une orchestration et partageant un état de travail typé. Les traces permettent de suivre les étapes de l'analyse.

Une intégration à des modèles locaux via Ollama est présente dans le projet. Son utilisation dépend de la configuration et de la disponibilité du service local. L'audit par lots désactive l'appel au LLM.

## Données

Les jeux de comptes et les fichiers de mutation sont synthétiques. Aucun jeu de données réel d'identifiants ou de mots de passe d'utilisateurs n'est nécessaire.

## Sécurité et confidentialité

- Les mots de passe de démonstration ne doivent jamais être réutilisés dans un environnement réel.
- Le pepper doit être conservé séparément de la base contenant les empreintes.
- La vérification Pwned Passwords utilise le mécanisme k-anonymity : seul le préfixe de l'empreinte SHA-1 est transmis au service.
- Cette vérification est facultative et désactivée par défaut dans la démonstration.
- Les fichiers analysés ne doivent pas être exécutés simplement parce qu'ils sont soumis à l'audit.

## Limites

- L'analyse repose notamment sur des motifs et des règles statiques ; des faux positifs et faux négatifs sont possibles.
- Les résultats sur 25 fichiers synthétiques ne prouvent pas une détection parfaite sur des applications réelles.
- Les modèles locaux peuvent produire des réponses incorrectes, incomplètes ou non pertinentes.
- Les benchmarks dépendent du matériel et des paramètres utilisés.
- La simulation de migration est statistique et ne constitue pas une migration réelle.
- Le prototype n'est ni un outil de certification ni un remplacement d'un audit professionnel.

## Supervision humaine

Les résultats, recommandations et éventuels correctifs doivent être examinés et validés par une personne compétente avant toute utilisation. Aucun correctif généré automatiquement ne doit être appliqué aveuglément.

## Public cible

Étudiants, enseignants et développeurs souhaitant comprendre les mécanismes de hachage des mots de passe et les principes d'un audit de sécurité assisté par agents.
