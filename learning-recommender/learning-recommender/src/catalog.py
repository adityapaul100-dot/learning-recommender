"""Course catalogue: school subjects, bachelor and postgraduate programs and courses.

A prerequisite written as "A|B" means either A or B is enough.
"""
import pandas as pd

LEVELS = ["Class 12", "Bachelor", "Postgraduate"]
CS, DS, BC, EN, SM = ("Computer Science & IT", "Data Science & AI", "Business & Commerce",
                      "Engineering", "Science & Mathematics")
DOMAINS = [CS, DS, BC, EN, SM]
L12, UG, PG = LEVELS

_ROWS = []


def _add(level, kind, name, domain, desc, prereqs=(), entry=False):
    _ROWS.append({"name": name, "level": level, "kind": kind, "domain": domain,
                  "description": desc, "prereqs": list(prereqs), "entry": entry})


def S(name, domain, desc): _add(L12, "Subject", name, domain, desc)
def P(level, name, domain, desc, pre): _add(level, "Program", name, domain, desc, pre)
def C(level, name, domain, desc, pre, entry=False): _add(level, "Course", name, domain, desc, pre, entry)


# ---- Class 12 subjects ----
S("Mathematics", SM, "algebra calculus trigonometry probability matrices functions")
S("Physics", EN, "mechanics electricity magnetism optics waves modern physics")
S("Chemistry", EN, "organic inorganic physical chemistry reactions materials")
S("Computer Science", CS, "programming python data structures databases computational thinking")
S("Informatics Practices", DS, "python pandas sql data handling visualization")
S("Accountancy", BC, "bookkeeping ledger financial statements accounts")
S("Business Studies", BC, "management marketing finance entrepreneurship organisations")
S("Economics", BC, "demand supply macroeconomics microeconomics national income statistics")

# ---- Bachelor programs ----
P(UG, "BCA", CS, "software development programming databases web applications computer systems", ["Computer Science", "Mathematics"])
P(UG, "B.Sc Computer Science", CS, "algorithms programming operating systems networks mathematics", ["Mathematics", "Computer Science", "Physics"])
P(UG, "B.Tech Computer Science", CS, "software engineering algorithms systems artificial intelligence engineering", ["Mathematics", "Physics", "Chemistry", "Computer Science"])
P(UG, "B.Sc Data Science", DS, "statistics machine learning data analysis programming visualization", ["Mathematics", "Informatics Practices|Computer Science"])
P(UG, "B.Sc Statistics", DS, "probability statistical inference sampling regression data analysis", ["Mathematics", "Economics"])
P(UG, "B.Sc Mathematics", SM, "calculus analysis algebra discrete mathematics numerical methods", ["Mathematics", "Physics"])
P(UG, "B.Sc Physics", SM, "classical mechanics quantum physics electronics experiments", ["Physics", "Mathematics", "Chemistry"])
P(UG, "B.Tech Electronics", EN, "digital electronics signals embedded systems communication circuits", ["Mathematics", "Physics", "Chemistry"])
P(UG, "B.Tech Mechanical", EN, "mechanics thermodynamics fluids machines design manufacturing", ["Mathematics", "Physics", "Chemistry"])
P(UG, "B.Com", BC, "financial accounting taxation corporate finance business economics", ["Accountancy", "Business Studies", "Economics"])
P(UG, "BBA", BC, "management marketing organisational behaviour operations business analytics", ["Business Studies", "Economics", "Mathematics"])

