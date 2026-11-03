"""Exploratory data analysis plots and feature importance."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from .preprocess import NUM, FeatureBuilder


def run_eda(students, topics, inter, out_dir="outputs/eda"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(students.prev_score, bins=25, color="#2a6f97")
    ax.set(title="Distribution of previous scores", xlabel="Previous score", ylabel="Students")
    fig.tight_layout(); fig.savefig(out / "score_distribution.png", dpi=130); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(students.study_hours, students.prev_score, s=10, alpha=0.5, color="#b85c00")
    ax.set(title="Study hours vs previous score", xlabel="Study hours per week", ylabel="Previous score")
    fig.tight_layout(); fig.savefig(out / "hours_vs_score.png", dpi=130); plt.close(fig)

    per_subject = inter.merge(topics, on="topic_id").groupby("subject").size().sort_values()
    fig, ax = plt.subplots(figsize=(6, 4))
    per_subject.plot.barh(ax=ax, color="#2a6f97")
    ax.set(title="Interactions per subject", xlabel="Interactions")
    fig.tight_layout(); fig.savefig(out / "interactions_per_subject.png", dpi=130); plt.close(fig)

    corr = students[NUM].corr()
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(NUM)), NUM, rotation=30); ax.set_yticks(range(len(NUM)), NUM)
    for i in range(len(NUM)):
        for j in range(len(NUM)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
    fig.colorbar(im); ax.set_title("Correlation of numeric features")
    fig.tight_layout(); fig.savefig(out / "correlation.png", dpi=130); plt.close(fig)

    imp = feature_importance(students, inter)
    fig, ax = plt.subplots(figsize=(6, 4))
    imp.sort_values().plot.barh(ax=ax, color="#b85c00")
    ax.set(title="Feature importance for average rating")
    fig.tight_layout(); fig.savefig(out / "feature_importance.png", dpi=130); plt.close(fig)
    return imp


def feature_importance(students, inter):
    avg = inter.groupby("student_id").score.mean()
    df = students[students.student_id.isin(avg.index)]
    fb = FeatureBuilder().fit(df)
    rf = RandomForestRegressor(n_estimators=200, random_state=42).fit(fb.transform(df), avg.loc[df.student_id].values)
    return pd.Series(rf.feature_importances_, index=fb.feature_names()).sort_values(ascending=False)
