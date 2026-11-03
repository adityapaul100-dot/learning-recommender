"""Study-material catalogue: every topic has a video, a reading guide and a practice set."""
import pandas as pd
from .preprocess import RESOURCES

_FORMATS = {"Video": ("Video lecture", 25, "min watch"),
            "Article": ("Reading guide", 12, "min read"),
            "Practice": ("Practice set", 20, "questions")}


def build_resources(topics):
    rows, rid = [], 0
    for t in topics.itertuples():
        for r in RESOURCES:
            rid += 1
            label, base, unit = _FORMATS[r]
            rows.append({"resource_id": rid, "topic_id": t.topic_id, "resource_type": r,
                         "title": f"{t.topic}: {label}", "effort": f"{base + 5 * t.difficulty} {unit}"})
    return pd.DataFrame(rows)


def attach_materials(recs, topics, resources, style):
    """Add the study material that matches the student's learning style to each recommended topic."""
    tid = dict(zip(topics.topic, topics.topic_id))
    out = recs.copy()
    mats, alts = [], []
    for name in out.topic:
        r = resources[resources.topic_id == tid[name]]
        pref = r[r.resource_type == style].iloc[0]
        mats.append(f"{pref.title} ({pref.effort})")
        alts.append(", ".join(r[r.resource_type != style].resource_type))
    out["study_material"] = mats
    out["also_available"] = alts
    return out