# ---- Bachelor courses ----
C(UG, "Programming in Python", CS, "python variables loops functions programming problem solving", ["Computer Science|Informatics Practices"], True)
C(UG, "Data Structures and Algorithms", CS, "arrays trees graphs sorting searching complexity algorithms", ["Programming in Python"])
C(UG, "Object-Oriented Programming", CS, "classes objects inheritance polymorphism java design", ["Programming in Python"])
C(UG, "Database Management Systems", CS, "sql relational model normalization transactions indexing", ["Programming in Python|Informatics Practices"])
C(UG, "Operating Systems", CS, "processes threads memory scheduling file systems concurrency", ["Data Structures and Algorithms"])
C(UG, "Computer Networks", CS, "tcp ip routing protocols network layers internet", ["Programming in Python"])
C(UG, "Web Development", CS, "html css javascript frontend backend web applications", ["Programming in Python"])
C(UG, "Software Engineering", CS, "requirements design testing agile project management software lifecycle", ["Object-Oriented Programming", "Database Management Systems"])
C(UG, "Cloud Computing", CS, "virtualization containers cloud services scalability deployment", ["Operating Systems", "Computer Networks"])
C(UG, "Cybersecurity Fundamentals", CS, "encryption threats network security authentication vulnerabilities", ["Computer Networks"])
C(UG, "Statistics for Data Science", DS, "descriptive statistics distributions hypothesis testing sampling inference", ["Mathematics"], True)
C(UG, "Linear Algebra", DS, "vectors matrices eigenvalues transformations linear systems", ["Mathematics"], True)
C(UG, "Probability Theory", DS, "random variables distributions expectation bayes theorem", ["Statistics for Data Science"])
C(UG, "Data Analysis with Pandas", DS, "pandas data cleaning exploratory analysis dataframes visualization", ["Programming in Python", "Statistics for Data Science"])
C(UG, "Data Visualization", DS, "charts dashboards storytelling matplotlib visual analytics", ["Data Analysis with Pandas"])
C(UG, "Machine Learning", DS, "supervised unsupervised learning regression classification clustering model evaluation", ["Programming in Python", "Statistics for Data Science", "Linear Algebra"])
C(UG, "Artificial Intelligence Fundamentals", DS, "search knowledge representation reasoning agents intelligent systems", ["Data Structures and Algorithms", "Probability Theory"])
C(UG, "Data Mining", DS, "pattern discovery association rules clustering large datasets", ["Database Management Systems", "Machine Learning"])
C(UG, "Financial Accounting", BC, "journal ledger balance sheet financial statements accounting standards", ["Accountancy"], True)
C(UG, "Marketing Management", BC, "consumer behaviour branding market segmentation promotion", ["Business Studies"], True)
C(UG, "Business Economics", BC, "demand supply market structures pricing macroeconomics", ["Economics"], True)
C(UG, "Organizational Behaviour", BC, "teams leadership motivation culture management", ["Business Studies"], True)
C(UG, "Corporate Finance", BC, "capital budgeting valuation risk financing investment", ["Financial Accounting"])
C(UG, "Business Analytics", BC, "data driven decisions forecasting dashboards business statistics", ["Statistics for Data Science", "Business Economics"])
C(UG, "Operations Management", BC, "supply chain planning inventory quality process improvement", ["Business Economics"])
C(UG, "Digital Marketing", BC, "social media search engine marketing analytics campaigns", ["Marketing Management"])
C(UG, "Digital Electronics", EN, "logic gates flip flops circuits boolean algebra", ["Physics"], True)
C(UG, "Engineering Mechanics", EN, "forces equilibrium statics dynamics structures", ["Physics", "Mathematics"], True)
C(UG, "Thermodynamics", EN, "heat energy entropy cycles engines", ["Engineering Mechanics"])
C(UG, "Fluid Mechanics", EN, "fluid flow pressure viscosity pipes turbines", ["Engineering Mechanics"])
C(UG, "Signals and Systems", EN, "signals fourier transform filters linear systems", ["Digital Electronics", "Linear Algebra"])
C(UG, "Embedded Systems", EN, "microcontrollers sensors firmware real time systems", ["Digital Electronics", "Programming in Python"])
C(UG, "Control Systems", EN, "feedback stability controllers automation modelling", ["Signals and Systems"])
C(UG, "Calculus and Real Analysis", SM, "limits continuity differentiation integration sequences series", ["Mathematics"], True)
C(UG, "Discrete Mathematics", SM, "logic sets graphs combinatorics proofs", ["Mathematics"], True)
C(UG, "Classical Mechanics", SM, "newtonian lagrangian motion oscillations conservation laws", ["Physics", "Mathematics"], True)
C(UG, "Quantum Physics", SM, "wave functions operators schrodinger atoms quantum states", ["Classical Mechanics", "Linear Algebra"])
C(UG, "Numerical Methods", SM, "root finding interpolation numerical integration simulation", ["Calculus and Real Analysis", "Programming in Python"])

# ---- Postgraduate programs ----
P(PG, "MCA", CS, "advanced software development algorithms cloud systems", ["Data Structures and Algorithms", "Database Management Systems", "Operating Systems"])
P(PG, "M.Tech Computer Science", CS, "advanced algorithms distributed systems security research", ["Data Structures and Algorithms", "Operating Systems", "Computer Networks"])
P(PG, "M.Sc Data Science", DS, "machine learning deep learning big data statistical modelling", ["Machine Learning", "Statistics for Data Science", "Linear Algebra"])
P(PG, "M.Sc Statistics", DS, "statistical inference bayesian modelling experimental design", ["Probability Theory", "Statistics for Data Science"])
P(PG, "MBA", BC, "strategy finance marketing operations leadership", ["Organizational Behaviour", "Marketing Management", "Corporate Finance"])
P(PG, "M.Sc Mathematics", SM, "functional analysis topology differential equations", ["Calculus and Real Analysis", "Linear Algebra", "Discrete Mathematics"])
P(PG, "M.Sc Physics", SM, "quantum mechanics condensed matter electrodynamics", ["Classical Mechanics", "Quantum Physics"])
P(PG, "M.Tech Electronics", EN, "vlsi communication systems embedded design", ["Signals and Systems", "Embedded Systems"])
P(PG, "M.Tech Mechanical", EN, "advanced thermodynamics cfd robotics design", ["Thermodynamics", "Fluid Mechanics"])

