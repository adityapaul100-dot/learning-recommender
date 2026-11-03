
import streamlit as st

st.set_page_config(
    page_title="Personalized Education Advisor",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# COURSE AND CAREER RECOMMENDATION DATABASE
# --------------------------------------------------

COURSES = {
    "Computer Science & IT": {
        "topics": [
            "Python Programming",
            "Data Structures and Algorithms",
            "Database Management Systems",
            "Web Development",
            "Computer Networks",
            "Artificial Intelligence",
            "Machine Learning",
            "Cybersecurity",
            "Cloud Computing"
        ],
        "skills": [
            "Python",
            "Java",
            "SQL",
            "Problem Solving",
            "Git and GitHub",
            "Web Development"
        ],
        "class12": [
            "B.Tech Computer Science",
            "BCA",
            "B.Sc Computer Science",
            "B.Sc Information Technology"
        ],
        "diploma": [
            "B.Tech Computer Science (lateral entry, if eligible)",
            "BCA",
            "B.Sc Computer Science",
            "B.Sc Information Technology"
        ],
        "bachelor": [
            "MCA",
            "M.Sc Computer Science",
            "M.Sc Data Science",
            "M.Sc Artificial Intelligence",
            "M.Tech Computer Science (if eligible)"
        ],
        "master": [
            "Ph.D. in Computer Science",
            "Advanced Research in Artificial Intelligence",
            "Advanced Research in Data Science",
            "Specialized Cybersecurity Certifications"
        ],
        "careers": [
            "Software Developer",
            "Data Analyst",
            "Web Developer",
            "AI/ML Engineer",
            "Cybersecurity Analyst",
            "Cloud Engineer"
        ]
    },

    "Business & Management": {
        "topics": [
            "Business Communication",
            "Financial Accounting",
            "Marketing Management",
            "Human Resource Management",
            "Business Analytics",
            "Entrepreneurship",
            "Financial Management",
            "Business Strategy"
        ],
        "skills": [
            "Communication",
            "Leadership",
            "Excel",
            "Financial Analysis",
            "Digital Marketing",
            "Project Management"
        ],
        "class12": [
            "BBA",
            "B.Com",
            "Bachelor of Management Studies",
            "BA Economics"
        ],
        "diploma": [
            "BBA",
            "B.Com",
            "Bachelor of Management Studies"
        ],
        "bachelor": [
            "MBA",
            "M.Com",
            "MA Economics",
            "PG Diploma in Business Management",
            "Master's in Finance or Marketing"
        ],
        "master": [
            "Ph.D. in Management",
            "Ph.D. in Commerce",
            "Advanced Business Analytics",
            "Executive Management Programs"
        ],
        "careers": [
            "Business Analyst",
            "Marketing Manager",
            "Financial Analyst",
            "HR Manager",
            "Business Consultant",
            "Entrepreneur"
        ]
    },

    "Science & Research": {
        "topics": [
            "Scientific Research Methods",
            "Statistics",
            "Biotechnology",
            "Physics",
            "Chemistry",
            "Data Analysis",
            "Laboratory Techniques",
            "Research Writing"
        ],
        "skills": [
            "Research",
            "Scientific Writing",
            "Statistics",
            "Data Analysis",
            "Laboratory Skills",
            "Critical Thinking"
        ],
        "class12": [
            "B.Sc Physics",
            "B.Sc Chemistry",
            "B.Sc Mathematics",
            "B.Sc Biotechnology",
            "B.Sc Statistics"
        ],
        "diploma": [
            "B.Sc Applied Science",
            "B.Sc Biotechnology",
            "B.Sc Chemistry",
            "B.Sc Mathematics"
        ],
        "bachelor": [
            "M.Sc Physics",
            "M.Sc Chemistry",
            "M.Sc Mathematics",
            "M.Sc Biotechnology",
            "M.Sc Statistics"
        ],
        "master": [
            "Ph.D. in Science",
            "Research Fellowships",
            "Advanced Scientific Research Programs"
        ],
        "careers": [
            "Research Scientist",
            "Laboratory Analyst",
            "Research Assistant",
            "Data Scientist",
            "Science Educator"
        ]
    },

    "Arts & Humanities": {
        "topics": [
            "History",
            "Political Science",
            "Psychology",
            "Sociology",
            "English Literature",
            "Philosophy",
            "Creative Writing",
            "Communication"
        ],
        "skills": [
            "Writing",
            "Communication",
            "Critical Thinking",
            "Research",
            "Public Speaking",
            "Content Creation"
        ],
        "class12": [
            "BA English",
            "BA Psychology",
            "BA History",
            "BA Political Science",
            "BA Sociology"
        ],
        "diploma": [
            "BA English",
            "BA Psychology",
            "BA History",
            "BA Sociology"
        ],
        "bachelor": [
            "MA English",
            "MA Psychology",
            "MA History",
            "MA Political Science",
            "MA Sociology"
        ],
        "master": [
            "Ph.D. in Humanities",
            "Ph.D. in Psychology",
            "Advanced Research Programs"
        ],
        "careers": [
            "Psychologist (with required qualifications)",
            "Content Writer",
            "Journalist",
            "Teacher",
            "Researcher",
            "Social Worker"
        ]
    },

    "Engineering & Technology": {
        "topics": [
            "Engineering Mathematics",
            "Electrical Circuits",
            "Mechanical Design",
            "Computer-Aided Design",
            "Robotics",
            "Electronics",
            "Embedded Systems",
            "Renewable Energy"
        ],
        "skills": [
            "Problem Solving",
            "CAD Tools",
            "Programming",
            "Technical Drawing",
            "Robotics",
            "Project Design"
        ],
        "class12": [
            "B.Tech Mechanical Engineering",
            "B.Tech Electrical Engineering",
            "B.Tech Civil Engineering",
            "B.Tech Electronics Engineering"
        ],
        "diploma": [
            "B.Tech through lateral entry (if eligible)",
            "B.E. through lateral entry (if eligible)",
            "Specialized Engineering Certifications"
        ],
        "bachelor": [
            "M.Tech Mechanical Engineering",
            "M.Tech Electrical Engineering",
            "M.Tech Civil Engineering",
            "M.Tech Electronics Engineering"
        ],
        "master": [
            "Ph.D. in Engineering",
            "Advanced Robotics Research",
            "Advanced Engineering Research"
        ],
        "careers": [
            "Mechanical Engineer",
            "Electrical Engineer",
            "Civil Engineer",
            "Electronics Engineer",
            "Robotics Engineer"
        ]
    },

    "Healthcare & Biology": {
        "topics": [
            "Human Anatomy",
            "Human Physiology",
            "Microbiology",
            "Genetics",
            "Biochemistry",
            "Public Health",
            "Biotechnology",
            "Nutrition"
        ],
        "skills": [
            "Scientific Knowledge",
            "Laboratory Skills",
            "Research",
            "Communication",
            "Patient Care",
            "Data Analysis"
        ],
        "class12": [
            "B.Sc Nursing",
            "B.Sc Biotechnology",
            "B.Sc Microbiology",
            "B.Pharm",
            "Relevant Allied Health Programs"
        ],
        "diploma": [
            "B.Sc Nursing (if eligible)",
            "B.Pharm (if eligible)",
            "Relevant Allied Health Degree Programs"
        ],
        "bachelor": [
            "M.Sc Biotechnology",
            "M.Sc Microbiology",
            "M.Sc Biochemistry",
            "Master of Public Health",
            "M.Sc Nutrition"
        ],
        "master": [
            "Ph.D. in Biotechnology",
            "Ph.D. in Microbiology",
            "Ph.D. in Biomedical Science",
            "Advanced Public Health Research"
        ],
        "careers": [
            "Biotechnologist",
            "Microbiologist",
            "Research Assistant",
            "Public Health Professional",
            "Clinical Research Associate"
        ]
    }
}


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_level_key(qualification):
    mapping = {
        "Class 12": "class12",
        "Diploma": "diploma",
        "Bachelor's Degree": "bachelor",
        "Master's Degree": "master",
        "Other": "class12"
    }
    return mapping[qualification]


def recommend_courses(qualification, interest):
    data = COURSES[interest]
    level = get_level_key(qualification)

    return data[level]


def recommend_next_topics(interest, studied_subjects):
    data = COURSES[interest]
    topics = data["topics"]

    studied = studied_subjects.lower()

    # Put topics that do not appear in the student's
    # previous-study description first.
    new_topics = [
        topic for topic in topics
        if topic.lower() not in studied
    ]

    return new_topics[:6]


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("🎓 Personalized Education & Career Recommendation System")

st.write(
    "Discover suitable courses, higher education options, "
    "important skills and possible career paths based on "
    "your educational background and interests."
)

st.info(
    "Enter your previous education details and area of interest. "
    "The system will suggest possible next steps without asking "
    "you to choose a future career goal."
)


# --------------------------------------------------
# STUDENT INPUT FORM
# --------------------------------------------------

st.header("📚 Student Information")

with st.form("student_form"):

    qualification = st.selectbox(
        "1. What is your highest educational qualification?",
        [
            "Class 12",
            "Diploma",
            "Bachelor's Degree",
            "Master's Degree",
            "Other"
        ]
    )

    stream = st.selectbox(
        "2. Which stream or educational background do you have?",
        [
            "Science",
            "Commerce",
            "Arts / Humanities",
            "Engineering",
            "Medical",
            "Computer Applications",
            "Other"
        ]
    )

    degree = st.text_input(
        "3. Enter your degree, diploma or specialization (if applicable)",
        placeholder="Example: BCA, B.Tech CSE, B.Com, Diploma in Mechanical"
    )

    subjects = st.text_area(
        "4. What subjects or topics have you studied previously?",
        placeholder="Example: Mathematics, Physics, Python, Java, DBMS, Accounting..."
    )

    interest = st.selectbox(
        "5. Which area interests you the most?",
        list(COURSES.keys())
    )

    submitted = st.form_submit_button(
        "Generate My Recommendations",
        use_container_width=True
    )


# --------------------------------------------------
# DISPLAY RECOMMENDATIONS
# --------------------------------------------------

if submitted:

    if not subjects.strip() and not degree.strip():
        st.warning(
            "Please enter at least your previous subjects "
            "or your degree/specialization."
        )

    else:

        st.success("Your recommendations are ready!")

        data = COURSES[interest]

        st.divider()

        # STUDENT PROFILE
        st.header("👤 Your Education Profile")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Highest Qualification:**", qualification)
            st.write("**Educational Stream:**", stream)

        with col2:
            st.write(
                "**Degree / Specialization:**",
                degree if degree.strip() else "Not provided"
            )
            st.write("**Area of Interest:**", interest)

        st.write(
            "**Previously Studied Subjects:**",
            subjects if subjects.strip() else "Not provided"
        )

        st.divider()

        # NEXT TOPICS
        st.header("📖 Recommended Topics to Study Next")

        next_topics = recommend_next_topics(
            interest,
            subjects
        )

        if next_topics:
            for i, topic in enumerate(next_topics, start=1):
                st.write(f"{i}. {topic}")
        else:
            st.write(
                "Review advanced topics and practical projects "
                "in your selected area."
            )

        st.divider()

        # COURSE RECOMMENDATIONS
        st.header("🎓 Recommended Courses and Higher Studies")

        recommended_courses = recommend_courses(
            qualification,
            interest
        )

        for i, course in enumerate(recommended_courses, start=1):
            st.write(f"{i}. {course}")

        if qualification == "Other":
            st.caption(
                "Your qualification is listed as Other, so these "
                "suggestions are general starting points. Check "
                "the admission requirements for your actual qualification."
            )

        st.divider()

        # SKILLS
        st.header("💡 Skills You Should Develop")

        skill_columns = st.columns(2)

        for i, skill in enumerate(data["skills"]):
            with skill_columns[i % 2]:
                st.write(f"✅ {skill}")

        st.divider()

        # CAREER OPTIONS
        st.header("💼 Possible Career Opportunities")

        for career in data["careers"]:
            st.write(f"🔹 {career}")

        st.divider()

        # FINAL NOTE
        st.subheader("📌 Important Note")

        st.caption(
            "These are preliminary, rule-based recommendations "
            "based on your qualification and selected interest area. "
            "They are not AI predictions or admission guarantees. "
            "Actual eligibility depends on university requirements, "
            "entrance examinations, academic results and prerequisites. "
            "For regulated professions, additional qualifications "
            "or licenses may be required."
        )

        st.balloons()
