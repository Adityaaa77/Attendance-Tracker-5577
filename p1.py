import streamlit as st
import pyrebase
import random

# 🎨 Random background color
def set_random_bg_color():
    colors = ["#FFDEE9", "#B5FFFC", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#A0C4FF", "#FFC6FF"]
    selected = random.choice(colors)
    st.markdown(f"<style>body {{background-color: {selected};}}</style>", unsafe_allow_html=True)

set_random_bg_color()
st.title("📚 Attendance Tracker App")

# 🔥 Firebase Config
firebase_config = {
    "apiKey": "AIzaSyD_rM1h0KGwEfNNZud5isKJ-yR99P1DKww",
    "authDomain": "attendance-tracker-8d858.firebaseapp.com",
    "databaseURL": "https://attendance-tracker-8d858-default-rtdb.firebaseio.com/",
    "projectId": "attendance-tracker-8d858",
    "storageBucket": "attendance-tracker-8d858.appspot.com",
    "messagingSenderId": "515015641247",
    "appId": "1:515015641247:web:9f44ae28a7f9801228faaa"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# 🧠 Ask for username
user = st.text_input("👤 Enter your name to continue")

if not user:
    st.warning("Please enter your name to access your data.")
    st.stop()

# 🔁 Load user data from Firebase
def load_user_data(user):
    data = db.child(user).get().val()
    return data if data else {}

# 💾 Save user data to Firebase
def save_user_data(user, data):
    db.child(user).set(data)

if "subjects" not in st.session_state:
    st.session_state.subjects = load_user_data(user)

# ➕ Add Subject
with st.form("add_form"):
    subject = st.text_input("📘 New Subject")
    submitted = st.form_submit_button("Add Subject")
    if submitted:
        if subject:
            subjects = st.session_state.subjects
            if subject not in subjects:
                subjects[subject] = {"present": 0, "absent": 0}
                save_user_data(user, subjects)
                st.success(f"✅ Added subject '{subject}'")
            else:
                st.warning("⚠️ Subject already exists.")
        else:
            st.error("Please enter a subject name.")

# 📋 Display Subjects & Attendance
subs = st.session_state.subjects
if subs:
    for subject, data in subs.items():
        st.subheader(f"📘 {subject}")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Present", key=f"present_{subject}"):
                subs[subject]["present"] += 1
        with col2:
            if st.button("❌ Absent", key=f"absent_{subject}"):
                subs[subject]["absent"] += 1
        with col3:
            if st.button("🗑️ Delete Subject", key=f"del_{subject}"):
                del subs[subject]
                save_user_data(user, subs)
                st.experimental_rerun()

        present = data["present"]
        absent = data["absent"]
        total = present + absent
        percentage = (present / total) * 100 if total > 0 else 0

        st.info(f"✅ Present: {present}, ❌ Absent: {absent}, 📊 Percentage: {percentage:.2f}%")
        st.progress(int(percentage))

        if st.button("🔁 Reset Attendance", key=f"reset_{subject}"):
            subs[subject] = {"present": 0, "absent": 0}
            save_user_data(user, subs)
            st.experimental_rerun()

        st.markdown("---")

    save_user_data(user, subs)
else:
    st.info("No subjects added yet. Start by adding one!")

st.caption("✨ Made with 💖 by Adii Darling")
