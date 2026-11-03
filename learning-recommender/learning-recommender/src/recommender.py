"""Hybrid recommender: content-based + user-based collaborative filtering
+ K-Means cluster popularity for cold-start students."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from .preprocess import RESOURCES, SUBJECTS, FeatureBuilder, ability_level

POSITIVE = 3  # rating at or above this counts as a positive interaction


def _norm(x):
    x = np.asarray(x, dtype=float)
    return (x - x.min()) / (x.max() - x.min() + 1e-9)


class HybridRecommender:
    def __init__(self, n_clusters=5, k_neighbors=20, w_cf=0.6, w_cb=0.4, seed=42):
        self.n_clusters, self.k, self.w_cf, self.w_cb, self.seed = n_clusters, k_neighbors, w_cf, w_cb, seed

    def fit(self, students, topics, interactions):
        self.students = students.reset_index(drop=True)
        self.topics = topics.reset_index(drop=True)
        self.uid = {s: i for i, s in enumerate(self.students.student_id)}
        self.tid = {t: i for i, t in enumerate(self.topics.topic_id)}
        R = np.zeros((len(self.students), len(self.topics)))
        for r in interactions.itertuples():
            R[self.uid[r.student_id], self.tid[r.topic_id]] = r.score
        self.R = R
        subj = (self.topics.subject.to_numpy(dtype=object)[:, None] == np.array(SUBJECTS)[None, :]).astype(float)
        res = (self.topics.resource_type.to_numpy(dtype=object)[:, None] == np.array(RESOURCES)[None, :]).astype(float)
        self.TF = np.hstack([subj, res, self.topics.difficulty.values[:, None] / 5.0])
        self.fb = FeatureBuilder().fit(self.students)
        X = self.fb.transform(self.students)
        self.km = KMeans(self.n_clusters, n_init=10, random_state=self.seed).fit(X)
        self.cluster = self.km.labels_
        pos = (R >= POSITIVE).astype(float)
        self.pop = pos.sum(0)
        self.cluster_pop = np.vstack([pos[self.cluster == c].mean(0) if (self.cluster == c).any()
                                      else np.zeros(R.shape[1]) for c in range(self.n_clusters)])
        self.sim = cosine_similarity(R)
        np.fill_diagonal(self.sim, 0)
        return self

    # ---- scoring components ------------------------------------------------
    def _fit_factor(self, prev_score, style):
        gap = np.abs(self.topics.difficulty.values - ability_level(prev_score))
        return np.exp(-gap / 2) * (1 + 0.15 * (self.topics.resource_type.to_numpy(dtype=object) == style))

    def _interest_profile(self, subject):
        prof = np.zeros(self.TF.shape[1])
        prof[SUBJECTS.index(subject)] = 1
        return prof

    def _content_from(self, prof, prev_score, style):
        return cosine_similarity(prof.reshape(1, -1), self.TF)[0] * self._fit_factor(prev_score, style)

    def _content(self, i):
        s, r = self.students.iloc[i], self.R[i]
        pos = np.where(r >= POSITIVE, r, 0)
        prof = pos @ self.TF / pos.sum() if pos.sum() > 0 else self._interest_profile(s.interest)
        return self._content_from(prof, s.prev_score, s.learning_style)

    def _cf(self, i):
        nn = np.argsort(self.sim[i])[::-1][: self.k]
        w = self.sim[i][nn]
        if w.sum() <= 0:
            return np.zeros(self.R.shape[1])
        return (w[:, None] * self.R[nn]).sum(0) / w.sum()

    def _scores(self, i, mode):
        if mode == "popularity":
            return self.pop.astype(float)
        if mode == "content":
            return self._content(i)
        cf = self._cf(i)
        if mode == "collaborative":
            return cf
        if self.R[i].sum() == 0:  # cold start: cluster popularity + content
            return 0.5 * _norm(self.cluster_pop[self.cluster[i]]) + 0.5 * _norm(self._content(i))
        return self.w_cf * _norm(cf) + self.w_cb * _norm(self._content(i))

    # ---- public API --------------------------------------------------------
    def top_ids(self, student_id, k=5, mode="hybrid"):
        i = self.uid[student_id]
        sc = self._scores(i, mode).astype(float)
        sc[self.R[i] > 0] = -np.inf
        return [int(self.topics.topic_id.iloc[j]) for j in np.argsort(sc)[::-1][:k]]

    def recommend(self, student_id, n=5, mode="hybrid", exclude_seen=True):
        i = self.uid[student_id]
        seen = self.R[i] > 0 if exclude_seen else np.zeros(self.R.shape[1], bool)
        return self._format(self._scores(i, mode), seen, n, self.students.iloc[i])

    def recommend_for_profile(self, profile, completed_ids=(), n=5):
        """Recommend for a brand-new student described by a dict of features."""
        x = self.fb.transform(pd.DataFrame([profile]))
        cl = int(self.km.predict(x)[0])
        pos = np.zeros(len(self.topics))
        for t in completed_ids:
            pos[self.tid[t]] = 4
        prof = self._interest_profile(profile["interest"])
        if pos.sum() > 0:
            prof = 0.5 * prof + 0.5 * (pos @ self.TF / pos.sum())
        content = self._content_from(prof, profile["prev_score"], profile["learning_style"])
        sc = 0.5 * _norm(self.cluster_pop[cl]) + 0.5 * _norm(content)
        return self._format(sc, pos > 0, n, profile)

    def _format(self, sc, seen, n, s):
        sc = _norm(sc)
        sc[seen] = -1
        ability = float(ability_level(s["prev_score"]))
        rows = []
        for j in np.argsort(sc)[::-1][:n]:
            t = self.topics.iloc[j]
            why = []
            if t.subject == s["interest"]:
                why.append(f"matches your interest in {t.subject}")
            if abs(t.difficulty - ability) <= 1:
                why.append("difficulty suits your level")
            if t.resource_type == s["learning_style"]:
                why.append(f"{t.resource_type} fits your learning style")
            rows.append({"topic": t.topic, "subject": t.subject, "difficulty": int(t.difficulty),
                         "resource_type": t.resource_type, "score": round(float(sc[j]), 3),
                         "reason": "; ".join(why) or "popular among similar students"})
        return pd.DataFrame(rows)
