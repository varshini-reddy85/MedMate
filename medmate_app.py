import streamlit as st
from datetime import datetime, date
import time
import threading
from plyer import notification
import pyttsx3

st.set_page_config(page_title="MedMate - Medicine Reminder", layout="centered")

# 🔊 Speak Function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 🔁 Background Reminder Checker
def check_reminders():
    while True:
        now = datetime.now().replace(second=0, microsecond=0)
        for reminder in st.session_state.reminders:
            if reminder["time"] == now and not reminder.get("notified", False):
                notification.notify(
                    title="💊 Medicine Reminder",
                    message=f"Time to take {reminder['medicine']} - {reminder['dosage']}",
                    timeout=10
                )
                speak(f"Time to take your medicine: {reminder['medicine']}")
                reminder["notified"] = True
        time.sleep(30)

# ✅ Start reminder thread once
if "reminders" not in st.session_state:
    st.session_state.reminders = []
if "reminder_thread_started" not in st.session_state:
    threading.Thread(target=check_reminders, daemon=True).start()
    st.session_state.reminder_thread_started = True

# 📝 Title
st.title("💊 MedMate: Personal Medicine Reminder")
st.markdown("### 📥 Add New Reminder")

# 🧾 Input Form
with st.form("reminder_form"):
    med_name = st.text_input("Enter Medicine Name:")
    dosage = st.text_input("Enter Dosage (e.g., 1 tablet):")
    reminder_time = st.time_input("Set Reminder Time:")
    uploaded_image = st.file_uploader("Upload Medicine Image", type=["jpg", "png"])
    captured_image = st.camera_input("Or Take a Photo")
    submit = st.form_submit_button("Add Reminder")

# ➕ Save Reminder
if submit:
    reminder_datetime = datetime.combine(date.today(), reminder_time)
    image_data = uploaded_image if uploaded_image else captured_image
    reminder = {
        "medicine": med_name,
        "dosage": dosage,
        "time": reminder_datetime,
        "image": image_data,
    }
    st.session_state.reminders.append(reminder)
    st.success(f"✅ Reminder saved for **{med_name}** at {reminder_time.strftime('%I:%M %p')}")

# 📋 Display Active Reminders
st.subheader("🗓️ Active Reminders")
if st.session_state.reminders:
    for i, reminder in enumerate(st.session_state.reminders):
        with st.expander(f"{reminder['medicine']} - {reminder['time'].strftime('%I:%M %p')}"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Medicine:** {reminder['medicine']}")
                st.markdown(f"**Dosage:** {reminder['dosage']}")
                st.markdown(f"**Time:** {reminder['time'].strftime('%I:%M %p')}")
            with col2:
                if reminder["image"]:
                    st.image(reminder["image"], caption="Medicine Image", width=100)
            if st.button("❌ Delete Reminder", key=f"del_{i}"):
                st.session_state.reminders.pop(i)
                st.experimental_rerun()
else:
    st.info("No reminders added yet.")

# 📢 Footer
st.markdown("---")
st.caption("🧠 Built with ❤️ using Streamlit • Developed by Varshini")
