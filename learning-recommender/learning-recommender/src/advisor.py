"""Course advisor: recommends the next topics for a student and builds a staged roadmap.

Score of a candidate course = 0.35 * similarity to completed courses (TF-IDF cosine)
                            + 0.40 * prerequisite coverage
                            + 0.25 * domain fit (stated interest, or domain of completed courses)
"""
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .catalog import CAREERS, SPECIALISATIONS, build_catalog

W_SIM, W_PRE, W_DOM = 0.35, 0.40, 0.25
COLS = ["name", "level", "kind", "domain", "score", "ready", "missing", "why"]
UG, PGL = "Bachelor", "Postgraduate"


def _fmt(missing):
    return ", ".join(m.replace("|", " or ") for m in missing)


class CourseAdvisor:
    def __init__(self, catalog=None):
        self.cat = (catalog if catalog is not None else build_catalog()).reset_index(drop=True)
        self.idx = {n: i for i, n in enumerate(self.cat["name"])}
        text = self.cat["name"] + " " + self.cat["description"]
        self.X = TfidfVectorizer(stop_words="english").fit_transform(text)
        self.S = cosine_similarity(self.X)  # course-to-course similarity

    # ---- building blocks ---------------------------------------------------
    def _pool(self, level, kind, entry_only=False):
        m = (self.cat["level"] == level) & (self.cat["kind"] == kind)
        if entry_only:
            m &= self.cat["entry"]
        return self.cat[m]

    @staticmethod
    def _coverage(prereqs, done):
        if not prereqs:
            return 1.0, []
        missing = [p for p in prereqs if not any(a in done for a in p.split("|"))]
        return 1 - len(missing) / len(prereqs), missing

    def score(self, pool, done, interest=None):
        """Rank the courses in `pool` for a student who has completed `done`."""
        done = {d for d in done if d in self.idx}
        pool = pool[~pool["name"].isin(done)]
        if pool.empty:
            return pd.DataFrame(columns=COLS)
        didx = [self.idx[d] for d in done]
        rows = []
        for r in pool.itertuples():
            i = self.idx[r.name]
            cov, miss = self._coverage(r.prereqs, done)
            sim = float(self.S[i, didx].mean()) if didx else 0.0
            rows.append((r, i, sim, cov, miss))
        sims = np.array([x[2] for x in rows])
        spread = sims.max() - sims.min()
        simn = (sims - sims.min()) / spread if spread > 0 else np.zeros_like(sims)
        share = self.cat[self.cat["name"].isin(done)]["domain"].value_counts(normalize=True)
        out = []
        for (r, i, sim, cov, miss), sn in zip(rows, simn):
            dom = float(r.domain == interest) if interest else float(share.get(r.domain, 0.0))
            why = []
            if didx:
                j = didx[int(np.argmax(self.S[i, didx]))]
                if self.S[i, j] > 0.05:
                    why.append(f"builds on {self.cat['name'][j]}")
            if interest and r.domain == interest:
                why.append(f"matches your interest in {interest}")
            why.append("all prerequisites completed" if not miss else "first learn: " + _fmt(miss))
            out.append({"name": r.name, "level": r.level, "kind": r.kind, "domain": r.domain,
                        "score": round(W_SIM * sn + W_PRE * cov + W_DOM * dom, 3),
                        "ready": not miss, "missing": miss, "why": "; ".join(why)})
        df = pd.DataFrame(out)
        return df.sort_values(["ready", "score"], ascending=False, kind="stable").reset_index(drop=True)

    def _path(self, pool, done, interest, steps):
        """Greedy learning path: take the best course, mark it done, repeat."""
        done, picks = set(done), []
        for _ in range(steps):
            r = self.score(pool, done, interest)
            if r.empty:
                break
            picks.append(r.iloc[0])
            done.add(r.iloc[0]["name"])
        return (pd.DataFrame(picks, columns=COLS) if picks else pd.DataFrame(columns=COLS)), done

    # ---- public API --------------------------------------------------------
    def next_topics(self, done, level, interest=None, n=5):
        """Best next courses for the student's current level."""
        lv = UG if level == "Class 12" else level
        return self.score(self._pool(lv, "Course", entry_only=(level == "Class 12")), done, interest).head(n)

    def next_programs(self, done, level, interest=None, n=3):
        nxt = {"Class 12": UG, UG: PGL}.get(level)
        if nxt is None:
            return pd.DataFrame(columns=COLS)
        return self.score(self._pool(nxt, "Program"), done, interest).head(n)

    def roadmap(self, done, level, interest=None, steps=4):
        base = {d for d in done if d in self.idx}
        stages = []

        def stage(title, when, df, note=""):
            stages.append({"title": title, "when": when, "note": note, "items": df.to_dict("records")})

        if level == "Class 12":
            start = self.next_topics(base, level, interest, 3)
            stage("Start learning now", "Next 3-6 months", start, "Starter topics to prepare for college.")
            stage("Choose your degree", "Admission year", self.next_programs(base, level, interest, 3),
                  "Bachelor programs that fit your Class 12 subjects.")
            path, d2 = self._path(self._pool(UG, "Course"), base | set(start["name"]), interest, steps + 1)
            stage("During your bachelor's", "Years 1 to 3", path)
            stage("Postgraduate options", "After graduation", self.score(self._pool(PGL, "Program"), d2, interest).head(3))
        elif level == UG:
            nxt = self.next_topics(base, level, interest, 3)
            stage("Next topics", "This semester", nxt)
            path, d2 = self._path(self._pool(UG, "Course"), base | set(nxt["name"]), interest, steps)
            stage("Rest of your bachelor's", "Coming semesters", path)
            stage("Postgraduate options", "After graduation", self.score(self._pool(PGL, "Program"), d2, interest).head(3))
            stage("Advanced topics ahead", "During postgraduate study", self.score(self._pool(PGL, "Course"), d2, interest).head(3))
        else:
            nxt = self.next_topics(base, level, interest, 3)
            stage("Next topics", "This semester", nxt)
            path, _ = self._path(self._pool(PGL, "Course"), base | set(nxt["name"]), interest, steps)
            stage("Specialise", "Coming semesters", path)

        domain = interest or self._infer_domain(stages)
        if level == PGL:
            spec = pd.DataFrame([{"name": s, "kind": "Pathway", "level": PGL, "domain": domain, "why": "Further study and research"}
                                 for s in SPECIALISATIONS[domain]])
            stage("Research and further study", "After your degree", spec)
        roles, skills = CAREERS[domain]
        stage("Career outcomes", "After your studies",
              pd.DataFrame([{"name": r, "kind": "Career", "level": "", "domain": domain, "why": ""} for r in roles]))
        stages[-1]["skills"] = skills
        return {"level": level, "domain": domain, "stages": stages}

    @staticmethod
    def _infer_domain(stages):
        w = defaultdict(float)
        for s in stages:
            for it in s["items"]:
                w[it["domain"]] += it.get("score", 0) + 0.01
        return max(w, key=w.get) if w else "Computer Science & IT"


