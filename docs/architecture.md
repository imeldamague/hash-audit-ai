

# Architecture du système



## Vue d'ensemble



Hash-Audit AI repose sur une architecture multi-agents conçue pour analyser les mécanismes de hachage et les pratiques de stockage des mots de passe.



Le système associe des agents spécialisés à un orchestrateur chargé de coordonner les opérations d'audit.



## Les six agents spécialisés



| Agent | Rôle |

|---|---|

| Explorateur | Collecte et analyse les éléments à auditer. |

| Identificateur | Identifie les mécanismes de hachage utilisés. |

| Évaluateur | Analyse les risques associés aux mécanismes détectés. |

| Correcteur | Propose des recommandations de sécurisation. |

| Testeur | Vérifie les résultats produits. |

| Auditeur | Contrôle et synthétise les résultats de l'audit. |



## Orchestration



L'orchestrateur coordonne les agents et organise le traitement des informations.



Les agents s'appuient sur un état de travail partagé et des traces permettant de suivre les opérations réalisées.



## Technologies utilisées



- **Python :** développement de l'application.

- **Argon2id :** mécanisme recommandé pour le stockage sécurisé des mots de passe.

- **bcrypt, scrypt et PBKDF2-SHA256 :** mécanismes utilisés pour les comparaisons.

- **Ollama :** intégration facultative de modèles d'IA locaux.

- **JSONL :** traçabilité des opérations.

- **Pytest :** tests automatisés.



## Fonctionnement local de l'IA



L'intégration d'Ollama est facultative et dépend de la configuration utilisée.



Les audits en lot peuvent fonctionner sans appel à un modèle de langage. Les résultats doivent toujours faire l'objet d'une validation humaine.



## Schéma logique



```text

              CODE SOURCE À AUDITER

                       |

                       v

                 ORCHESTRATEUR

                       |

          +------------+------------+

          |            |            |

          v            v            v

     EXPLORATEUR  IDENTIFICATEUR  ÉVALUATEUR

          |            |            |

          +------------+------------+

                       |

                       v

                  CORRECTEUR

                       |

                       v

                    TESTEUR

                       |

                       v

                   AUDITEUR

                       |

                       v

              RAPPORT ET TRACES

```



## Traçabilité



Le système conserve des traces des opérations d'audit au format JSONL afin de faciliter l'analyse et le suivi des traitements.



---



[Retour à l'accueil](index.md)



