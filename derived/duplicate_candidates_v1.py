import hashlib
import re
from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher

ALLOWED_REASONS = {
    "high_token_overlap",
    "shared_normalized_phrase",
    "shared_anchor_text",
    "low_edit_distance",
}


def candidate_id_for(claim_ids: List[str]) -> str:
    key = "duplicate_candidates_v1|" + "|".join(sorted(claim_ids))
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def tokenize(text: str) -> List[str]:
    if not text:
        return []
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [t for t in text.split() if t]


def ngrams(tokens: List[str], n: int = 3) -> List[str]:
    if len(tokens) < n:
        return []
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def token_overlap_score(a_tokens: List[str], b_tokens: List[str]) -> float:
    if not a_tokens or not b_tokens:
        return 0.0
    a_set = set(a_tokens)
    b_set = set(b_tokens)
    return len(a_set & b_set) / len(a_set | b_set)


def phrase_overlap_score(a_tokens: List[str], b_tokens: List[str]) -> float:
    a_ngrams = set(ngrams(a_tokens))
    b_ngrams = set(ngrams(b_tokens))
    if not a_ngrams or not b_ngrams:
        return 0.0
    return len(a_ngrams & b_ngrams) / len(a_ngrams | b_ngrams)


def anchor_overlap_score(a_anchors: List[str], b_anchors: List[str]) -> float:
    if not a_anchors or not b_anchors:
        return 0.0
    a_set = set(a.lower() for a in a_anchors)
    b_set = set(b.lower() for b in b_anchors)
    return len(a_set & b_set) / len(a_set | b_set)


def edit_distance_score(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def compute_similarity(
    claim_a: Dict[str, Any], claim_b: Dict[str, Any]
) -> Tuple[float, List[str], Dict[str, float]]:

    a_tokens = tokenize(
        claim_a.get("normalized_statement") or claim_a.get("statement", "")
    )
    b_tokens = tokenize(
        claim_b.get("normalized_statement") or claim_b.get("statement", "")
    )

    token_score = token_overlap_score(a_tokens, b_tokens)
    phrase_score = phrase_overlap_score(a_tokens, b_tokens)
    anchor_score = anchor_overlap_score(
        claim_a.get("anchors", []), claim_b.get("anchors", [])
    )
    edit_score = edit_distance_score(
        claim_a.get("normalized_statement", ""), claim_b.get("normalized_statement", "")
    )

    similarity = (
        0.4 * token_score + 0.3 * phrase_score + 0.2 * anchor_score + 0.1 * edit_score
    )

    reasons = []

    if token_score > 0.6:
        reasons.append("high_token_overlap")

    if phrase_score > 0.5:
        reasons.append("shared_normalized_phrase")

    if anchor_score > 0.5:
        reasons.append("shared_anchor_text")

    if edit_score > 0.8:
        reasons.append("low_edit_distance")

    reasons = [r for r in reasons if r in ALLOWED_REASONS]

    component_scores = {
        "token_overlap": token_score,
        "phrase_overlap": phrase_score,
        "anchor_overlap": anchor_score,
        "edit_similarity": edit_score,
    }

    return similarity, reasons, component_scores


def detect_duplicate_candidates(
    claims: List[Dict[str, Any]], threshold: float = 0.7
) -> Dict[str, Any]:

    candidates = []

    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):

            claim_a = claims[i]
            claim_b = claims[j]

            score, reasons, components = compute_similarity(claim_a, claim_b)

            if score >= threshold and reasons:

                claim_ids = [claim_a["claim_id"], claim_b["claim_id"]]

                candidates.append(
                    {
                        "candidate_id": candidate_id_for(claim_ids),
                        "claim_refs": [
                            {
                                "claim_id": claim_a["claim_id"],
                                "artifact_id": claim_a["artifact_id"],
                            },
                            {
                                "claim_id": claim_b["claim_id"],
                                "artifact_id": claim_b["artifact_id"],
                            },
                        ],
                        "similarity_basis": "lexical",
                        "similarity_score": round(score, 4),
                        "reasons": reasons,
                        "component_scores": components,
                    }
                )

    return {
        "type": "DuplicateCandidateSet",
        "schema_version": "v1",
        "non_authoritative": True,
        "candidates": candidates,
    }
