import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Custom styling
# -----------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">🤖 AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your intelligent AI chatbot</div>',
    unsafe_allow_html=True
)

# -----------------------------
# API key check
# -----------------------------
if not api_key:
    st.error(
        "Gemini API key was not found. "
        "Please check your .env file or Streamlit Secrets."
    )
    st.stop()

# -----------------------------
# Conversation memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("🤖 AI Assistant")

    st.write(
        "Ask questions, get explanations, "
        "brainstorm ideas, generate content, "
        "or search for current information."
    )

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # Suggested questions
    st.subheader("💡 Try asking")

    suggestions = [
        "What is artificial intelligence?",
        "Explain machine learning in simple words.",
        "What are the latest technology trends?",
        "What are today's major news headlines?",
        "Give me some project ideas."
    ]

    for question in suggestions:
        if st.button(question, use_container_width=True):
            st.session_state.pending_question = question

# -----------------------------
# Display previous messages
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
user_message = st.chat_input(
    "Ask me anything..."
)

# Check suggested question
if "pending_question" in st.session_state:

    user_message = st.session_state.pending_question

    del st.session_state.pending_question

# -----------------------------
# Process user message
# -----------------------------
if user_message:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    try:

        # Create Gemini client
        client = genai.Client(api_key=api_key)

        # Build conversation history
        conversation = []

        for message in st.session_state.messages:

            role = (
                "User"
                if message["role"] == "user"
                else "Assistant"
            )

            conversation.append(
                f"{role}: {message['content']}"
            )

        conversation_text = "\n\n".join(conversation)

        # Google Search grounding tool
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

        # Generate response
        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=f"""
You are a helpful, intelligent and friendly AI assistant.

You can answer general questions, explain concepts,
help with writing, brainstorming, learning, coding,
problem solving and everyday conversations.

You also have access to Google Search.

When the user's question requires current or
time-sensitive information, such as:

- latest news
- current events
- politics
- elections
- current political leaders
- recent developments
- current technology trends
- recent sports results
- current prices
- recent announcements
- today's information
- this week's information

use Google Search to obtain up-to-date information.

For questions that do not require current information,
answer normally using your knowledge.

When using current information, clearly distinguish
reported facts from opinions or analysis and prefer
reliable sources.

Use the previous conversation to understand
follow-up questions such as "it", "its", "they",
"them", "this", and "that".

Previous conversation:

{conversation_text}

Answer the user's latest question.
""",

            config=types.GenerateContentConfig(
                tools=[grounding_tool]
            )
        )

        answer = response.text

        # Display answer
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Save answer
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "🤖 AI Assistant | Powered by Google Gemini + Google Search"
)
