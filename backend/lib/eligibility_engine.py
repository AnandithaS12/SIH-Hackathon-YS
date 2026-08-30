"""Eligibility engine — orchestration only.

The individual criterion rules live in `lib/eligibility_checks.py` and the persona
rules in `lib/personas.py`. This module composes them and turns the collected
verdicts into a single EligibilityResult.
"""

from typing import Optional

from models.citizen import CitizenProfile, EligibilityResult, PersonaInfo
from models.scheme import Scheme
from lib.eligibility_checks import (
    CRITERION_CHECKS,
    CheckResult,
    build_document_status,
)
from lib.personas import determine_persona as _determine_persona

# Re-exported so existing callers keep importing determine_persona from here.
__all__ = ["determine_persona", "evaluate_scheme_eligibility"]

# A profile missing at most this many criteria, with a score at or above the
# threshold, is surfaced as a likely ("partially eligible") match.
PARTIAL_MAX_MISSING = 2
PARTIAL_MIN_SCORE = 60


def determine_persona(profile: CitizenProfile) -> PersonaInfo:
    return _determine_persona(profile)


def _match_score(result: CheckResult) -> int:
    total = len(result.passed) + len(result.missing)
    if total == 0:
        return 100
    return int((len(result.passed) / total) * 100)


def _first_document_name(scheme: Scheme) -> str:
    return scheme.required_documents[0].name if scheme.required_documents else "Aadhaar"


def _classify(result: CheckResult, score: int, scheme: Scheme) -> tuple[str, bool, str]:
    """Return (status, is_fully_eligible, next_action_tip).

    Every branch is terminal, and the defaults below guarantee the three values
    are always defined regardless of which branch is taken.
    """
    status = "INELIGIBLE"
    is_fully_eligible = False
    next_action_tip = "Review the eligibility criteria for this scheme."

    if not result.missing:
        status = "ELIGIBLE"
        is_fully_eligible = True
        next_action_tip = (
            f"You satisfy all criteria! Have your {_first_document_name(scheme)} ready "
            "and apply directly on the official portal."
        )
    elif result.hard_blockers:
        # Decisive mismatch (wrong state/gender/area, or a PwD-only scheme).
        next_action_tip = f"Not eligible: {result.hard_blockers[0]}"
    elif len(result.missing) == 1 and result.is_conditional:
        status = "PARTIALLY_ELIGIBLE"
        next_action_tip = (
            f"Conditional match: review the requirement for '{result.missing[0]}' "
            "to unlock full benefits."
        )
    elif len(result.missing) <= PARTIAL_MAX_MISSING and score >= PARTIAL_MIN_SCORE:
        status = "PARTIALLY_ELIGIBLE"
        next_action_tip = (
            "Check supporting document verification to confirm your application status."
        )
    else:
        next_action_tip = f"Not directly eligible due to: {result.missing[0]}"

    return status, is_fully_eligible, next_action_tip


def evaluate_scheme_eligibility(
    scheme: Scheme, profile: CitizenProfile, result: Optional[CheckResult] = None
) -> EligibilityResult:
    checks = result or CheckResult()

    for check in CRITERION_CHECKS:
        check(scheme.eligibility_rules, profile, checks, scheme)

    score = _match_score(checks)
    status, is_fully_eligible, next_action_tip = _classify(checks, score, scheme)

    return EligibilityResult(
        scheme_id=scheme.id,
        status=status,
        match_score=score,
        is_fully_eligible=is_fully_eligible,
        passed_criteria=checks.passed,
        missing_criteria=checks.missing,
        next_action_tip=next_action_tip,
        required_documents_status=build_document_status(scheme, profile),
    )
