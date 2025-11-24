import os
import random
import speech_recognition as sr
from google.cloud import texttospeech, speech
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
import google.generativeai as genai
import pyaudio
import wave
from google.cloud import speech
from google.cloud import texttospeech

RATE = 16000
CHUNK = int(RATE / 10)

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

conversation_history = ""
current_role = ""

acknowledgements = [
    "Thanks for explaining that.",
    "Great, I appreciate the clarity.",
    "Got it, thank you.",
    "Nice, that makes sense.",
    "Understood, thanks for sharing.",
]


# ---------- GOOGLE CLOUD TEXT TO SPEECH ---------- #
def speak(text):
    print("\nInterviewer:", text)

    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000,
                    output=True)
    stream.write(response.audio_content)
    stream.stop_stream()
    stream.close()
    p.terminate()



# ---------- GOOGLE CLOUD SPEECH TO TEXT ---------- #
def listen():
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        single_utterance=True,
    )

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1,
                      rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("\n🎤 Start speaking now...")

    requests = (speech.StreamingRecognizeRequest(audio_content=stream.read(CHUNK))
                for _ in range(int(RATE / CHUNK * 6)))  # 6 seconds limit

    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            if result.is_final:
                text = result.alternatives[0].transcript
                print("You (voice):", text)
                stream.stop_stream()
                stream.close()
                mic.terminate()
                return text


# ---------- ROLE SELECTION ---------- #
def choose_role():
    global current_role

    print("\nSelect interview type:")
    print("1. Software Development Engineer (SDE)")
    print("2. Data Analyst")
    print("3. Sales / Business Development")

    choice = input("\nEnter choice (1/2/3): ")

    if choice == "1":
        current_role = "SDE"
    elif choice == "2":
        current_role = "Analyst"
    elif choice == "3":
        current_role = "Sales"
    else:
        print("Invalid choice. Try again.")
        return choose_role()

    print(f"\nStarting {current_role} voice interview...\n")
    return current_role


# ---------- GEMINI INTERVIEW GENERATION ---------- #
def ask_gemini(history, user_input):
    acknowledgement = random.choice(acknowledgements)

    prompt = f"""
You are an experiencaed Senior Software Engineering Interviewer conducting a realistic mock interview for a {current_role} position.

GOAL:
Behave like a real human interviewer with natural, adaptive conversation flow and deep technical reasoning. Ask easy to medium conceptual and engineering questions and dig into skills and areas the candidate claims expertise in.

CONVERSATION RULES:
- Sound human, friendly, and conversational — never robotic, repetitive, or templated.
- Start each turn by briefly acknowledging the candidate’s last response (one short sentence only).
- Ask ONE question at a time.
- Ask intelligent, context-aware follow-up questions based on what the candidate actually says, not generic "provide an example" phrasing.
- Do NOT repeatedly ask for examples unless needed.
- Do NOT tutor or explain answers — redirect if they request help.
- If the candidate gives a vague answer, ask a specific probing question instead of generic clarification.

TECHNICAL DEPTH EXPECTATION:
If the candidate mentions a technology, immediately ask conceptual question related to it. For example:
- C++ / Java / Python → some basic concepts, memory management, concurrency, compilation, performance tuning, multithreading
- DSA → some basic concepts, reasoning approach, complexity analysis, edge cases, alternative strategies
- DBMS / SQL → indexing, transactions, ACID, isolation levels, query optimization
- OS → scheduling, deadlocks, paging, synchronization primitives
- Networks → TCP vs UDP, congestion control, DNS, load balancing
- OOP → SOLID principles, polymorphism decisions, object design critique
- System Design → requirements, bottlenecks, scaling decisions, trade-offs, capacity planning
- Frontend → rendering pipelines, state mgmt, API aggregation, performance optimization
- Backend → microservices, message queues, caching, distributed system challenges

PROJECT DEEP-DIVE RULES:
Ask questions about:
- Key architecture decisions and reasons behind them
- Scaling strategies and performance measurement
- Trade-offs considered
- Debugging incidents and root cause analysis
- Testing & devops processes

BEHAVIORAL SECTION:
Ask STAR-based questions requiring analytical thinking about teamwork, conflict, failure, resilience.

INTERVIEW STRUCTURE:
1. Background & intro
2. Project deep dive
3. Skill-based deep technical questioning
4. System design scenario
5. Behavioral question
6. Summary evaluation after 8–10 answers when user types "feedback"

IMPORTANT:
- NEVER answer your own questions.
- NEVER say "as an AI model".
- NEVER provide definitions unless explicitly asked.
- Speak like a seasoned engineering leader assessing capability.

CONTEXT FOR NEXT TURN:
Conversation so far:
{history}

Candidate just said: "{user_input}"

Respond ONLY with the next interviewer message.
Do not produce explanations, definitions, or multi-question responses.
"""

    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()


def generate_evaluation(history):
    prompt = f"""
Act as a supportive hiring manager. Write a feedback summary including:
- Score out of 10
- Strengths (bullet list)
- Areas to improve (bullet list)
- Encouraging final message

Transcript:
{history}
"""
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()


# ---------- INTERVIEW FLOW ---------- #
def start_interview():
    global conversation_history

    role = choose_role()

    question = "Let's begin. Tell me about yourself."
    speak(question)

    rounds = 0

    while True:
        user_input = listen()

        if user_input.lower() in ["feedback", "evaluation", "summary"]:
            speak("Generating evaluation summary now.")
            print("\n" + generate_evaluation(conversation_history))
            break

        if user_input.lower() in ["exit", "quit", "bye", "stop"]:
            speak("Thank you for participating. You did well. Goodbye!")
            break

        conversation_history += f"\nCandidate: {user_input}\nInterviewer: {question}"

        question = ask_gemini(conversation_history, user_input)
        rounds += 1
        speak(question)

        if rounds >= 10:
            speak("Generating final evaluation summary now.")
            print("\n" + generate_evaluation(conversation_history))
            break


if __name__ == "__main__":
    start_interview()
