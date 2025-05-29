import streamlit as st
import requests
import base64
from io import BytesIO

st.title("Agentic Finance Assistant")
st.set_page_config(page_title="Financial Analysis", page_icon="📈")

audio_file = st.audio_input("Record your market briefing")

if audio_file is not None:
    st.write("Processing your audio...")
    files = {"file": ("recording.wav", audio_file, "audio/wav")}

    try:
        response = requests.post("http://localhost:8000/process_audio", files=files)
    except Exception as e:
        st.error(f"Failed to connect to the backend: {e}")
    else:
        if response.status_code == 200:
            st.success("Audio processed successfully!")
            data = response.json()
            st.subheader("AI Summary:")
            st.write(data["final_text"])

            # Decode and play audio
            audio_bytes = base64.b64decode(data["audio_base64"])
            st.audio(BytesIO(audio_bytes), format="audio/wav")
        else:
            st.error("API Key rate limit exceeded, please try cloning the project locally and using your api key.")


