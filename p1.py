import streamlit as st
import pyrebase
import random

# 🔥 Firebase Configuration (replace with your actual project values if needed)
firebaseConfig = {
    "apiKey": "AIzaSyD_rM1h0KGwEfNNZud5isKJ-yR99P1DKww",
    "authDomain": "attendance-tracker-8d858.firebaseapp.com",
    "databaseURL": "https://attendance-tracker-8d858-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "attendance-tracker-8d858.appspot.com"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# 🎨 Random Background Color
def set_random_bg_color():
    colors = ["#FFDEE9", "#B5FFFC", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#A0C4FF", "#FFC6FF"]
    selected = random.choice(colors)
    st.markdown(f"<style>body {{background-color: {selected};}}</style>", unsafe_allow_html=True)

set_random_bg_color()
st.title("📚 Attendance Tracker (Firebase Edition)")

# 🧠 User Input (Session)
user = st.text_input("👤 Enter your name to continue:")

# 🔁 Load data from Firebase
def load_user_data(user):
    try:
        if user:
            data = db.child(user).get().val()
            return data if data else {}
        return {}
    except Exception as e:
        st.error(f"Firebase Load Error: {e}")
        return {}

# 💾 Save data to Firebase
def save_user_data(user, data):
    try:
        db.child(user).set(data)
    except Exception as e:
        st.error(f"Firebase Save Error: {e}")

# 🧠 Load to session
if user:
    if "subjects" not in st.session_state:
        st.session_state.subjects = load_user_data(user)

    # ➕ Add New Subject
    with st.form("add_subject"):
        new_subject = st.text_input("➕ Add New Subject")
        add = st.form_submit_button("Add")
        if add and new_subject:
            subs = st.session_state.subjects
            if new_subject not in subs:
                subs[new_subject] = {"present": 0, "absent": 0}
                save_user_data(user, subs)
                st.success(f"Subject '{new_subject}' added!")
            else:
                st.warning("Subject already exists!")

    # 📋 Attendance Controls
    subs = st.session_state.subjects
    if subs:
        for subject in list(subs.keys()):
            st.subheader(f"📘 {subject}")
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

            with col1:
                if st.button("✅ Present", key=f"present_{subject}"):
                    subs[subject]["present"] += 1

            with col2:
                if st.button("❌ Absent", key=f"absent_{subject}"):
                    subs[subject]["absent"] += 1

            with col3:
                if st.button("🗑️ Delete Subject", key=f"delete_{subject}"):
                    del subs[subject]
                    save_user_data(user, subs)
                    st.experimental_rerun()

            with col4:
                if st.button("🔁 Reset", key=f"reset_{subject}"):
                    subs[subject] = {"present": 0, "absent": 0}

            # 📊 Attendance Stats
            present = subs[subject]["present"]
            absent = subs[subject]["absent"]
            total = present + absent
            percentage = (present / total * 100) if total > 0 else 0
            st.info(f"✅ Present: {present} | ❌ Absent: {absent} | 📈 Percentage: {percentage:.2f}%")
            st.progress(int(percentage))
            st.markdown("---")

        # 💾 Save on any change
        save_user_data(user, subs)
    else:
        st.info("Add a subject to begin tracking attendance!")

    st.caption("✨ App by Aditya Rajpal, powered by Firebase ☁️")
else:
    st.warning("Please enter your name to start tracking attendance.")
