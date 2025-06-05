from datetime import datetime, timedelta

def classify_recency(
    last_reviewed: str,
    recall_score: int,
    times_seen: int,
    difficulty: int,
    now: datetime = datetime.utcnow()
) -> dict:
    last = datetime.fromisoformat(last_reviewed)
    days_since = (now - last).days

    # Spaced repetition rule (simplified SM2 logic)
    next_review_in_days = (recall_score + 1) * (4 - difficulty) * (1 + times_seen // 2)
    status = "LATER"
    score = 0.5

    if days_since >= next_review_in_days:
        status = "REVIEW_NOW"
        score = 1.0
    elif recall_score == 2 and times_seen >= 5:
        status = "MASTERED"
        score = 0.0

    return {
        "score": score,
        "status": status,
        "days_since": days_since,
        "next_review_after": next_review_in_days
    }
