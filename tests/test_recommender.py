import numpy as np
from src.data_gen import generate
from src.evaluate import ranking_metrics
from src.preprocess import clean_interactions, clean_students
from src.recommender import HybridRecommender


def build(tmp_path):
    s, t, i = generate(200, out_dir=str(tmp_path))
    s = clean_students(s)
    return HybridRecommender().fit(s, t, clean_interactions(i, s, t)), s, t, i


def test_cleaning_removes_missing(tmp_path):
    s, _, _ = generate(200, out_dir=str(tmp_path))
    assert clean_students(s).isna().sum().sum() == 0


def test_recommend_excludes_seen_topics(tmp_path):
    model, s, t, i = build(tmp_path)
    sid = int(s.student_id.iloc[0])
    seen = set(t[t.topic_id.isin(i[i.student_id == sid].topic_id)].topic)
    recs = model.recommend(sid, n=5)
    assert len(recs) == 5 and not (set(recs.topic) & seen)


def test_new_student_profile(tmp_path):
    model, *_ = build(tmp_path)
    p = {"prev_score": 70, "study_hours": 8, "attendance": 85, "learning_style": "Video", "interest": "Physics"}
    assert len(model.recommend_for_profile(p, [], 4)) == 4


def test_ranking_metrics_perfect():
    p, r, ndcg, hit = ranking_metrics([1, 2, 3, 4, 5], {1, 2}, 5)
    assert np.isclose(r, 1) and np.isclose(ndcg, 1) and hit == 1


def test_materials_and_visuals(tmp_path):
    import matplotlib.pyplot as plt
    from src import visuals as vz
    from src.resources import attach_materials, build_resources
    model, s, t, i = build(tmp_path)
    res = build_resources(t)
    assert len(res) == 3 * len(t)
    sid = int(s.student_id.iloc[0])
    recs = attach_materials(model.recommend(sid, n=4), t, res, "Video")
    assert recs.study_material.str.contains("Video lecture").all()
    prof = {"prev_score": 70, "study_hours": 8, "attendance": 85, "learning_style": "Video", "interest": "Physics"}
    for fig in [vz.recommendation_bars(recs), vz.profile_radar(model, sid), vz.profile_radar(model, None, prof, 2),
                vz.cluster_map(model, sid), vz.cluster_map(model, None, prof), vz.cluster_subject_heatmap(model)]:
        assert fig is not None
        plt.close(fig)
    assert len(vz.cluster_summary(model)) == model.n_clusters
