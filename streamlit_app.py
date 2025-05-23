import streamlit as st
import requests
import time

API_BASE_URL = "http://localhost:8000"  # Your FastAPI base URL

st.set_page_config(page_title="Async Number Generator", layout="centered")
st.title("🎲 Random Number Generator using FastAPI + Celery")

# Input for count
count = st.number_input("Enter how many numbers to generate between(1-20):", value=5, step=1)


if st.button("🚀 Submit Task"):
    if not(count > 0 and count < 21):
        st.warning("⚠️ Random number will generate from 1 - 20 value. \n Please enter a value between 1 and 20.")
        st.stop()
    with st.spinner("Submitting task..."):
        try:
            # Send count as query param, not JSON
            response = requests.post(f"{API_BASE_URL}/submit/", params={"count": count})
            if response.status_code == 200:
                task_id = response.json().get("task_id")
                st.session_state.task_id = task_id
                st.success(f"✅ Task submitted! Task ID: {task_id}")
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Exception: {str(e)}")

# If task submitted
if "task_id" in st.session_state:
    task_id = st.session_state.task_id
    st.markdown(f"**Tracking Task ID:** `{task_id}`")
    progress_bar = st.progress(0)
    status_box = st.empty()
    result_box = st.empty()

    while True:
        try:
            res = requests.get(f"{API_BASE_URL}/result/{task_id}")
            data = res.json()
            status = data.get("status")

            if status == "PENDING":
                status_box.info("Status: PENDING")
            elif status == "PROGRESS":
                progress = data.get("progress", {})
                current = progress.get("current", 0)
                total = progress.get("total", 1)
                numbers = progress.get("numbers", [])
                percent = int((current / total) * 100)
                progress_bar.progress(percent)
                status_box.info(f"Progress: {current}/{total}")
                result_box.write(f"Generated so far: {numbers}")
            elif status == "SUCCESS":
                result = data.get("result", {})
                numbers = result.get("numbers", [])
                status_box.success("✅ Task Completed!")
                result_box.write(f"🎉 Final Numbers: {numbers}")
                progress_bar.empty()
                del st.session_state.task_id
                break
            elif status == "FAILURE":
                status_box.error("❌ Task Failed!")
                del st.session_state.task_id
                break
            else:
                status_box.info(f"Status: {status}")
        except Exception as e:
            status_box.error(f"Error: {str(e)}")
            break

        time.sleep(5)
