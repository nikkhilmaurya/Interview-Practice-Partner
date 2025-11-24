import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

conversation_history = ""
current_role = ""


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

    print(f"\nStarting {current_role} interview...\n")
    return current_role


def ask_gemini(history, user_input):
    prompt = f"""
You are an experiencaed Senior Software Engineering Interviewer conducting a realistic mock interview for a {current_role} position.

GOAL:
Beginner friendly question and Behave like a real human interviewer with natural, adaptive conversation flow and deep technical reasoning. Ask easy to medium conceptual and engineering questions and dig into skills and areas the candidate claims expertise in.
After asking 10 questions end the conversation by saying thank you for your time.
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
- OOP → some basic concepts, classes and objects, constructors, polymorphism decisions, object design critique
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


    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


def generate_evaluation(history):
    prompt = f"""
You are a senior recruiter evaluating a {current_role} candidate after a mock interview.

Transcript:
{history}

Write a final evaluation including:
- Score out of 10 with reasoning
- 2 strengths (after proper analysis)
- 2 improvements (after proper analysis)
- 1 short practice suggestion (after proper analysis)
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


def start_interview():
    global conversation_history

    role = choose_role()
    question = "Let's begin. Tell me about yourself."
    print("\nInterviewer:", question)

    rounds = 0

    while True:
        user_answer = input("\nYou: ")

        # User manually requests evaluation
        if user_answer.lower() in ["final evaluation", "evaluation", "summary"]:
            print("\nGenerating evaluation...\n")
            print(generate_evaluation(conversation_history))
            print("\nInterview complete. Thank you!")
            break

        if user_answer.lower() in ["exit", "quit", "bye"]:
            print("\nInterviewer: Thank you for participating. Goodbye!")
            break

        conversation_history += f"\nCandidate: {user_answer}\nInterviewer: {question}"
        question = ask_gemini(conversation_history, user_answer)
        rounds += 1

        print("\nInterviewer:", question)

        # Automatic evaluation after 10 rounds
        if rounds >= 10:
            print("\nInterviewer: Thank you for your time. The interview is now complete.")
            print("\nGenerating automatic evaluation...\n")
            print(generate_evaluation(conversation_history))
            print("\nInterview complete. Thank you!")
            break


if __name__ == "__main__":
    start_interview()
