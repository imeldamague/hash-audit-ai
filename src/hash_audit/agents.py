from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from .crypto import identify_format
from .llm import ask_ollama

@dataclass
class AuditState:
    target: str
    files: list[str] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)

class Explorer:
    tools=("lister_fichiers","lire_fichier","grep")
    def run(self,state:AuditState):
        p=Path(state.target)
        if not p.is_file() or p.suffix not in (".py",".txt") or p.stat().st_size>100_000:
            raise ValueError("Only local .py/.txt files under 100 KB are accepted")
        state.files=[str(p)]
        state.trace.append({"agent":"explorateur","files":state.files})


class Identifier:
    tools = ("identifier_format",)

    def run(self, state: AuditState):
        import re

        source = Path(state.target).read_text(encoding="utf-8")

        patterns = {
            "md5": "hashlib.md5",
            "sha1": "hashlib.sha1",
            "argon2id": "PasswordHasher",
        }

        for scheme, needle in patterns.items():
            if needle in source:
                state.findings.append({
                    "scheme": scheme,
                    "indicator": needle,
                    "severity": "high" if scheme in ("md5", "sha1") else "info",
                })

        if "hashlib.sha256" in source:
            password_context = re.search(
                r"\b(password|passwd|pwd)\b",
                source,
                re.IGNORECASE,
            )
            salt_context = re.search(
                r"\b(salt|sel)\b",
                source,
                re.IGNORECASE,
            )

            if password_context:
                scheme = "sha256_salted" if salt_context else "sha256_unsalted"
                state.findings.append({
                    "scheme": scheme,
                    "indicator": "hashlib.sha256",
                    "severity": "high",
                })
            else:
                state.findings.append({
                    "scheme": "sha256_usage_review",
                    "indicator": "hashlib.sha256",
                    "severity": "review",
                })

        match = re.search(
            r"^\s*SCHEME\s*=\s*['\"](md5|sha1|sha256_salted)['\"]",
            source,
            re.MULTILINE,
        )

        if match and not any(
            finding.get("scheme") == match.group(1)
            for finding in state.findings
        ):
            state.findings.append({
                "scheme": match.group(1),
                "indicator": "SCHEME assignment",
                "severity": "high",
            })

        checks = (
            ("constant_salt", "FIXED_SALT"),
            ("timing_comparison", "== digest"),
            ("truncated_hash", "hexdigest()[:"),
            ("bad_encoding", "encode('ascii')"),
        )

        for flag, needle in checks:
            if needle in source:
                state.findings.append({
                    "scheme": flag,
                    "indicator": needle,
                    "severity": "high",
                })

        state.trace.append({
            "agent": "identificateur",
            "findings": len(state.findings),
        })


class Evaluator:
    tools = ("attaque_dictionnaire", "bench_hash")

    def run(self, state: AuditState):
        risky = [
            f for f in state.findings
            if f.get("severity") == "high"
        ]

        if not risky:
            state.trace.append({
                "agent": "evaluateur",
                "assessment": "Aucun risque élevé détecté par les règles.",
                "model": "none",
            })
            return

        schemes = sorted({
            f["scheme"] for f in risky
        })

        prompt = (
            "Tu es un auditeur de sécurité informatique. "
            "Les indicateurs suivants ont été détectés : "
            + ", ".join(schemes)
            + ". Analyse le risque pour le stockage des mots "
            "de passe en 3 phrases maximum, en français. "
            "Pour MD5 et SHA-1, explique que le danger principal "
            "est leur rapidité, facilitant les attaques hors ligne "
            "par dictionnaire ou force brute. "
            "Recommande Argon2id avec un sel aléatoire unique. "
            "Ne prétends pas avoir exécuté d'attaque ni de benchmark."
        )

        try:
            assessment = ask_ollama(
                prompt,
                model="llama3.2:3b",
            )
            model = "llama3.2:3b"
        except Exception as exc:
            assessment = (
                "Analyse IA indisponible. "
                "Les mécanismes signalés doivent être vérifiés."
            )
            model = "fallback"
            state.trace.append({
                "agent": "evaluateur_erreur",
                "error_type": type(exc).__name__,
            })

        state.trace.append({
            "agent": "evaluateur",
            "assessment": assessment,
            "model": model,
        })

class Corrector:
    tools = ("proposer_patch",)

    def run(self, state: AuditState):
        risky = [
            f for f in state.findings
            if f.get("severity") == "high"
        ]

        if not risky:
            state.trace.append({
                "agent": "correcteur",
                "recommendation": "Aucune correction proposée.",
                "model": "none",
            })
            return

        schemes = sorted({
            f["scheme"] for f in risky
        })

        prompt = (
            "Tu es un expert en sécurité des mots de passe. "
            "Une analyse statique a signalé : "
            + ", ".join(schemes)
            + ". Propose une correction défensive en français "
            "en 3 phrases maximum. "
            "Si MD5 ou SHA-1 est utilisé pour les mots de passe, "
            "recommande Argon2id avec un sel aléatoire unique. "
            "Explique que le risque principal des fonctions "
            "rapides est l'attaque hors ligne par dictionnaire "
            "ou force brute, et non les collisions. "
            "Propose une migration progressive après "
            "authentification réussie ou une réinitialisation "
            "du mot de passe. "
            "Ne prétends pas avoir modifié le code."
        )

        try:
            recommendation = ask_ollama(
                prompt,
                model="llama3.2:3b",
            )
            model = "llama3.2:3b"
        except Exception as exc:
            recommendation = (
                "Vérifier les mécanismes signalés. "
                "Pour les mots de passe, privilégier Argon2id "
                "et une migration contrôlée."
            )
            model = "fallback"
            state.trace.append({
                "agent": "correcteur_erreur",
                "error_type": type(exc).__name__,
            })

        state.trace.append({
            "agent": "correcteur",
            "recommendation": recommendation,
            "model": model,
            "patch_applied": False,
        })

    
class Tester:
    tools=("appliquer_patch","pytest")
    def run(self,state:AuditState):
        state.trace.append({"agent":"testeur","status":"not_run","reason":"No patch applied; original target is immutable"})

class PolicyAuditor:
    tools=("verifier_politique",)
    def run(self,state:AuditState):
        state.trace.append({"agent":"auditeur_politique","status":"review_required","reference":"NIST SP 800-63B; ANSSI"})

AGENTS=(Explorer(),Identifier(),Evaluator(),Corrector(),Tester(),PolicyAuditor())

def audit(target:str)->AuditState:
    state=AuditState(target=target)
    for agent in AGENTS: agent.run(state)
    return state
