import streamlit as st
import PyPDF2
import re

# ---------------- PAGE ----------------
st.set_page_config(page_title="Smart Career AI Pro", layout="wide")

st.markdown("""
<style>
.title {
    text-align:center;
    font-size:40px;
    font-weight:800;
    color:#00ffcc;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚀 Smart Career AI Advisor</div>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("📌 Career Preferences")

sector = st.sidebar.selectbox(
    "Select Sector",
    ["IT", "Data Science", "Finance", "Marketing", "HR", "Design"]
)

experience = st.sidebar.selectbox(
    "Experience Level",
    ["Fresher", "Junior", "Mid", "Senior"]
)

preferred_city = st.sidebar.selectbox(
    "Preferred City",
    ["Any", "Bangalore", "Hyderabad", "Pune", "Chennai", "Mumbai", "Delhi"]
)

work_mode = st.sidebar.selectbox(
    "Work Mode",
    ["All", "Remote", "Hybrid", "Office"]
)

office_only = st.sidebar.checkbox("Show Only Office Jobs")

file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ---------------- DATABASE ----------------
skills_db = {
    "IT": ["python", "java", "sql", "aws"],
    "Data Science": ["python", "machine learning", "sql", "pandas"],
    "Finance": ["excel", "finance", "accounting"],
    "Marketing": ["seo", "ads", "branding"],
    "HR": ["recruitment", "communication"],
    "Design": ["figma", "ui", "ux"]
}

job_data = {
    "IT": {
        "Remote": ["Frontend Developer", "Backend Developer"],
        "Hybrid": ["Software Engineer", "DevOps Engineer"],
        "Office": ["System Engineer", "Network Engineer"],
        "locations": ["Bangalore", "Hyderabad", "Pune", "Chennai"]
    },
    "Data Science": {
        "Remote": ["Data Analyst", "ML Engineer"],
        "Hybrid": ["Data Scientist"],
        "Office": ["BI Analyst"],
        "locations": ["Bangalore", "Hyderabad", "Mumbai"]
    },
    "Finance": {
        "Remote": ["Financial Analyst"],
        "Hybrid": ["Accountant"],
        "Office": ["Bank Officer"],
        "locations": ["Mumbai", "Delhi", "Bangalore"]
    },
    "Marketing": {
        "Remote": ["SEO Analyst"],
        "Hybrid": ["Digital Marketer"],
        "Office": ["Brand Manager"],
        "locations": ["Mumbai", "Delhi", "Bangalore"]
    },
    "HR": {
        "Remote": ["HR Assistant"],
        "Hybrid": ["HR Executive"],
        "Office": ["Recruiter"],
        "locations": ["Bangalore", "Hyderabad", "Gurgaon"]
    },
    "Design": {
        "Remote": ["UI Designer"],
        "Hybrid": ["UX Designer"],
        "Office": ["Graphic Designer"],
        "locations": ["Bangalore", "Pune", "Remote"]
    }
}

salary_map = {
    "IT": (400000, 2500000),
    "Data Science": (500000, 3000000),
    "Finance": (350000, 1500000),
    "Marketing": (300000, 1200000),
    "HR": (250000, 1000000),
    "Design": (300000, 1500000)
}

# ---------------- PDF ----------------
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.lower()

def extract_skills(text, sector):
    found = []
    for skill in skills_db[sector]:
        if re.search(r"\b" + skill + r"\b", text):
            found.append(skill)
    return set(found)

# ---------------- MAIN ----------------
if file:

    resume_text = extract_text(file)

    user_skills = extract_skills(resume_text, sector)
    required_skills = set(skills_db[sector])

    matched = user_skills & required_skills
    missing = required_skills - user_skills

    score = (len(matched) / len(required_skills)) * 100

    # ---------------- DASHBOARD CARDS ----------------
    st.markdown("## 📊 Career Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background:#0f172a;padding:20px;border-radius:15px;text-align:center;color:#00ffcc;">
            <h3>🎯 Match Score</h3>
            <h2>{score:.2f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:#0f172a;padding:20px;border-radius:15px;text-align:center;color:white;">
            <h3>✅ Matched Skills</h3>
            <h2>{len(matched)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background:#0f172a;padding:20px;border-radius:15px;text-align:center;color:#ff4b4b;">
            <h3>❌ Missing Skills</h3>
            <h2>{len(missing)}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.progress(int(score))

    # ---------------- SALARY ----------------
    min_sal, max_sal = salary_map[sector]
    predicted = int(min_sal + (max_sal - min_sal) * (score / 100))

    st.markdown("## 💰 Salary Prediction")
    st.info(f"Range (PA): ₹{min_sal:,} - ₹{max_sal:,}")
    st.success(f"Predicted Salary (PA): ₹{predicted:,}")
    st.write(f"Monthly: ₹{predicted // 12:,}/month")

    # ---------------- JOBS (CITY WISE) ----------------
    st.markdown("## 💼 Job Recommendations (City-wise)")

    selected_jobs = job_data[sector][work_mode] if work_mode != "All" else (
        job_data[sector]["Remote"]
        + job_data[sector]["Hybrid"]
        + job_data[sector]["Office"]
    )

    if office_only:
        selected_jobs = job_data[sector]["Office"]

    for city in job_data[sector]["locations"]:
        with st.expander(f"📍 {city} Jobs"):
            for job in selected_jobs:
                st.write("👉", job)

    # ---------------- INSIGHTS ----------------
    st.markdown("## 🧠 Career Insight")

    if score < 40:
        st.error("Weak profile - needs improvement")
    elif score < 70:
        st.warning("Medium profile - improve skills")
    else:
        st.success("Strong profile - job ready")

    st.markdown("## 🚀 AI Insights")
    st.write("Interview Readiness:", f"{max(0, score - 10):.0f}%")
    st.write("Job Match Confidence:", f"{min(95, score + 8):.0f}%") 