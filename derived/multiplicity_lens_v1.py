from typing import List, Dict, Any

# NOTE:
# Assumes candidate_id is deterministic across runs.


def multiplicity_lens(candidate_sets: List[Dict[str, Any]]) -> Dict[str, Any]:

    times = [cs["lineage"]["generated_at"] for cs in candidate_sets]
    if len(times) != len(set(times)):
        raise ValueError("Duplicate generated_at values detected")

    runs = sorted(
        [(cs["lineage"]["generated_at"], cs) for cs in candidate_sets],
        key=lambda x: x[0],
    )

    index: Dict[str, Dict[str, Any]] = {}

    for t, cs in runs:
        for c in cs.get("candidates", []):
            cid = c["candidate_id"]

            if cid not in index:
                index[cid] = {
                    "candidate_id": cid,
                    "claim_refs": c["claim_refs"],
                    "similarity_basis": c["similarity_basis"],
                    "timeline": {},
                }

            index[cid]["timeline"][t] = {
                "similarity_score": c["similarity_score"],
                "reasons": c["reasons"],
            }

    all_times = [t for t, _ in runs]
    results = []

    for cid, entry in index.items():
        present_times = sorted(entry["timeline"].keys())

        if len(present_times) == len(all_times):
            status = "stable"
        elif present_times == [all_times[-1]]:
            status = "emergent"
        elif all_times[-1] not in present_times:
            status = "dissipated"
        else:
            status = "intermittent"

        results.append(
            {
                "candidate_id": cid,
                "claim_refs": entry["claim_refs"],
                "similarity_basis": entry["similarity_basis"],
                "present_in": present_times,
                "timeline": entry["timeline"],
                "status": status,
            }
        )

    results.sort(key=lambda x: x["candidate_id"])

    return {
        "type": "MultiplicityLensView",
        "non_authoritative": True,
        "runs": all_times,
        "run_count": len(all_times),
        "candidates": results,
    }
