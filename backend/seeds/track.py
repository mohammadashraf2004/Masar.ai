from app.models.learning import CareerTrack


def seed_track(db) -> CareerTrack:
    track = CareerTrack(
        slug="ai-engineer",
        title="AI Engineer",
        description=(
            "Go from beginner to job-ready AI Engineer. "
            "Build real RAG systems, deploy ML models, and master the full AI engineering stack."
        ),
        icon="🤖",
        estimated_weeks=24,
    )
    db.add(track)
    db.flush()
    print(f"  ✓ Track: {track.title}")
    return track
