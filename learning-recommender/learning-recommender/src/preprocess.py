"""Data cleaning and feature engineering."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SUBJECTS = ["Mathematics", "Programming", "Data Science", "Physics", "Databases", "Networking"]
RESOURCES = ["Video", "Article", "Practice"]
NUM = ["prev_score", "study_hours", "attendance"]
CAT = ["learning_style", "interest"]


def ability_level(score):
    """Map previous score (0-100) to an ability level between 1 and 5."""
    return np.clip(1 + 4 * (np.asarray(score, dtype=float) - 20) / 80, 1, 5)


def clean_students(df):
    df = df.drop_duplicates("student_id").copy()
    for c in NUM:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df[c] = df[c].fillna(df[c].median())
    for c in CAT:
        df[c] = df[c].fillna(df[c].mode().iloc[0])
    df["prev_score"] = df["prev_score"].clip(0, 100)
    df["attendance"] = df["attendance"].clip(0, 100)
    return df.reset_index(drop=True)


def clean_interactions(inter, students, topics):
    inter = inter.dropna().drop_duplicates(["student_id", "topic_id"])
    inter = inter[inter.student_id.isin(students.student_id) & inter.topic_id.isin(topics.topic_id)]
    inter = inter[inter.score.between(1, 5)]
    return inter.reset_index(drop=True)


class FeatureBuilder:
    """Scales numeric features and one-hot encodes categorical ones."""

    def fit(self, df):
        self.ct = ColumnTransformer([
            ("num", StandardScaler(), NUM),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT),
        ])
        self.ct.fit(df[NUM + CAT])
        return self

    def transform(self, df):
        return self.ct.transform(df[NUM + CAT])

    def feature_names(self):
        return [n.split("__", 1)[1] for n in self.ct.get_feature_names_out()]
