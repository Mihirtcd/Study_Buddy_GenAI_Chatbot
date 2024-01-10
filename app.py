# from openai import OpenAI
# import streamlit as st
# from dotenv import load_dotenv
# import os
# import shelve

# load_dotenv()

# st.title("Streamlit Chatbot Interface")

# USER_AVATAR = "👤"
# BOT_AVATAR = "🤖"
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Ensure openai_model is initialized in session state
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"


# # Load chat history from shelve file
# def load_chat_history():
#     with shelve.open("chat_history") as db:
#         return db.get("messages", [])


# # Save chat history to shelve file
# def save_chat_history(messages):
#     with shelve.open("chat_history") as db:
#         db["messages"] = messages


# # Initialize or load chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = load_chat_history()

# # Sidebar with a button to delete chat history
# with st.sidebar:
#     if st.button("Delete Chat History"):
#         st.session_state.messages = []
#         save_chat_history([])

# # Display chat messages
# for message in st.session_state.messages:
#     avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
#     with st.chat_message(message["role"], avatar=avatar):
#         st.markdown(message["content"])

# # Main chat interface
# if prompt := st.chat_input("How can I help?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user", avatar=USER_AVATAR):
#         st.markdown(prompt)

#     with st.chat_message("assistant", avatar=BOT_AVATAR):
#         message_placeholder = st.empty()
#         full_response = ""
#         for response in client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=st.session_state["messages"],
#             stream=True,
#         ):
#             full_response += response.choices[0].delta.content or ""
#             message_placeholder.markdown(full_response + "|")
#         message_placeholder.markdown(full_response)
#     st.session_state.messages.append({"role": "assistant", "content": full_response})

# # Save chat history after each interaction
# save_chat_history(st.session_state.messages)
import openai
import json
import streamlit as st
from dotenv import load_dotenv
import os
import shelve

load_dotenv()

st.title("Streamlit Chatbot Interface")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure openai_model is initialized in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Main chat interface
# if prompt := st.chat_input("How can I help?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user", avatar=USER_AVATAR):
#         st.markdown(prompt)

#     with st.chat_message("assistant", avatar=BOT_AVATAR):
#         message_placeholder = st.empty()
#         full_response = ""
#         # for response in openai.Completion.create(
#         #     model=st.session_state["openai_model"],
#         #     prompt=prompt,
#         #     max_tokens=150
#         # ):
#     #     for response in openai.ChatCompletion.create(
#     #         model=st.session_state["openai_model"],
#     #         messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
#     #     ):
#     # # Your processing code

#     #         full_response += response.choices[0].text.strip()
#     #         message_placeholder.markdown(full_response)
#     #     st.session_state.messages.append({"role": "assistant", "content": full_response})
#         # for response in openai.ChatCompletion.create(
#         #     model=st.session_state["openai_model"],
#         #     messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
#         #     ):
#         #     if 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0]:
#         #         full_response += response['choices'][0]['message']['content']
#         #     else:
#         #         # Handle cases where the response structure is different or missing expected fields
#         #         full_response += "Error: Unexpected response format."

#         #     message_placeholder.markdown(full_response)
#         for response in openai.ChatCompletion.create(
#             model=st.session_state["openai_model"],
#             messages=[{"role": "user", "content": prompt}]
#             ):
#             # Extract the message from the response
#             if response is not None and hasattr(response, 'choices') and len(response.choices) > 0:
#                 full_response += response.choices[0].message['content']
#             else:
#                 # Handle cases where the response is not as expected
#                 full_response += "Error: Unexpected response format."

#             message_placeholder.markdown(full_response)
# if prompt := st.chat_input("How can I help?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user", avatar=USER_AVATAR):
#         st.markdown(prompt)

#     with st.chat_message("assistant", avatar=BOT_AVATAR):
#         message_placeholder = st.empty()
#         full_response = ""

#         try:
#             # Call to OpenAI's ChatCompletion
#             response = openai.ChatCompletion.create(
#                 model=st.session_state["openai_model"],
#                 messages=[{"role": "user", "content": prompt}]
#             )

#             # Extracting the response content
#             if response.choices and len(response.choices) > 0:
#                 for message in response.choices[0].message:
#                     full_response += message['content'] + "\n"

#         except Exception as e:
#             full_response = f"Error: {str(e)}"

#         message_placeholder.markdown(full_response)
#         st.session_state.messages.append({"role": "assistant", "content": full_response})
# if prompt := st.chat_input("How can I help?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user", avatar=USER_AVATAR):
#         st.markdown(prompt)

#     with st.chat_message("assistant", avatar=BOT_AVATAR):
#         message_placeholder = st.empty()
#         full_response = ""

#         try:
#             # Call to OpenAI's ChatCompletion
#             response = openai.ChatCompletion.create(
#                 model=st.session_state["openai_model"],
#                 messages=[{"role": "user", "content": prompt}]
#             )

#             # Debugging: Print the entire response
#             print(json.dumps(response, indent=2))

#             # Check if response is structured as expected
#             if 'choices' in response and len(response['choices']) > 0:
#                 messages = response['choices'][0].get('message', {})
#                 if isinstance(messages, list):
#                     for message in messages:
#                         full_response += message.get('content', '') + "\n"
#                 else:
#                     full_response = "Unexpected message format in response."

#         except Exception as e:
#             full_response = f"Error: {str(e)}"

#         message_placeholder.markdown(full_response)
#         st.session_state.messages.append({"role": "assistant", "content": full_response})
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Call to OpenAI's ChatCompletion
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[{"role": "user", "content": prompt}]
            )

            # Parsing the response
            if 'choices' in response and len(response['choices']) > 0:
                assistant_message = response['choices'][0]['message']
                if 'content' in assistant_message:
                    full_response = assistant_message['content']
                else:
                    full_response = "Error: Content missing in response."
            else:
                full_response = "Error: Invalid response format."

        except Exception as e:
            full_response = f"Error: {str(e)}"

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# Save chat history after each interaction
save_chat_history(st.session_state.messages)

