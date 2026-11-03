"""Creates a synthetic student-learning dataset (students, topics, interactions)."""
from pathlib import Path
import numpy as np
import pandas as pd
from .preprocess import RESOURCES, SUBJECTS, ability_level


def make_topics():
    rows, tid = [], 0
    for s in SUBJECTS:
        for d in range(1, 6):
            tid += 1
            rows.append({"topic_id": tid, "topic": f"{s} - Level {d}", "subject": s,
                         "difficulty": d, "resource_type": RESOURCES[tid % 3]})
    return pd.DataFrame(rows)


def make_students(n, rng):
    df = pd.DataFrame({
        "student_id": np.arange(1, n + 1),
        "prev_score": rng.normal(65, 15, n).clip(20, 100).round(1),
        "study_hours": rng.gamma(3, 2, n).clip(1, 30).round(1),
        "attendance": rng.normal(80, 12, n).clip(30, 100).round(1),
        "learning_style": rng.choice(RESOURCES, n),
        "interest": rng.choice(SUBJECTS, n),
    })
    # inject a few missing values so the cleaning step has something to do
    for col in ["attendance", "study_hours"]:
        df.loc[rng.random(n) < 0.03, col] = np.nan
    return df


def make_interactions(students, topics, rng):
    ability = ability_level(students.prev_score.fillna(65).values)[:, None]
    gap = np.abs(topics.difficulty.values[None, :] - ability)
    interest = students.interest.to_numpy(dtype=object)[:, None] == topics.subject.to_numpy(dtype=object)[None, :]
    style = students.learning_style.to_numpy(dtype=object)[:, None] == topics.resource_type.to_numpy(dtype=object)[None, :]
    hours = students.study_hours.fillna(6).values[:, None]
    logit = -1.5 + 2.0 * interest + 0.6 * style - 0.5 * gap + 0.08 * hours
    p = 1 / (1 + np.exp(-logit))
    taken = rng.random(p.shape) < p
    rating = np.clip(np.round(3 + 1.0 * interest + 0.4 * style - 0.4 * gap
                              + rng.normal(0, 0.6, p.shape)), 1, 5)
    si, ti = np.where(taken)
    return pd.DataFrame({"student_id": students.student_id.values[si],
                         "topic_id": topics.topic_id.values[ti],
                         "score": rating[si, ti].astype(int)})


def generate(n_students=600, seed=42, out_dir="data"):
    rng = np.random.default_rng(seed)
    topics = make_topics()
    students = make_students(n_students, rng)
    inter = make_interactions(students, topics, rng)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    students.to_csv(out / "students.csv", index=False)
    topics.to_csv(out / "topics.csv", index=False)
    inter.to_csv(out / "interactions.csv", index=False)
    return students, topics, inter


def load_or_generate(data_dir="data"):
    d = Path(data_dir)
    if not (d / "interactions.csv").exists():
        return generate(out_dir=data_dir)
    return (pd.read_csv(d / "students.csv"), pd.read_csv(d / "topics.csv"),
            pd.read_csv(d / "interactions.csv"))
