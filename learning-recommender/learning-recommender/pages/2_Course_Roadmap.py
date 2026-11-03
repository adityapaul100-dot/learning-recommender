"""Course and career roadmap advisor (Streamlit page)."""
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from src import visuals as vz
from src.advisor import CourseAdvisor, roadmap_markdown
from src.catalog import DOMAINS, LEVELS

st.set_page_config(page_title="Course and Roadmap Advisor", layout="wide")


@st.cache_resource
def get_advisor():
    return CourseAdvisor()


def show(fig):
    st.pyplot(fig)
    plt.close(fig)


def table(items):
    rows = [{"Course": i["name"], "Type": i.get("kind", ""), "Level": i.get("level", ""), "Area": i.get("domain", ""),
             "Ready now": "Yes" if i.get("ready", True) else "No", "Why": i.get("why", "")} for i in items]
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


adv = get_advisor()
st.title("Course and Career Roadmap Advisor")
st.caption("Enter your level and the courses you have studied. Get the best next topics and a roadmap to postgraduate study and careers.")

level = st.sidebar.selectbox("Your current level", LEVELS)
choice = st.sidebar.selectbox("Interest area", ["Not sure (infer from my courses)"] + DOMAINS)
interest = None if choice.startswith("Not sure") else choice
allowed = adv.cat[adv.cat["level"].isin(LEVELS[: LEVELS.index(level) + 1])]
label = {r.name: f"{r.name} [{r.level}]" for r in allowed.itertuples()}
done = st.sidebar.multiselect("Courses completed or in progress", list(label), format_func=label.get)
n = st.sidebar.slider("Next topics to show", 3, 10, 5)

if not done:
    st.info("Select at least one course in the sidebar to see recommendations.")
    st.stop()

res = adv.roadmap(done, level, interest)
tab1, tab2, tab3 = st.tabs(["Next topics", "Roadmap", "Careers and skills"])
with tab1:
    nt = adv.next_topics(done, level, interest, n)
    st.subheader("Recommended next topics")
    table(nt.to_dict("records"))
    if not nt.empty:
        show(vz.topic_bars(nt))
with tab2:
    show(vz.roadmap_timeline(res))
    st.download_button("Download roadmap (Markdown)", roadmap_markdown(res, done), file_name="roadmap.md")
    for s in res["stages"]:
        with st.expander(f"{s['title']} - {s['when']}"):
            if s.get("note"):
                st.write(s["note"])
            table(s["items"])
with tab3:
    st.subheader(f"Focus area: {res['domain']}")
    last = res["stages"][-1]
    c1, c2 = st.columns(2)
    c1.markdown("**Career roles**\n\n" + "\n".join(f"- {i['name']}" for i in last["items"]))
    c2.markdown("**Key skills to build**\n\n" + "\n".join(f"- {s}" for s in last.get("skills", [])))