def roadmap_markdown(result, completed):
    lines = [f"# Learning roadmap ({result['level']})", "", f"Focus area: {result['domain']}",
             f"Courses completed: {', '.join(completed)}", ""]
    for k, s in enumerate(result["stages"], 1):
        lines.append(f"## {k}. {s['title']} ({s['when']})")
        if s.get("note"):
            lines.append(s["note"])
        for it in s["items"]:
            kind = f" ({it['kind']})" if it.get("kind") in ("Program", "Course") else ""
            lines.append(f"- **{it['name']}**{kind}" + (f": {it['why']}" if it.get("why") else ""))
        if s.get("skills"):
            lines.append("Key skills: " + ", ".join(s["skills"]))
        lines.append("")
    return "\n".join(lines)


def catalog_consistency(adv, k=5, use_interest=False):
    """Sanity check on the catalogue (not student data): given exactly the prerequisites of a
    course, does the advisor rank that course within the top k of its level and kind?"""
    ranks = []
    for c in adv.cat.itertuples():
        if not c.prereqs or c.level == "Class 12":
            continue
        done = {p.split("|")[0] for p in c.prereqs}
        pool = adv.cat[(adv.cat["level"] == c.level) & (adv.cat["kind"] == c.kind)]
        r = adv.score(pool, done, c.domain if use_interest else None)
        ranks.append(list(r["name"]).index(c.name) + 1)
    ranks = np.array(ranks)
    return {"courses_tested": len(ranks), f"hit@{k}": round(float((ranks <= k).mean()), 3),
            "mrr": round(float((1 / ranks).mean()), 3)}