# ---- Postgraduate courses ----
C(PG, "Deep Learning", DS, "neural networks backpropagation convolutional recurrent transformers training", ["Machine Learning", "Linear Algebra"])
C(PG, "Natural Language Processing", DS, "text language models tokenization embeddings translation chatbots", ["Machine Learning", "Programming in Python"])
C(PG, "Computer Vision", DS, "image recognition detection segmentation convolutional networks", ["Machine Learning", "Linear Algebra"])
C(PG, "Reinforcement Learning", DS, "agents rewards policies decision making simulation", ["Machine Learning", "Probability Theory"])
C(PG, "Big Data Analytics", DS, "spark hadoop distributed data processing large scale analytics", ["Database Management Systems", "Data Mining"])
C(PG, "MLOps and Model Deployment", DS, "deployment pipelines monitoring containers production machine learning", ["Machine Learning", "Cloud Computing"])
C(PG, "Statistical Inference", DS, "estimation likelihood bayesian testing asymptotics", ["Probability Theory", "Statistics for Data Science"])
C(PG, "Advanced Algorithms", CS, "approximation randomized algorithms graph optimization complexity", ["Data Structures and Algorithms", "Discrete Mathematics"])
C(PG, "Distributed Systems", CS, "consensus replication fault tolerance microservices scalability", ["Operating Systems", "Computer Networks"])
C(PG, "Information Security and Cryptography", CS, "cryptography protocols secure systems threat modelling", ["Cybersecurity Fundamentals", "Discrete Mathematics"])
C(PG, "Advanced Business Analytics", BC, "forecasting optimisation machine learning decision analytics", ["Business Analytics", "Machine Learning"])
C(PG, "Strategic Management", BC, "competitive strategy corporate strategy leadership innovation", ["Organizational Behaviour", "Marketing Management"])
C(PG, "Financial Management", BC, "portfolio risk derivatives valuation corporate finance", ["Corporate Finance"])
C(PG, "Supply Chain Management", BC, "logistics procurement inventory optimisation global operations", ["Operations Management"])
C(PG, "VLSI Design", EN, "chip design cmos fabrication digital integrated circuits", ["Digital Electronics", "Embedded Systems"])
C(PG, "Robotics and Automation", EN, "robots sensors actuators control motion planning", ["Control Systems", "Embedded Systems"])
C(PG, "Computational Fluid Dynamics", EN, "numerical simulation fluid flow meshes solvers", ["Fluid Mechanics", "Numerical Methods"])
C(PG, "Quantum Computing", SM, "qubits quantum gates algorithms entanglement", ["Quantum Physics", "Linear Algebra"])
C(PG, "Functional Analysis", SM, "banach hilbert spaces operators topology", ["Calculus and Real Analysis", "Linear Algebra"])

CAREERS = {
    CS: (["Software Developer", "Backend or Cloud Engineer", "Cybersecurity Analyst", "Systems Architect"],
         ["Data structures and system design", "Cloud and DevOps tools", "Secure coding", "Version control and testing"]),
    DS: (["Data Analyst", "Machine Learning Engineer", "Data Scientist", "AI Researcher"],
         ["Python and SQL", "Statistics and ML modelling", "Deep learning frameworks", "MLOps and deployment"]),
    BC: (["Business Analyst", "Financial Analyst", "Marketing Manager", "Operations Manager"],
         ["Financial modelling", "Data-driven decision making", "Communication and leadership", "Spreadsheet and BI tools"]),
    EN: (["Electronics Engineer", "Embedded Systems Engineer", "Mechanical Design Engineer", "Automation Engineer"],
         ["CAD and simulation tools", "Embedded programming", "Control and circuit design", "Technical documentation"]),
    SM: (["Research Scientist", "Quantitative Analyst", "Actuary", "Lecturer or Academic"],
         ["Mathematical modelling", "Scientific programming", "Technical writing", "Statistical analysis"]),
}

SPECIALISATIONS = {
    CS: ["PhD in systems or security", "Research in distributed computing", "Industry research labs"],
    DS: ["PhD in machine learning", "Applied research in NLP or computer vision", "Industry AI research labs"],
    BC: ["PhD in finance or management", "Professional certifications (CFA, CMA)", "Entrepreneurship and consulting"],
    EN: ["PhD in embedded or VLSI systems", "Research in robotics and automation", "R&D roles in industry"],
    SM: ["PhD in mathematics or physics", "Research in quantum information", "Academic and research institutes"],
}


def build_catalog():
    return pd.DataFrame(_ROWS)
