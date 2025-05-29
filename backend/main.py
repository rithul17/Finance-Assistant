from fastapi import FastAPI, UploadFile, File
import whisper
import shutil
import os
import base64
from fastapi.responses import JSONResponse
import edge_tts
import sys

#to import from agents 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.crew import CrewAgent
from fastapi.middleware.cors import CORSMiddleware

#function to use tts
async def tts_to_file(text: str, file_path: str, speed: float = 1.0, voice: str = "en-US-GuyNeural"):
    rate_percent = int((speed - 1.0) * 100)
    rate = f"+{rate_percent}%" if rate_percent > 0 else f"{rate_percent}%"
    
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(file_path)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-streamlit-app.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Initializing
@app.on_event("startup")
async def startup_event():
    global whisper_model, crew_agent

    st_msg = "Loading Whisper model..."
    print(st_msg)
    whisper_model = whisper.load_model("base")
    print("Whisper loaded.")


    print("Initializing CrewAI agent...")
    crew_agent = CrewAgent()  
    print("CrewAI agent ready.")


#main endpoint
@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):

    temp_audio_path = "temp_input.wav"
    with open(temp_audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #stt
    result = whisper_model.transcribe(temp_audio_path)
    transcribed_text = result.get("text", "")
    print(f"Transcribed text: {transcribed_text}")

    crew_response = crew_agent.crew().kickoff(inputs={"input_text":transcribed_text})
    print(f"CrewAI response: {crew_response}")

    final_text = crew_response
    #convert crew response object to string.
    final_text = str(final_text)

    #tts
    output_audio_path = "output_audio.wav"
    await tts_to_file(text=final_text, file_path=output_audio_path, speed=1.2)
    print("Audio synthesis complete.")

    with open(output_audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    os.remove(output_audio_path)
    os.remove(temp_audio_path)

    return JSONResponse(content={
        "audio_base64": audio_b64,
        "final_text": final_text
        })


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "financial-analysis-backend"}
