"""Offline evaluation with a per-student hold-out split."""
import numpy as np
import pandas as pd
from .recommender import POSITIVE, HybridRecommender

MODES = ["popularity", "content", "collaborative", "hybrid"]


def split_interactions(inter, test_frac=0.2, seed=42):
    rng = np.random.default_rng(seed)
    test_idx = []
    for _, g in inter[inter.score >= POSITIVE].groupby("student_id"):
        if len(g) < 3:
            continue
        n_test = max(1, int(round(len(g) * test_frac)))
        test_idx.extend(rng.choice(g.index.values, n_test, replace=False))
    test = inter.loc[test_idx]
    return inter.drop(test.index), test


def ranking_metrics(recs, relevant, k):
    hits = [1 if r in relevant else 0 for r in recs[:k]]
    dcg = sum(h / np.log2(i + 2) for i, h in enumerate(hits))
    idcg = sum(1 / np.log2(i + 2) for i in range(min(len(relevant), k)))
    return (sum(hits) / k, sum(hits) / len(relevant), dcg / idcg if idcg else 0.0, float(sum(hits) > 0))


def evaluate(students, topics, inter, k=5, seed=42):
    train, test = split_interactions(inter, seed=seed)
    model = HybridRecommender().fit(students, topics, train)
    relevant = test.groupby("student_id").topic_id.apply(set)
    rows = {}
    for mode in MODES:
        res = [ranking_metrics(model.top_ids(sid, k, mode), rel, k) for sid, rel in relevant.items()]
        rows[mode] = np.mean(res, axis=0)
    return pd.DataFrame(rows, index=[f"Precision@{k}", f"Recall@{k}", f"NDCG@{k}", f"HitRate@{k}"]).T.round(4)
