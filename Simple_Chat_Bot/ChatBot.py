from groq import Groq
import streamlit as st
import time  # To control typing speed

st.title("ChatGPT-like Clone")

# Initialize the API client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Check if the model is loaded in session state
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-8b-8192"

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user query
if prompt := st.chat_input("What is up?"):
    # Add user message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant thinking and typing effect
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["groq_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )

        response = stream.choices[0].message.content  # Get the assistant's response
        response_placeholder = st.empty()  # Placeholder to dynamically update the message

        # "Typing" effect: gradually display each character
        typed_text = ""
        for char in response:
            typed_text += char
            response_placeholder.markdown(typed_text)
            time.sleep(0.005)  # Adjust typing speed (lower for faster, higher for slower)

    # Add the assistant's message to the session state
    st.session_state.messages.append({"role": "assistant", "content": response})
