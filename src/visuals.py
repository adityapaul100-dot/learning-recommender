"""Visualisations used by the app and the pipeline (all return matplotlib figures)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from sklearn.decomposition import PCA
from .preprocess import SUBJECTS

NAVY, ORANGE, BLUE, GREY = "#14213d", "#b85c00", "#2a6f97", "#9aa0a6"
AXES = ["Previous score", "Study hours", "Attendance", "Topics studied", "Average rating"]


def behaviour_table(model):
    """Per-student performance and behaviour metrics on a 0-100 scale."""
    n = (model.R > 0).sum(1)
    avg = np.divide(model.R.sum(1), n, out=np.full(len(n), np.nan), where=n > 0)
    s = model.students
    df = pd.DataFrame({"Previous score": s.prev_score.to_numpy(),
                       "Study hours": np.minimum(s.study_hours.to_numpy() / 30 * 100, 100),
                       "Attendance": s.attendance.to_numpy(),
                       "Topics studied": n / max(n.max(), 1) * 100,
                       "Average rating": avg / 5 * 100})
    df["cluster"] = model.cluster
    return df


def _profile_values(model, student_id, profile, n_done):
    df = behaviour_table(model)
    allm = df[AXES].mean()
    if student_id is not None:
        i = model.uid[student_id]
        v, cl = df.loc[i, AXES].fillna(allm), int(model.cluster[i])
    else:
        cl = int(model.km.predict(model.fb.transform(pd.DataFrame([profile])))[0])
        nmax = max((model.R > 0).sum(1).max(), 1)
        v = pd.Series({"Previous score": profile["prev_score"],
                       "Study hours": min(profile["study_hours"] / 30 * 100, 100),
                       "Attendance": profile["attendance"], "Topics studied": n_done / nmax * 100,
                       "Average rating": allm["Average rating"]})
    return v.astype(float), df[df.cluster == cl][AXES].mean(), allm, cl


def profile_radar(model, student_id=None, profile=None, n_done=0):
    v, clm, allm, cl = _profile_values(model, student_id, profile, n_done)
    ang = np.linspace(0, 2 * np.pi, len(AXES), endpoint=False)
    fig = plt.figure(figsize=(5.2, 4.6))
    ax = fig.add_subplot(111, polar=True)
    for vals, lab, col, fill in [(v.values, "This student", ORANGE, 0.25), (clm.values, f"Cluster {cl} average", BLUE, 0.12),
                                 (allm.values, "All students", GREY, 0.05)]:
        a, y = np.r_[ang, ang[0]], np.r_[vals, vals[0]]
        ax.plot(a, y, color=col, label=lab, linewidth=1.8)
        ax.fill(a, y, color=col, alpha=fill)
    ax.set_xticks(ang)
    ax.set_xticklabels(AXES, fontsize=8)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right", bbox_to_anchor=(1.45, 1.12), fontsize=8)
    ax.set_title("Learning profile (0-100 scale)", fontsize=10, pad=16)
    fig.tight_layout()
    return fig


def cluster_map(model, student_id=None, profile=None):
    X = model.fb.transform(model.students)
    pca = PCA(2, random_state=0)
    Z = pca.fit_transform(X)
    fig, ax = plt.subplots(figsize=(6, 4.5))
    sc = ax.scatter(Z[:, 0], Z[:, 1], c=model.cluster, cmap="tab10", s=14, alpha=0.6)
    handles, _ = sc.legend_elements()
    labels = [f"Cluster {i}" for i in range(len(handles))]
    z = Z[model.uid[student_id]] if student_id is not None else pca.transform(model.fb.transform(pd.DataFrame([profile])))[0]
    ax.scatter(*z, marker="X", s=260, c="black", edgecolors="white", linewidths=1.5, zorder=5)
    handles.append(Line2D([], [], marker="X", color="black", linestyle="", markersize=10))
    labels.append("This student")
    ax.legend(handles, labels, fontsize=8, loc="best")
    ax.set(xlabel=f"Component 1 ({pca.explained_variance_ratio_[0]:.0%} of variance)",
           ylabel=f"Component 2 ({pca.explained_variance_ratio_[1]:.0%} of variance)", title="Student clusters (PCA view)")
    fig.tight_layout()
    return fig


def recommendation_bars(recs):
    colours = dict(zip(SUBJECTS, plt.cm.tab10.colors))
    r = recs.iloc[::-1]
    fig, ax = plt.subplots(figsize=(6, 0.55 * len(r) + 1.3))
    ax.barh(r.topic, r.score, color=[colours[s] for s in r.subject])
    for y, v in enumerate(r.score):
        ax.text(v + 0.01, y, f"{v:.2f}", va="center", fontsize=8)
    ax.set(xlim=(0, 1.1), xlabel="Recommendation score (0-1)", title="Top recommended topics")
    fig.tight_layout()
    return fig


def cluster_subject_heatmap(model):
    subj = model.topics.subject.to_numpy(dtype=object)
    M = np.array([[model.cluster_pop[c][subj == s].mean() for s in SUBJECTS] for c in range(model.n_clusters)])
    fig, ax = plt.subplots(figsize=(7, 4))
    im = ax.imshow(M, cmap="YlOrBr", aspect="auto")
    ax.set_xticks(range(len(SUBJECTS)), SUBJECTS, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(model.n_clusters), [f"Cluster {c}" for c in range(model.n_clusters)])
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, label="Share of positive interactions")
    ax.set_title("What each cluster studies most")
    fig.tight_layout()
    return fig


def cluster_summary(model):
    s = model.students.copy()
    s["cluster"] = model.cluster
    g = s.groupby("cluster")
    df = g.agg(Students=("student_id", "count"), AvgScore=("prev_score", "mean"),
               AvgHours=("study_hours", "mean"), AvgAttendance=("attendance", "mean"))
    df["TopInterest"] = g.interest.agg(lambda x: x.mode().iloc[0])
    df["TopStyle"] = g.learning_style.agg(lambda x: x.mode().iloc[0])
    return df.round(1).reset_index().rename(columns={"cluster": "Cluster"})


def roadmap_timeline(result):
    """Draw the roadmap stages as connected boxes."""
    import textwrap
    from matplotlib.patches import FancyBboxPatch
    stages = result["stages"]
    n = len(stages)
    fig, ax = plt.subplots(figsize=(3.2 * n, 5.4))
    ax.set_xlim(0, 3.2 * n)
    ax.set_ylim(0, 10)
    ax.axis("off")
    cols = [NAVY, BLUE, ORANGE, "#4d7c0f", "#6b4e9b", "#8c2f39"]
    for i, s in enumerate(stages):
        x, col = i * 3.2 + 0.1, cols[i % len(cols)]
        ax.add_patch(FancyBboxPatch((x, 0.3), 2.7, 9.3, boxstyle="round,pad=0.04,rounding_size=0.2", fc="#f4f1ea", ec=col, lw=1.6))
        ax.add_patch(FancyBboxPatch((x, 8.2), 2.7, 1.4, boxstyle="round,pad=0.04,rounding_size=0.2", fc=col, ec=col))
        ax.text(x + 1.35, 8.9, "\n".join(textwrap.wrap(s["title"], 22)), ha="center", va="center", color="white", fontsize=9, fontweight="bold")
        ax.text(x + 1.35, 7.85, s["when"], ha="center", va="center", fontsize=8, style="italic", color=GREY)
        y = 7.3
        for it in s["items"][:6]:
            lines = textwrap.wrap("\u2022 " + it["name"], 27)
            ax.text(x + 0.15, y, "\n".join(lines), va="top", fontsize=8.5, color=NAVY)
            y -= 0.38 * len(lines) + 0.3
        if i < n - 1:
            ax.annotate("", xy=(x + 3.15, 5), xytext=(x + 2.78, 5), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2))
    ax.set_title(f"Roadmap: {result['level']} student, focus on {result['domain']}", fontsize=11, color=NAVY)
    fig.tight_layout()
    return fig


def topic_bars(df):
    domains = sorted(df["domain"].unique())
    colours = dict(zip(domains, plt.cm.tab10.colors))
    r = df.iloc[::-1]
    fig, ax = plt.subplots(figsize=(6.5, 0.5 * len(r) + 1.3))
    ax.barh(r["name"], r["score"], color=[colours[d] for d in r["domain"]])
    for y, v in enumerate(r["score"]):
        ax.text(v + 0.01, y, f"{v:.2f}", va="center", fontsize=8)
    ax.set(xlim=(0, 1.1), xlabel="Recommendation score (0-1)", title="Best next topics")
    fig.tight_layout()
    return fig
