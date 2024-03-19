import streamlit as st
import os
import json
from streamlit.script_run_context import add_script_run_ctx

# Use session ID as file name for individual state management
state = add_script_run_ctx().streamlit_script_run_ctx.session_id + '.json'

# Initialize chat history for the current user session
if not os.path.isfile(state):
    with open(state, 'w') as f:
        json.dump({'messages': []}, f)

# Load messages for the current user session
with open(state) as f:
    messages = json.load(f)['messages']

# Display chat messages
for message in messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    messages.append({"role": "user", "content": prompt})
    with open(state, 'w') as f:
        json.dump({'messages': messages}, f)

    # Here, you would also add logic to update the database and notify other users
