import streamlit as st
import os
from langfuse import Langfuse
from langfuse.decorators import observe

os.environ["GROQ_API_KEY"] = "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"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-14a6687b-b3e1-4d27-8823-6bd971e140f1"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-bdf91ecc-29ac-4447-bb73-6466eddb3643"
# 🇪🇺 EU region
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"


langfuse = Langfuse(
  secret_key="sk-lf-14a6687b-b3e1-4d27-8823-6bd971e140f1",
  public_key="pk-lf-bdf91ecc-29ac-4447-bb73-6466eddb3643",
  host="https://cloud.langfuse.com"
)



# Set page configuration
st.set_page_config(page_title="Chat Interface", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main interface
st.title("🌟 Interact with Yash Paddalwar")
st.write("Engage in a delightful chat experience!")

@observe()
def answer_llm(query):
    from groq import Groq
    import os

    client = Groq(
        api_key = os.environ['GROQ_API_KEY']
    )

    with open("info.txt","r") as file:
        info = file.read()

    with open("Prompts/main.txt") as file:
        prompt = file.read()

    prompt = prompt.replace("{info}",info)
    prompt = prompt.replace("{query}",query)


    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.07,
        max_tokens=1024,
        top_p=1,
        stop=None,
    )

    return completion.choices[0].message.content


# Clear Chat button
if st.button("🧹 Clear Chat"):
    # Clear chat history
    st.session_state.messages.clear()

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Append the user's message to chat history
    st.session_state.messages.append(("user", prompt))
    
    # Append the assistant's response to chat history
    with st.spinner("Yash is typing...."):
        response = answer_llm(prompt)  # Simple echo for now
        st.session_state.messages.append(("assistant", response))

# Display chat history
for msg_type, content in st.session_state.messages:
    if msg_type == "user":
        st.chat_message("user").write(content)
    elif msg_type == "assistant":
        st.chat_message("assistant").write(content)
