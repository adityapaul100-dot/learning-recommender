from src.advisor import CourseAdvisor, catalog_consistency, roadmap_markdown
from src.catalog import DOMAINS, build_catalog

adv = CourseAdvisor()


def test_catalog_is_consistent():
    cat = build_catalog()
    names = set(cat["name"])
    assert len(names) == len(cat)
    for prereqs in cat["prereqs"]:
        for p in prereqs:
            assert all(a in names for a in p.split("|")), p
    assert set(cat["domain"]) <= set(DOMAINS)


def test_class12_science_student_gets_programs_and_starter_topics():
    res = adv.roadmap(["Mathematics", "Physics", "Chemistry", "Computer Science"], "Class 12")
    stages = {s["title"]: s for s in res["stages"]}
    assert all(i["kind"] == "Course" and i["level"] == "Bachelor" for i in stages["Start learning now"]["items"])
    assert all(i["kind"] == "Program" and i["level"] == "Bachelor" for i in stages["Choose your degree"]["items"])
    assert stages["Postgraduate options"]["items"]


def test_commerce_student_gets_commerce_programs():
    items = adv.next_programs(["Accountancy", "Business Studies", "Economics"], "Class 12", n=2).to_dict("records")
    assert {i["name"] for i in items} <= {"B.Com", "BBA"}


def test_bachelor_data_science_student_next_topic():
    top = adv.next_topics(["Programming in Python", "Statistics for Data Science", "Linear Algebra"], "Bachelor",
                          "Data Science & AI", 3)
    assert "Machine Learning" in set(top["name"])


def test_postgraduate_roadmap_and_markdown():
    done = ["Programming in Python", "Statistics for Data Science", "Linear Algebra", "Machine Learning"]
    res = adv.roadmap(done, "Postgraduate", "Data Science & AI")
    assert res["stages"][0]["items"][0]["level"] == "Postgraduate"
    assert any(s["title"] == "Research and further study" for s in res["stages"])
    assert "Career outcomes" in roadmap_markdown(res, done)


def test_paths_do_not_repeat_courses():
    res = adv.roadmap(["Mathematics", "Computer Science"], "Class 12")
    names = [i["name"] for s in res["stages"] for i in s["items"] if i.get("kind") == "Course"]
    assert len(names) == len(set(names))


def test_catalog_consistency_reasonable():
    assert catalog_consistency(adv)["hit@5"] >= 0.6
