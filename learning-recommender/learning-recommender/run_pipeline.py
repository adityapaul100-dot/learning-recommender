"""End-to-end pipeline: data -> cleaning -> EDA -> evaluation -> sample recommendations."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.data_gen import load_or_generate
from src.eda import run_eda
from src.evaluate import evaluate
from src.preprocess import clean_interactions, clean_students
from src import visuals as vz
from src.recommender import HybridRecommender
from src.resources import attach_materials, build_resources

if __name__ == "__main__":
    Path("outputs").mkdir(exist_ok=True)
    students, topics, inter = load_or_generate("data")
    print(f"Loaded {len(students)} students, {len(topics)} topics, {len(inter)} interactions")
    students = clean_students(students)
    inter = clean_interactions(inter, students, topics)

    imp = run_eda(students, topics, inter)
    print("\nTop features:\n", imp.head(5).round(3).to_string())

    metrics = evaluate(students, topics, inter, k=5)
    metrics.to_csv("outputs/metrics.csv")
    print("\nEvaluation (hold-out, K=5):\n", metrics.to_string())
    ax = metrics.plot.bar(figsize=(8, 4), rot=0, colormap="tab20c")
    ax.set(title="Model comparison (K=5)", ylabel="Score")
    plt.tight_layout(); plt.savefig("outputs/metrics.png", dpi=130)

    model = HybridRecommender().fit(students, topics, inter)
    resources = build_resources(topics)
    resources.to_csv("data/resources.csv", index=False)
    sid = int(students.student_id.iloc[0])
    style = students.loc[students.student_id == sid, "learning_style"].iloc[0]
    recs = attach_materials(model.recommend(sid), topics, resources, style)
    recs.to_csv("outputs/sample_recommendations.csv", index=False)
    print(f"\nTop-5 topics and study materials for student {sid} ({style} learner):")
    print(recs[["topic", "study_material", "score", "reason"]].to_string(index=False))

    out = Path("outputs/recommendations")
    out.mkdir(parents=True, exist_ok=True)
    for name, fig in [("recommendations", vz.recommendation_bars(recs)), ("learning_profile", vz.profile_radar(model, sid)),
                      ("cluster_map", vz.cluster_map(model, sid)), ("cluster_subject_heatmap", vz.cluster_subject_heatmap(model))]:
        fig.savefig(out / f"{name}.png", dpi=130, bbox_inches="tight")
        plt.close(fig)
    print("\nCluster summary:\n", vz.cluster_summary(model).to_string(index=False))
    print("\nSaved charts to outputs/ and outputs/recommendations/")
