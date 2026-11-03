"""Command-line course and roadmap advisor.

Example:
  python advisor_cli.py --level Bachelor --courses "Programming in Python,Statistics for Data Science,Linear Algebra" --interest "Data Science & AI"
"""
import argparse
import difflib
from src.advisor import CourseAdvisor, roadmap_markdown
from src.catalog import DOMAINS, LEVELS

p = argparse.ArgumentParser(description="Recommend next topics and a future roadmap.")
p.add_argument("--level", choices=LEVELS, required=True, help="Class 12, Bachelor or Postgraduate")
p.add_argument("--courses", required=True, help="comma-separated courses completed or in progress")
p.add_argument("--interest", choices=DOMAINS, default=None, help="optional interest area")
p.add_argument("--steps", type=int, default=4, help="courses in each learning path")
p.add_argument("--out", default=None, help="optional path to save the roadmap as Markdown")
a = p.parse_args()

adv = CourseAdvisor()
names = list(adv.cat["name"])
done = []
for c in [x.strip() for x in a.courses.split(",") if x.strip()]:
    hit = next((n for n in names if n.lower() == c.lower()), None)
    if hit is None:
        raise SystemExit(f"Unknown course '{c}'. Did you mean: {difflib.get_close_matches(c, names, 3)}")
    done.append(hit)

result = adv.roadmap(done, a.level, a.interest, a.steps)
text = roadmap_markdown(result, done)
print(text)
if a.out:
    open(a.out, "w", encoding="utf-8").write(text)
    print(f"Saved to {a.out}")
