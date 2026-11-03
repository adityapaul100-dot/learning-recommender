# Personalized Learning Recommendation System

A machine learning system that analyses student learning behaviour, performance, interests and learning
preferences, and recommends suitable topics and study materials, shown with clear visualisations.

## How the project meets the requirements
| Requirement | Where it is done |
|---|---|
| Student-learning dataset | `src/data_gen.py` (600 students, 30 topics, 90 study materials, 4,771 interactions) |
| Data preprocessing | `src/preprocess.py` (duplicates, missing values, range checks, scaling, one-hot encoding) |
| Exploratory data analysis | `src/eda.py` (distributions, correlation, interactions per subject, feature importance) |
| Behaviour, performance, interests, preferences | features: study hours, attendance, previous score, topics studied, ratings, interest, learning style |
| Model development | `src/recommender.py` (K-Means + content-based + collaborative filtering = hybrid) |
| Evaluation | `src/evaluate.py` (Precision@K, Recall@K, NDCG@K, HitRate@K vs popularity baseline) |
| Recommendations with visualisations | `src/visuals.py` and `app.py` (bar chart, learning-profile radar, cluster map, cluster heatmap) |

## Features
- Recommends topics **and the specific study material** (video lecture, reading guide or practice set) that matches the student's learning style
- Hybrid model with cold-start handling for new students, and a plain-language reason for every recommendation
- Streamlit app with four tabs: Recommendations, Student analysis, Cluster insights, Evaluation and EDA

## Module 2: Course and Career Roadmap Advisor
Takes the student's **level** (Class 12, Bachelor or Postgraduate) and the **courses already studied**, then recommends
the best next topics and builds a staged roadmap: next topics, the rest of the current level, degree or postgraduate
options, and career roles with key skills. The catalogue has 85 entries (8 Class 12 subjects, 11 bachelor programs,
38 bachelor courses, 9 postgraduate programs, 19 postgraduate courses) in five areas.

Score = 0.35 x TF-IDF similarity to completed courses + 0.40 x prerequisite coverage + 0.25 x domain fit.
Courses whose prerequisites are done are ranked first, and each recommendation lists what to learn first if something is missing.

```bash
streamlit run app.py             # then open the "Course Roadmap" page in the sidebar
python advisor_cli.py --level Bachelor --courses "Programming in Python,Statistics for Data Science,Linear Algebra" --interest "Data Science & AI" --out roadmap.md
```

Catalogue consistency check (not student data): given exactly the prerequisites of a course, the advisor ranks that course
in the top 5 of its level in 96.1 percent of 77 cases (MRR 0.815), and in 100 percent when the interest area is given.

## Project structure
```
app.py                 Streamlit interface
run_pipeline.py        data -> cleaning -> EDA -> evaluation -> sample recommendations and charts
src/data_gen.py        synthetic dataset
src/preprocess.py      cleaning and feature engineering
src/eda.py             EDA plots and feature importance
src/recommender.py     hybrid recommendation model
src/resources.py       study-material catalogue and matching
src/visuals.py         recommendation visualisations
src/evaluate.py        hold-out evaluation and metrics
src/catalog.py         course catalogue, careers and specialisations
src/advisor.py         next-topic recommender and roadmap builder
pages/2_Course_Roadmap.py   Streamlit page for the advisor
advisor_cli.py         command-line advisor
tests/                 pytest unit tests
data/                  students.csv, topics.csv, interactions.csv, resources.csv
outputs/               metrics, EDA charts, recommendations/ charts, sample_recommendations.csv
```

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # Mac / Linux
pip install -r requirements.txt
```

## Usage
```bash
python run_pipeline.py           # EDA + evaluation + sample recommendations, saved to outputs/
streamlit run app.py             # launches the web app
pytest                           # runs tests
```

## How it works
1. **Content-based:** builds a taste profile from topics rated 3 or higher, scores topics by cosine similarity, then adjusts for difficulty fit with the student's level and resource type fit with their learning style.
2. **Collaborative:** finds the 20 most similar students (cosine similarity on rating vectors) and averages their ratings.
3. **Hybrid:** `0.6 * collaborative + 0.4 * content` after min-max normalisation.
4. **Cold start:** new students are assigned to a K-Means cluster; scores combine cluster popularity with interest-based content scores.
5. **Study material:** the recommended topic is mapped to the video, article or practice set that matches the student's learning style.

## Results (K=5, synthetic data, seed 42)
| Method | Precision@5 | Recall@5 | NDCG@5 | HitRate@5 |
|---|---|---|---|---|
| Popularity | 0.078 | 0.311 | 0.195 | 0.370 |
| Content | 0.116 | 0.461 | 0.321 | 0.534 |
| Collaborative | 0.108 | 0.438 | 0.321 | 0.501 |
| Hybrid | 0.126 | 0.502 | 0.361 | 0.568 |

The data is synthetic, so these numbers show the pipeline works, not real-world performance. To use real data
(for example OULAD), place `students.csv`, `topics.csv` and `interactions.csv` in `data/` with the same columns.

## Push to GitHub
```bash
git init
git add .
git commit -m "Personalized learning recommender"
git branch -M main
git remote add origin https://github.com/<your-username>/learning-recommender.git
git push -u origin main
```

## License
MIT
