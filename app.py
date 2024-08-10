# import openai
# import streamlit as st
# from dotenv import load_dotenv
# import os
# import shelve

# # Load environment variables
# load_dotenv()

# # Set the title of the Streamlit app
# st.title("Streamlit Chatbot Interface")

# # Define avatars for user and bot
# USER_AVATAR = "👤"
# BOT_AVATAR = "🤖"

# # Set OpenAI API key from .env file
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Ensure the model is initialized in the session state
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# # Function to load chat history
# def load_chat_history():
#     with shelve.open("chat_history") as db:
#         return db.get("messages", [])

# # Function to save chat history
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
#     st.chat_message(message["content"], avatar=avatar)

# # Main chat interface for input
# prompt = st.text_input("How can I help?")
# if prompt:
#     # Append user message to session state messages
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Prepare messages for the API
#     chat_messages = [{"role": message["role"], "content": message["content"]} for message in st.session_state.messages]

#     # Generate response from OpenAI API
#     response = openai.ChatCompletion.create(
#         model=st.session_state["openai_model"],
#         messages=chat_messages,
#         temperature=0.7
#     )
    
#     # Extract bot response
#     bot_response = response.choices[0].message["content"]

#     # Display bot response and update session state
#     st.session_state.messages.append({"role": "assistant", "content": bot_response})
#     st.chat_message(bot_response, avatar=BOT_AVATAR)

#     # Save chat history after each interaction
#     save_chat_history(st.session_state.messages)
# #Code for Basic Agent
# import openai
# import json
# import streamlit as st
# from dotenv import load_dotenv
# import os
# import shelve

# load_dotenv()

# st.title("Initial Agent Interface")

# USER_AVATAR = "👤"
# BOT_AVATAR = "🤖"

# # Set the OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

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

# # Handle new user input
# if prompt := st.chat_input("How can I help?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     # Attempt to generate a response from OpenAI
#     try:
#         response = openai.ChatCompletion.create(
#             model=st.session_state["openai_model"],
#             messages=[{"role": "user", "content": prompt}]
#         )

#         if response and 'choices' in response and len(response['choices']) > 0:
#             bot_response = response['choices'][0]['message']['content']
#         else:
#             bot_response = "Sorry, I couldn't fetch a response."
#     except Exception as e:
#         bot_response = f"Error: {str(e)}"

#     st.session_state.messages.append({"role": "assistant", "content": bot_response})
#     with st.chat_message("assistant", avatar=BOT_AVATAR):
#         st.markdown(bot_response)

#     # Save chat history after each interaction
#     save_chat_history(st.session_state.messages)

# import openai
# import streamlit as st
# import mysql.connector
# from datetime import datetime
# from dotenv import load_dotenv
# import os
# # Make sure to load the environment variables at the beginning of your script
# load_dotenv()



# # Now retrieve the environment variables
# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_NAME = os.getenv("DB_NAME")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Your db_config should now look like this
# db_config = {
#     'user': DB_USER,
#     'password': DB_PASS,
#     'host': DB_HOST,
#     'database': DB_NAME,
#     'raise_on_warnings': True
# }



# # Function to create a database connection
# def create_db_connection():
#     return mysql.connector.connect(**db_config)

# # Function to close the database connection
# def close_db_connection(conn):
#     conn.close()

# # Function to get the current milestone for a student
# def get_current_milestone(student_id):
#     conn = create_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     query = """
#     SELECT * FROM CWMilestonesStudent
#     WHERE StudentID = %s AND CWSubmitDate IS NULL
#     ORDER BY CWMilestoneSequence ASC
#     LIMIT 1
#     """
#     cursor.execute(query, (student_id,))
#     milestone = cursor.fetchone()
#     close_db_connection(conn)
#     return milestone

# # Function to get a prompt for the current milestone
# def get_prompt_for_milestone(coursework_id, milestone_sequence):
#     conn = create_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     query = """
#     SELECT * FROM Prompts
#     WHERE CourseWorkID = %s AND Remarks LIKE %s
#     """
#     remark = f"%M{milestone_sequence} deadline%"
#     cursor.execute(query, (coursework_id, remark))
#     prompt = cursor.fetchone()
#     close_db_connection(conn)
#     return prompt

# # Function to get a nudge for a prompt
# def get_nudge_for_prompt(prompt_id):
#     conn = create_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     query = "SELECT * FROM Nudges WHERE PromptID = %s"
#     cursor.execute(query, (prompt_id,))
#     nudge = cursor.fetchone()
#     close_db_connection(conn)
#     return nudge

# # Function to log a nudge
# def log_nudge(nudge_id, student_id, prompt_id):
#     conn = create_db_connection()
#     cursor = conn.cursor()
#     query = """
#     INSERT INTO NudgeLog (NudgeID, StudentID, PromptID, NudgeDateTime)
#     VALUES (%s, %s, %s, %s)
#     """
#     nudge_time = datetime.now()
#     cursor.execute(query, (nudge_id, student_id, prompt_id, nudge_time))
#     conn.commit()
#     close_db_connection(conn)

# # Function to get student information
# def get_student(student_id):
#     conn = create_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (student_id,))
#     student = cursor.fetchone()
#     close_db_connection(conn)
#     return student

# # Function to subscribe a student
# def subscribe_student(student_id, coursework_id):
#     # Here you would add logic to handle the subscription process
#     pass

# # Streamlit UI
# st.title("Nudge Based Motivational Agent")

# # Initialize session state variables
# if "student_id" not in st.session_state:
#     st.session_state["student_id"] = None

# # Subscription form
# with st.form("Subscription"):
#     student_id = st.text_input("Student ID")
#     coursework_id = st.text_input("Coursework ID")
#     submitted = st.form_submit_button("Subscribe")
#     if submitted and student_id and coursework_id:
#         st.session_state["student_id"] = student_id
#         subscribe_student(student_id, coursework_id)

# # Chat interface
# if st.session_state["student_id"]:
#     student = get_student(st.session_state["student_id"])
#     st.write(f"Hello, {student['StudentName']}")
#     if 'messages' not in st.session_state:
#         st.session_state['messages'] = []

#     # Display previous messages
#     for message in st.session_state['messages']:
#                 # Display previous messages
#         for message in st.session_state['messages']:
#             st.text_area("", value=message['content'], key=message['id'], height=75, disabled=True)

#         # User sends a message
#         user_message = st.text_input("Ask me anything...", key="user_message")

#         # When the user sends a message, it's processed here
#         if user_message:
#             # Save user message in session state
#             st.session_state['messages'].append({
#                 'id': len(st.session_state['messages']),
#                 'role': 'user',
#                 'content': user_message
#             })

#             # Generate a response from OpenAI
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_message}]
#             )

#             # Save OpenAI's response in session state
#             st.session_state['messages'].append({
#                 'id': len(st.session_state['messages']),
#                 'role': 'assistant',
#                 'content': response.choices[0].message['content']
#             })

#             # Check for nudges after each response
#             milestone = get_current_milestone(st.session_state["student_id"])
#             if milestone:
#                 prompt = get_prompt_for_milestone(milestone["CourseWorkID"], milestone["CWMilestoneSequence"])
#                 if prompt:
#                     nudge = get_nudge_for_prompt(prompt["PromptID"])
#                     if nudge:
#                         # Save nudge message in session state
#                         st.session_state['messages'].append({
#                             'id': len(st.session_state['messages']),
#                             'role': 'nudge',
#                             'content': nudge["NudgeText"]
#                         })

#                         # Log the nudge
#                         log_nudge(nudge["NudgeID"], st.session_state["student_id"], prompt["PromptID"])

#             # Clear the input
#             st.session_state['user_message'] = ""

# # Show the send button for the chat
# if st.button("Send"):
#     # This will trigger the message processing block above
#     pass

# # Show all messages
# for message in st.session_state['messages']:
#     if message['role'] == 'user':
#         st.text_area("You", value=message['content'], height=100, disabled=True)
#     elif message['role'] == 'assistant':
#         st.text_area("Assistant", value=message['content'], height=100, disabled=True)
#     elif message['role'] == 'nudge':
#         st.text_area("Nudge", value=message['content'], height=100, disabled=True)

##Working code but not fully.
# import openai
# import streamlit as st
# import mysql.connector
# from datetime import datetime
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Retrieve environment variables
# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_NAME = os.getenv("DB_NAME")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Configure the database connection
# db_config = {
#     'user': DB_USER,
#     'password': DB_PASS,
#     'host': DB_HOST,
#     'database': DB_NAME,
#     'raise_on_warnings': True
# }

# # Function to create a database connection
# def create_db_connection():
#     return mysql.connector.connect(**db_config)

# # Function to get student information using email
# def get_student_by_email(email):
#     conn = create_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM students WHERE StudentEmail = %s", (email,))
#     student = cursor.fetchone()
#     conn.close()
#     return student

# # Database Functions (to be defined according to your schema)

# def get_current_milestone(student_id):
#     conn = create_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     query = """
#     SELECT *
#     FROM CWMilestonesStudent
#     WHERE StudentID = %s AND CWSubmitDate IS NULL
#     ORDER BY CWMilestoneSequence ASC
#     LIMIT 1;
#     """
#     cursor.execute(query, (student_id,))
#     milestone = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return milestone

# def get_prompt_for_milestone(coursework_id, milestone_sequence):
#     conn = create_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     query = """
#     SELECT *
#     FROM Prompts
#     WHERE CourseWorkID = %s AND Remarks LIKE %s;
#     """
#     remark = f"%M{milestone_sequence} deadline%"
#     cursor.execute(query, (coursework_id, remark))
#     prompt = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return prompt

# def get_nudge_for_prompt(prompt_id):
#     conn = create_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     query = """
#     SELECT *
#     FROM Nudges
#     WHERE PromptID = %s;
#     """
#     cursor.execute(query, (prompt_id,))
#     nudge = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return nudge

# def log_nudge(nudge_id, student_id, prompt_id):
#     conn = create_db_connection()
#     cursor = conn.cursor()
#     query = """
#     INSERT INTO NudgeLog (NudgeID, StudentID, PromptID, NudgeDateTime)
#     VALUES (%s, %s, %s, %s);
#     """
#     nudge_time = datetime.now()
#     cursor.execute(query, (nudge_id, student_id, prompt_id, nudge_time))
#     conn.commit()
#     cursor.close()
#     conn.close()


# # Initialize session state variables
# if 'email' not in st.session_state:
#     st.session_state['email'] = None
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []

# # Streamlit UI for login
# st.title("Nudge Based Motivational Agent")
# email = st.text_input("Email", key="email_input")
# if st.button("Login"):
#     student = get_student_by_email(email)
#     if student:
#         st.session_state['email'] = email
#         st.session_state['student'] = student
#         st.session_state['messages'].clear()  # Clear previous chat history
#         st.write(f"Hello, {student['StudentName']}")
#     else:
#         st.error("No student found with this email.")

# # ... previous code ...

# # Function to fetch and send a nudge if applicable
# def check_and_send_nudge(student_id):
#     milestone = get_current_milestone(student_id)
#     if milestone:
#         prompt = get_prompt_for_milestone(milestone["CourseWorkID"], milestone["CWMilestoneSequence"])
#         if prompt:
#             nudge = get_nudge_for_prompt(prompt["PromptID"])
#             if nudge:
#                 # Append nudge message in session state
#                 st.session_state['messages'].append({
#                     'sender': 'Agent', 
#                     'text': nudge["NudgeText"]
#                 })
#                 # Log the nudge
#                 log_nudge(nudge["NudgeID"], student_id, prompt["PromptID"])

# # ... previous code ...

# # If student is logged in, display the chat interface
# if st.session_state.get('student'):
#     # Display chat history
#     for idx, msg in enumerate(st.session_state['messages']):
#         st.text_area(f"{msg['sender']}", value=msg['text'], height=75, disabled=True, key=f"msg_{idx}")

#     # Chat message input form
#     with st.form(key='chat'):
#         user_message = st.text_input("Type your message here...", key="user_message_input")
#         submit_button = st.form_submit_button(label='Send')

#         if submit_button and user_message:
#             # Append user message to the chat history
#             st.session_state['messages'].append({'sender': 'You', 'text': user_message})

#             # OpenAI API call to generate the response
#             openai.api_key = OPENAI_API_KEY
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{"role": "system", "content": "You are a helpful assistant."}, 
#                           {"role": "user", "content": user_message}]
#             )

#             # Append the response to the chat history
#             st.session_state['messages'].append({'sender': 'Agent', 'text': response.choices[0].message['content']})
            
#             # Check for any nudges that should be sent after this interaction
#             check_and_send_nudge(st.session_state['student']['StudentID'])

#             # Rerun the script to clear the input box
#             st.experimental_rerun()

# ... previous code ...

# import openai
# import streamlit as st
# import mysql.connector
# from datetime import datetime
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Retrieve environment variables
# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_NAME = os.getenv("DB_NAME")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Configure the database connection
# db_config = {
#     'user': DB_USER,
#     'password': DB_PASS,
#     'host': DB_HOST,
#     'database': DB_NAME,
#     'raise_on_warnings': True
# }

# # Initialize session state variables
# if 'student_email' not in st.session_state:
#     st.session_state['student_email'] = None
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []

# # Streamlit UI for login and chatbot interaction
# st.title("Nudge Based Motivational Agent")

# # User login using email
# email = st.text_input("Enter your student email", key="email_input")
# login_button = st.button("Login")

# # Database helper functions
# def create_db_connection():
#     connection = None
#     try:
#         connection = mysql.connector.connect(**db_config)
#     except mysql.connector.Error as e:
#         st.error(f"Error: {e}")
#     return connection

# def get_student_by_email(email):
#     student = None
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM students WHERE StudentEmail = %s", (email,))
#         student = cursor.fetchone()
#         conn.close()
#     return student

# def get_current_milestone(student_id):
#     milestone = None
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT cms.*, cw.CourseWorkDesc
#             FROM CWMilestonesStudent cms
#             JOIN CourseWork cw ON cms.CourseWorkID = cw.CourseWorkID
#             WHERE cms.StudentID = %s AND cms.CWSubmitDate IS NULL
#             ORDER BY cms.CWMilestoneSequence ASC
#             LIMIT 1
#         """, (student_id,))
#         milestone = cursor.fetchone()
#         conn.close()
#     return milestone

# def get_prompt_for_milestone(coursework_id, milestone_sequence):
#     prompt = None
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT * FROM Prompts
#             WHERE CourseWorkID = %s AND Remarks LIKE %s
#         """, (coursework_id, f"%M{milestone_sequence} deadline%"))
#         prompt = cursor.fetchone()
#         conn.close()
#     return prompt

# def get_nudge_for_prompt(prompt_id):
#     nudge = None
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM Nudges WHERE PromptID = %s", (prompt_id,))
#         nudge = cursor.fetchone()
#         conn.close()
#     return nudge

# def log_nudge(nudge_id, student_id, prompt_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO NudgeLog (NudgeID, StudentID, PromptID, NudgeDateTime)
#             VALUES (%s, %s, %s, %s)
#         """, (nudge_id, student_id, prompt_id, datetime.now()))
#         conn.commit()
#         conn.close()

# # Login logic
# if login_button:
#     student = get_student_by_email(email)
#     if student:
#         st.session_state['student_email'] = email
#         st.session_state['student_info'] = student
#         st.success(f"Logged in as {student['StudentName']}")
#     else:
#         st.error("Student with this email does not exist.")

# # # Chatbot interface
# # if 'student_info' in st.session_state and st.session_state['student_info']:
# #     student = st.session_state['student_info']
    
# #     # Display chat history
# #     for idx, msg in enumerate(st.session_state['messages']):
# #         st.text_area(f"{msg['sender']}", value=msg['text'], height=75, disabled=True, key=f"msg_{idx}")

# #     # Chat message input form
# #     user_message = st.text_input("Type your message here...", key="user_message_input")
# #     send_button = st.button("Send")

# # Function to get upcoming deadlines
# def get_upcoming_deadlines(student_id):
#     conn = create_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     query = """
#     SELECT CWMilestones.CWMilestoneDesc, CWMilestones.CWDueDate 
#     FROM CWMilestones
#     INNER JOIN CWMilestonesStudent 
#     ON CWMilestones.CWMilestoneID = CWMilestonesStudent.CWMilestoneID
#     WHERE CWMilestonesStudent.StudentID = %s AND CWMilestones.CWDueDate >= CURDATE()
#     ORDER BY CWMilestones.CWDueDate ASC;
#     """
#     cursor.execute(query, (student_id,))
#     upcoming_milestones = cursor.fetchall()
#     conn.close()
#     return upcoming_milestones

# # Function to format the milestones into a human-readable string
# def format_milestones(milestones):
#     if not milestones:
#         return "There are no upcoming deadlines."
#     milestones_str = "Your upcoming deadlines are:\n"
#     for milestone in milestones:
#         milestones_str += f"- {milestone['CWMilestoneDesc']} by {milestone['CWDueDate']}\n"
#     return milestones_str

# # ... (rest of your imports and setup code)

# # Chatbot interface
# if 'student_info' in st.session_state and st.session_state['student_info']:
#     student = st.session_state['student_info']
    
#     # Display chat history
#     for idx, msg in enumerate(st.session_state['messages']):
#         st.text_area(f"{msg['sender']}", value=msg['text'], height=75, disabled=True, key=f"msg_{idx}")

#     # Get user message from input
#     user_message = st.text_input("Type your message here...", key="user_message_input")
    
#     # When the user clicks 'send'
#     send_button = st.button("Send")
#     if send_button and user_message:
#         # Normal conversation, get response from OpenAI
#         openai.api_key = OPENAI_API_KEY
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "system", "content": "You are a helpful assistant."},
#                       {"role": "user", "content": user_message}]
#         )
#         response_text = response.choices[0].message['content']
        
#         # Special handling for "upcoming deadlines"
#         if "upcoming deadlines" in user_message.lower():
#             upcoming_milestones = get_upcoming_deadlines(student['StudentID'])
#             response_text = format_milestones(upcoming_milestones)
        
#         # Append both user message and response to the chat history
#         st.session_state['messages'].append({'sender': 'You', 'text': user_message})
#         st.session_state['messages'].append({'sender': 'Agent', 'text': response_text})

#         # Clear the input box after sending the message
#         st.experimental_rerun()

# ... (rest of your code)
##CODE WORKING FINE BUT NUDGE FUNCTIONALITY NOT WORKING;USE IF REQUIREMENT NOT REACHED WITH OTHER CODES....
# import openai
# import streamlit as st
# import mysql.connector
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta

# # Load environment variables
# load_dotenv()

# # Retrieve environment variables
# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_NAME = os.getenv("DB_NAME")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Configure the database connection
# db_config = {
#     'user': DB_USER,
#     'password': DB_PASS,
#     'host': DB_HOST,
#     'database': DB_NAME,
#     'raise_on_warnings': True
# }

# # Initialize session state variables
# if 'student_email' not in st.session_state:
#     st.session_state['student_email'] = None
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []

# # Streamlit UI for login and chatbot interaction
# st.title("Nudge Based Motivational Agent")

# # User login using email
# email = st.text_input("Enter your student email", key="email_input")
# login_button = st.button("Login")

# # Database helper functions
# def create_db_connection():
#     try:
#         conn = mysql.connector.connect(**db_config)
#         return conn
#     except mysql.connector.Error as e:
#         st.error(f"Database connection failed: {e}")
#         return None

# def get_student_by_email(email):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM students WHERE StudentEmail = %s", (email,))
#         student = cursor.fetchone()
#         conn.close()
#         return student
#     return None

# def get_current_milestone(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT cw.CourseWorkDesc, cm.CWMilestoneDesc, cm.CWDueDate 
#             FROM CWMilestones cm
#             INNER JOIN CourseWork cw ON cm.CourseWorkID = cw.CourseWorkID
#             INNER JOIN CWMilestonesStudent cms ON cm.CWMilestoneID = cms.CWMilestoneID
#             WHERE cms.StudentID = %s AND cms.CWSubmitDate IS NULL
#             ORDER BY cm.CWDueDate ASC
#             LIMIT 1
#         """, (student_id,))
#         milestone = cursor.fetchone()
#         conn.close()
#         return milestone
#     return None

# def get_nudges(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT n.NudgeText 
#             FROM Nudges n
#             INNER JOIN Prompts p ON n.PromptID = p.PromptID
#             INNER JOIN students s ON p.StudentID = s.StudentID
#             WHERE s.StudentID = %s
#             ORDER BY n.NudgeOccurrence DESC
#             LIMIT 1
#         """, (student_id,))
#         nudge = cursor.fetchone()
#         conn.close()
#         return nudge
#     return None

# def log_nudge(nudge_id, student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO NudgeLog (NudgeID, StudentID, NudgeDateTime)
#             VALUES (%s, %s, %s)
#         """, (nudge_id, student_id, datetime.now()))
#         conn.commit()
#         conn.close()

# # Define the get_nudge_if_appropriate function
# def get_nudge_if_appropriate(student_id):
#     # Determine if a nudge is needed based on the student's interaction
#     # This is simplified logic, replace with your own conditions as necessary
#     milestone = get_current_milestone(student_id)
#     if milestone and datetime.now().date() >= milestone['CWDueDate'] - timedelta(days=7):
#         # If there's an upcoming deadline within the next 7 days, fetch a nudge
#         nudge = get_nudges(student_id)
#         return nudge
#     return None

# # Define the format_deadlines function if not already defined
# def format_deadlines(milestones):
#     if not milestones:
#         return "You have no upcoming deadlines."
#     response = "Your upcoming deadlines are:\n"
#     for m in milestones:
#         response += f"{m['CWMilestoneDesc']} by {m['CWDueDate'].strftime('%Y-%m-%d')}\n"
#     return response

# # Define the get_upcoming_deadlines function if not already defined
# def get_upcoming_deadlines(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         query = """
#         SELECT cm.CWMilestoneDesc, cm.CWDueDate 
#         FROM CWMilestones cm
#         INNER JOIN CWMilestonesStudent cms ON cm.CWMilestoneID = cms.CWMilestoneID
#         WHERE cms.StudentID = %s AND cm.CWDueDate >= CURDATE()
#         ORDER BY cm.CWDueDate ASC;
#         """
#         cursor.execute(query, (student_id,))
#         upcoming_milestones = cursor.fetchall()
#         conn.close()
#         return upcoming_milestones
#     return None

# # Login logic
# if login_button:
#     student = get_student_by_email(email)
#     if student:
#         st.session_state['student_info'] = student
#         st.success(f"Logged in as {student['StudentName']}")
#     else:
#         st.error("Student with this email does not exist.")

# # Chatbot interface logic
# if 'student_info' in st.session_state and st.session_state['student_info']:
#     student = st.session_state['student_info']

#     # Display chat history
#     for idx, msg in enumerate(st.session_state['messages']):
#         st.text_area(f"{msg['sender']}", value=msg['text'], height=75, disabled=True, key=f"msg_{idx}")

#     # Chat message input
#     user_message = st.text_input("Type your message here...", key="user_message_input")
#     send_button = st.button("Send")

#     # Check if a nudge should be sent
#     nudge = get_nudge_if_appropriate(student['StudentID'])

#     if send_button and user_message:
#         # Append user message to the chat history
#         st.session_state['messages'].append({'sender': 'You', 'text': user_message})

#         # Generate a response from OpenAI's GPT-3.5-turbo
#         openai.api_key = OPENAI_API_KEY
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": user_message}
#             ]
#         )
#         response_text = response.choices[0].message['content']

#         # Append the response to the chat history
#         st.session_state['messages'].append({'sender': 'Agent', 'text': response_text})

#         # Clear the input box after sending the message
#         user_message = ""
#         st.experimental_rerun()

#     # If a nudge is appropriate, show it as a "ping"
#     if nudge:
#         st.sidebar.warning("Nudge Alert!")
#         st.sidebar.info(nudge['NudgeText'])
#         log_nudge(nudge['NudgeID'], student['StudentID'])

#         # You can also choose to append the nudge message directly to the chat history
#         st.session_state['messages'].append({'sender': 'Nudge', 'text': nudge['NudgeText']})
#         # Clear the input box after sending the message
#         st.experimental_rerun()


# from textblob import TextBlob
# import openai
# import streamlit as st
# import mysql.connector
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_NAME = os.getenv("DB_NAME")

# # Initialize OpenAI API key
# openai.api_key = OPENAI_API_KEY

# # Database connection configuration
# def get_db_connection():
#     conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
#     return conn

# # Fetch student info by email
# def get_student_by_email(email):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM students WHERE StudentEmail = %s", (email,))
#     student = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return student

# # Fetch current milestone for a student
# def get_current_milestone(student_id):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM CWMilestones WHERE StudentID = %s AND CWDueDate > CURDATE() ORDER BY CWDueDate ASC LIMIT 1", (student_id,))
#     milestone = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return milestone

# # Analyze message sentiment
# def analyze_sentiment(message):
#     analysis = TextBlob(message)
#     return 'positive' if analysis.sentiment.polarity >= 0 else 'negative'

# # Fetch nudge based on sentiment and student ID
# def get_nudge(student_id, sentiment):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM Nudges WHERE StudentID = %s AND Sentiment = %s ORDER BY RAND() LIMIT 1", (student_id, sentiment))
#     nudge = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return nudge

# # Main app
# st.title("Student Support Chatbot")

# if 'email' not in st.session_state:
#     st.session_state.email = st.text_input("Enter your email:")

# if st.session_state.email:
#     student = get_student_by_email(st.session_state.email)
#     if student:
#         user_message = st.text_input("How can I help you today?")
#         if user_message:
#             sentiment = analyze_sentiment(user_message)
#             milestone = get_current_milestone(student['StudentID'])
#             if sentiment == 'negative' and milestone:
#                 nudge = get_nudge(student['StudentID'], sentiment)
#                 if nudge:
#                     st.write(f"Nudge: {nudge['NudgeText']}")
#                 else:
#                     st.write("Remember, challenges are just opportunities in disguise.")
#             else:
#                 response = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=[{"role": "system", "content": "You are a helpful assistant."},
#                               {"role": "user", "content": user_message}]
#                 )
#                 bot_response = response.choices[0].message['content']
#                 st.write(f"Chatbot: {bot_response}")
#     else:
#         st.error("Student not found. Please check your email.")






       

# Streamlit is an open-source Python library that is used to build web applications for data science and machine learning projects. It provides a simple and efficient way to create interactive applications with minimal lines of code. With Streamlit, developers can easily visualize and explore data, create interactive plots and charts, and share their projects with others. It automatically updates and reruns the application as the code changes, making the development process smooth and hassle-free.
# Yes, you can connect a database with the Streamlit interface you are using right now. 
# Streamlit provides various ways to connect and interact with databases.
# You can use database libraries and packages such as SQLAlchemy, Pandas, or PyODBC to establish a connection with your database and perform queries or retrieve data.
# To connect to a database using an API key, you may need to check the documentation or specific requirements of the database you are using. Some databases may require additional authentication methods or specific connection parameters.
# Once you establish the connection, you can integrate the database functionality into your Streamlit application and display the retrieved data or perform CRUD operations directly from the interface.

# import streamlit as st
# from mysql.connector import connect, Error

# # Function to create a database connection
# def create_db_connection():
#     try:
#         return connect(
#             host='localhost',
#             user='root',
#             passwd='9717558791Mi#',  # Replace with your password
#             database='Nudge_Based_MotivationalAgent'
#         )
#     except Error as e:
#         st.error(f"Error connecting to the database: {e}")
#         st.stop()

# # Function to close the database connection
# def close_db_connection(connection):
#     if connection.is_connected():
#         connection.close()

# # Function to execute a read query
# def execute_read_query(query):
#     connection = create_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute(query)
#         result = cursor.fetchall()
#     except Error as e:
#         st.error(f"The error '{e}' occurred")
#         result = None
#     finally:
#         close_db_connection(connection)
#     return result

# # Load environment variables and set up Streamlit
# st.title("Nudge-Based Motivational Agent Interface")

# USER_AVATAR = "👤"
# BOT_AVATAR = "🤖"

# # Initialize or load chat history
# if "messages" not in st.session_state:
#     st.session_state['messages'] = []

# # Display chat messages
# for message in st.session_state['messages']:
#     avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
#     st.text(f"{avatar} {message['content']}")

# # Main chat interface
# user_input = st.text_input("How can I help?", key="chat_input")

# if user_input:
#     st.session_state['messages'].append({"role": "user", "content": user_input})

#     # Fetch student data based on user input, e.g., student ID
#     # Implement the logic to parse the student ID from the user input
#     student_id = "21355018"  # Replace with actual logic to extract from user input

#     # Fetch nudges for the student with a JOIN on the `Prompts` table
#     nudges_query = f"""
#     SELECT Nudges.NudgeText
#     FROM Nudges
#     INNER JOIN Prompts ON Nudges.PromptID = Prompts.PromptID
#     WHERE Prompts.StudentID = '{student_id}'
#     """
#     nudges = execute_read_query(nudges_query)

#     if nudges:
#         # Construct the response including the nudges
#         response = "Here are your nudges:\n"
#         response += "\n".join(nudge['NudgeText'] for nudge in nudges)
#     else:
#         response = "No nudges found for the given student ID."

#     st.session_state['messages'].append({"role": "assistant", "content": response})


# Best Prototype code
# import streamlit as st
# from mysql.connector import connect, Error
# import os  # For environment variables

# # Database connection setup
# def create_db_connection():
#     try:
#         connection = connect(
#             host=os.environ['DB_HOST'],  # Use environment variables
#             user=os.environ['DB_USER'],
#             passwd=os.environ['DB_PASS'],
#             database=os.environ['DB_NAME']
#         )
#         return connection
#     except Error as e:
#         st.error(f"Database connection failed due to: {e}")
#         st.stop()

# # Execute read query
# def execute_read_query(query):
#     connection = create_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute(query)
#         return cursor.fetchall()
#     finally:
#         cursor.close()
#         connection.close()

# # Simulate student login and fetch profile
# def fetch_student_profile(email):
#     query = f"SELECT * FROM Students WHERE StudentEmail = '{email}'"
#     results = execute_read_query(query)
#     return results[0] if results else None

# # Fetch coursework and milestones for a student
# def fetch_coursework_and_milestones(student_id):
#     query = f"""
#     SELECT cw.CourseWorkDesc, cwm.CWMilestoneDesc, cwm.CWDueDate
#     FROM CourseWork cw
#     JOIN CWMilestones cwm ON cw.CourseWorkID = cwm.CourseWorkID
#     WHERE cw.CourseID IN (
#         SELECT CourseID FROM Students WHERE StudentID = '{student_id}'
#     )
#     ORDER BY cwm.CWDueDate
#     """
#     return execute_read_query(query)


# # Fetch nudges for a student
# def fetch_nudges(student_id):
#     query = f"SELECT NudgeText FROM Nudges WHERE NudgeID IN (SELECT NudgeID FROM NudgeLog WHERE StudentID = '{student_id}')"
#     return execute_read_query(query)

# # Displaying student information and fetched data
# def display_student_info(student_profile, coursework_and_milestones, nudges):
#     st.subheader("Student Profile")
#     st.json(student_profile)

#     st.subheader("Coursework and Milestones")
#     for cm in coursework_and_milestones:
#         st.write(f"{cm['CourseWorkDesc']}: {cm['CWMilestoneDesc']} - Due {cm['CWDueDate']}")

#     st.subheader("Nudges")
#     for nudge in nudges:
#         st.write(nudge['NudgeText'])

# # Main app functionality
# def main():
#     st.title("Nudge-Based Motivational Agent Prototype")

#     student_email = st.text_input("Enter your student email:")
#     if student_email:
#         student_profile = fetch_student_profile(student_email)
#         if student_profile:
#             coursework_and_milestones = fetch_coursework_and_milestones(student_profile['StudentID'])
#             nudges = fetch_nudges(student_profile['StudentID'])
#             display_student_info(student_profile, coursework_and_milestones, nudges)
#         else:
#             st.error("Student profile not found. Please check the email entered.")

# if __name__ == "__main__":
#     main()

#Just to fetch personalised nudge of each student.
# import os
# from dotenv import load_dotenv
# import streamlit as st
# from mysql.connector import connect, Error
# import openai

# # Load environment variables
# load_dotenv()

# # Set the OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Database connection setup
# def create_db_connection():
#     try:
#         connection = connect(
#             host=os.getenv('DB_HOST'),
#             user=os.getenv('DB_USER'),
#             passwd=os.getenv('DB_PASS'),
#             database=os.getenv('DB_NAME')
#         )
#         return connection
#     except Error as e:
#         st.error(f"Database connection failed: {e}")
#         return None

# # Function to execute a query
# def execute_query(connection, query, params=None):
#     with connection.cursor(dictionary=True) as cursor:
#         cursor.execute(query, params)
#         return cursor.fetchall()

# # Function to fetch nudges for a student
# def fetch_nudges_for_student(student_id):
#     connection = create_db_connection()
#     if connection is not None:
#         query = """
#         SELECT Nudges.NudgeText
#         FROM Nudges
#         INNER JOIN NudgeLog ON Nudges.NudgeID = NudgeLog.NudgeID
#         WHERE NudgeLog.StudentID = %s;
#         """
#         nudges = execute_query(connection, query, (student_id,))
#         connection.close()
#         return nudges

# # Streamlit app
# def app():
#     st.title('Nudge-Based Motivational Agent Interface')

#     # Student ID input (you can also use email or other identifiers)
#     student_id = st.text_input('Enter your Student ID to receive personalized nudges:')
    
#     if student_id:
#         # Here you might want to call the OpenAI API using the openai.ChatCompletion.create function
#         # and pass the student's conversation context to generate a response
        
#         nudges = fetch_nudges_for_student(student_id)
#         if nudges:
#             st.write('Personalized Nudges:')
#             for nudge in nudges:
#                 st.write(nudge['NudgeText'])
#         else:
#             st.write('No nudges found for the given Student ID.')

# if __name__ == "__main__":
#     app()

# import os
# from dotenv import load_dotenv
# import streamlit as st
# import mysql.connector
# from mysql.connector import connect, Error
# import openai

# # Set the OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# load_dotenv()
# # Database connection setup
# def create_db_connection():
#     try:
#         connection = mysql.connector.connect(
#              host=os.getenv('DB_HOST'),
#              user=os.getenv('DB_USER'),
#              passwd=os.getenv('DB_PASS'),
#              database=os.getenv('DB_NAME')
#         )
#         return connection
#     except Error as e:
#         st.error(f"Database connection failed due to: {e}")
#         st.stop()

# # Define the callback to update the user input in the session state
# def update_input():
#     st.session_state.user_input = st.text_input("user_input")
    
# # Check if the user exists in the database
# def check_user(email):
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT * FROM students WHERE StudentEmail = '{email}'")
#     result = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     return result

# # Main function to drive the Streamlit app
# def main():
#     st.title("Nudge-Based Motivational Agent")
    
#     # Only Login functionality in the sidebar
#     login_user_email = st.sidebar.text_input("Enter your student email to login:")
    
#     if st.sidebar.button("Login"):
#         user = check_user(login_user_email)
#         if user:
#             st.success(f"Welcome back {user[1]}")  # Assuming the second column is the name
#             chat_interface(user[0])  # Pass the StudentID to the chat interface
#         else:
#             st.error("Student profile not found. Please check the email entered.")

# # Chat interface where dynamic nudges are displayed
# def chat_interface(student_id):
#     st.subheader("Chat with NudgeBot")
    
#     # Use session state to store and display chat history
#     if 'chat_history' not in st.session_state:
#         st.session_state['chat_history'] = []

#     # Display the chat history
#     for message in st.session_state['chat_history']:
#         st.text(message)

#     # Text input for user's message with a key to preserve state across reruns
#     user_message = st.text_input("Type your message here...", key="user_message")

#     # When the "Send" button is pressed, process the input
#     if st.button("Send"):
#         if user_message:  # Check if the input is not only whitespace
#             st.session_state['chat_history'].append(f"You: {user_message}")
#             nudge = fetch_nudge(student_id, user_message)  # Fetch a nudge based on the context
#             st.session_state['chat_history'].append(f"NudgeBot: {nudge}")
#             # Clear the input box after sending the message
#             st.session_state['user_message'] = ''
#             # Rerun the app to update the chat history display
#             st.experimental_rerun()
#         else:
#             st.warning("Please type a message before sending.")


# # Fetch a personalized nudge from the database based on the student's context
# def fetch_nudge(student_id, context):
#     # This function remains the same as previously defined
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT NudgeText FROM Nudges WHERE StudentID = '{student_id}' ORDER BY RAND() LIMIT 1")
#     nudge = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     return nudge[0] if nudge else "Keep up the good work!"

# if __name__ == "__main__":
#     main()

# import openai
# import streamlit as st
# from dotenv import load_dotenv
# import os
# import shelve
# import mysql.connector
# from mysql.connector import connect, Error

# load_dotenv()


# # Set the OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Database connection setup
# def create_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host=os.getenv('DB_HOST'),
#             user=os.getenv('DB_USER'),
#             passwd=os.getenv('DB_PASS'),
#             database=os.getenv('DB_NAME')
#         )
#         return connection
#     except Error as e:
#         st.error(f"Database connection failed due to: {e}")
#         return None

# # Check if the user exists in the database
# def check_user(email):
#     connection = create_db_connection()
#     if connection:
#         cursor = connection.cursor()
#         cursor.execute(f"SELECT * FROM students WHERE StudentEmail = '{email}'")
#         result = cursor.fetchone()
#         cursor.close()
#         connection.close()
#         return result
#     else:
#         return None

# # Function to fetch personalized nudge
# def fetch_nudge(student_id):
#     connection = create_db_connection()
#     if connection:
#         try:
#             cursor = connection.cursor()
#             cursor.execute(f"""
#                 SELECT NudgeText FROM Nudges 
#                 WHERE StudentID = %s
#                 ORDER BY RAND() 
#                 LIMIT 1
#             """, (student_id,))
#             result = cursor.fetchone()
#             nudge = result[0] if result else "Keep up the good work!"
#             return nudge
#         except Error as e:
#             st.error(f"Error fetching nudge: {e}")
#             return "Keep striving for your goals!"
#         finally:
#             cursor.close()
#             connection.close()
#     else:
#         return "Could not fetch nudge due to database connection issues."

# # Load chat history from shelve file
# def load_chat_history():
#     with shelve.open("chat_history") as db:
#         return db.get("messages", [])

# # Save chat history to shelve file
# def save_chat_history(messages):
#     with shelve.open("chat_history") as db:
#         db["messages"] = messages

# # Display login form
# def show_login():
#     st.sidebar.subheader("Login")
#     login_user_email = st.sidebar.text_input("Enter your student email to login:")
#     if st.sidebar.button("Login"):
#         user = check_user(login_user_email)
#         if user:
#             st.sidebar.success(f"Welcome back {user[1]}")
#             st.session_state['student_id'] = user[0]
#             # Initialize chat history
#             st.session_state['messages'] = load_chat_history()
#         else:
#             st.sidebar.error("Student profile not found. Please check the email entered.")

# # Main application
# def main():
#     st.title("Nudge-Based Motivational Agent")

#     # Only show login if student_id is not set
#     if 'student_id' not in st.session_state:
#         show_login()
#     else:
#         chat_with_bot()

# # Chatbot interaction code
# def chat_with_bot():
#     st.subheader("Chat with NudgeBot")

#     # Display chat messages
#     if 'messages' in st.session_state:
#         for message in st.session_state['messages']:
#             role, text = message["role"], message["content"]
#             st.text(f"{role}: {text}")

#     # User input
#     user_input = st.text_input("Type your message here...", key="user_input")

#     # Handle sending message
#     if st.button("Send"):
#         if user_input:
#             # Append user input to messages
#             st.session_state['messages'].append({"role": "user", "content": user_input})
            
#             # Generate response using OpenAI's GPT chat model
#             try:
#                 response = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo",  # Use the model name directly as a string
#                     messages=[{"role": "user", "content": user_input}]
#                 )
#                 # Append bot response to messages
#                 bot_response = response.choices[0].message['content'].strip() if response.choices else "Let me think..."
#                 st.session_state['messages'].append({"role": "assistant", "content": bot_response})
#             except openai.error.OpenAIError as e:
#                 st.error(f"An error occurred: {e}")
#                 bot_response = "I'm having trouble thinking of a response right now."
#                 st.session_state['messages'].append({"role": "assistant", "content": bot_response})

#             # Clear input field after sending the message
#             st.session_state.user_input = ""
#             # Save chat history
#             save_chat_history(st.session_state['messages'])
#             # Rerun to display new messages
#             st.experimental_rerun()

#     # Add a personalized nudge to the conversation
#     if st.button('Get Motivational Nudge'):
#         nudge = fetch_nudge(st.session_state['student_id'])
#         st.session_state['messages'].append({"role": "assistant", "content": nudge})
#         save_chat_history(st.session_state['messages'])
#         # Rerun to display the nudge
#         st.experimental_rerun()


# # Run the main function
# if __name__ == "__main__":
#     main()



# import openai
# import streamlit as st
# import mysql.connector
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta, date

# # Load environment variables
# load_dotenv()

# # Retrieve environment variables
# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_NAME = os.getenv("DB_NAME")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Configure the database connection
# db_config = {
#     'user': DB_USER,
#     'password': DB_PASS,
#     'host': DB_HOST,
#     'database': DB_NAME,
#     'raise_on_warnings': True,
# }

# # Initialize session state variables
# if 'student_email' not in st.session_state:
#     st.session_state['student_email'] = None
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []
# # Initialize the simulated date to the start of your project timeline
# if 'simulated_date' not in st.session_state:
#     st.session_state['simulated_date'] = date(2024, 2, 28)  # Example start date based on your SQL script

# # Streamlit UI for login and chatbot interaction
# st.title("Nudge Based Motivational Agent")

# # User login using email
# email = st.text_input("Enter your student email", key="email_input")
# login_button = st.button("Login")

# # Database helper functions
# def create_db_connection():
#     try:
#         conn = mysql.connector.connect(**db_config)
#         return conn
#     except mysql.connector.Error as e:
#         st.error(f"Database connection failed: {e}")
#         return None

# def get_student_by_email(email):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM students WHERE StudentEmail = %s", (email,))
#         student = cursor.fetchone()
#         conn.close()
#         return student
#     return None

# def get_nudges(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT n.NudgeText, n.NudgeID, p.PromptID  # Include PromptID in selection
#             FROM Nudges n
#             INNER JOIN Prompts p ON n.PromptID = p.PromptID
#             INNER JOIN students s ON p.StudentID = s.StudentID
#             WHERE s.StudentID = %s
#             ORDER BY n.NudgeOccurrence DESC
#             LIMIT 1
#         """, (student_id,))
#         nudge = cursor.fetchone()
#         conn.close()
#         return nudge
#     return None


# # Modify the log_nudge function to prevent duplicate logging
# def log_nudge(nudge_id, student_id, prompt_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         # Check if the nudge has already been logged for the student
#         cursor.execute("""
#             SELECT * FROM NudgeLog WHERE NudgeID = %s AND StudentID = %s
#         """, (nudge_id, student_id))
#         existing_log = cursor.fetchone()
#         if not existing_log:  # If it hasn't been logged, then insert
#             cursor.execute("""
#                 INSERT INTO NudgeLog (NudgeID, StudentID, PromptID, NudgeDateTime)
#                 VALUES (%s, %s, %s, %s)
#             """, (nudge_id, student_id, prompt_id, datetime.now()))
#             conn.commit()
#         conn.close()


# def simulate_time_progression(days=1):
#     """Simulates the progression of time by increasing the simulated_date."""
#     if 'simulated_date' in st.session_state:
#         st.session_state['simulated_date'] += timedelta(days=days)

# def get_nudge_if_appropriate(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         today = st.session_state['simulated_date']
#         upcoming_days = today + timedelta(days=7)  # Check for milestones within the next 7 days

#         cursor.execute("""
#             SELECT n.NudgeText, n.NudgeID, p.PromptID  # Make sure to select PromptID
#             FROM Nudges n
#             JOIN Prompts p ON n.PromptID = p.PromptID
#             JOIN CWMilestones cm ON p.CourseWorkID = cm.CourseWorkID
#             JOIN CWMilestonesStudent cms ON cm.CWMilestoneID = cms.CWMilestoneID
#             WHERE cms.StudentID = %s AND cm.CWDueDate >= %s AND cm.CWDueDate <= %s
#             ORDER BY cm.CWDueDate ASC
#             LIMIT 1
#         """, (student_id, today, upcoming_days))

#         nudge = cursor.fetchone()
#         conn.close()
#         return nudge
#     return None


# def check_for_milestone_request(message):
#     # This is a rudimentary check. In a real-world application, you might use NLP techniques to determine intent.
#     keywords = ["milestone", "deadline", "due date", "assignment"]
#     return any(keyword in message.lower() for keyword in keywords)

# def get_milestones_for_student(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT cm.CWMilestoneDesc, cm.CWDueDate 
#             FROM CWMilestones cm
#             JOIN CWMilestonesStudent cms ON cm.CWMilestoneID = cms.CWMilestoneID
#             WHERE cms.StudentID = %s AND cms.CWSubmitDate IS NULL
#             ORDER BY cm.CWDueDate ASC
#         """, (student_id,))
#         milestones = cursor.fetchall()
#         conn.close()
#         return milestones
#     return None

# def format_milestones_response(milestones):
#     if not milestones:
#         return "You have no upcoming coursework milestones."
#     response = "Here are your upcoming coursework milestones:\n"
#     for milestone in milestones:
#         due_date = milestone['CWDueDate'].strftime('%Y-%m-%d')
#         response += f"- {milestone['CWMilestoneDesc']} due by {due_date}\n"
#     return response

# # Login logic
# if login_button:
#     student = get_student_by_email(email)
#     if student:
#         st.session_state['student_info'] = student
#         st.success(f"Logged in as {student['StudentName']}")
#     else:
#         st.error("Student with this email does not exist.")

# # ... (The beginning of your code remains unchanged)

# # Function to get the latest nudge for the student
# def display_nudge(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         # Make sure the SELECT statement includes the NudgeID
#         cursor.execute("""
#             SELECT n.NudgeID, n.NudgeText, p.PromptID  # Include PromptID and NudgeID in the selection
#             FROM Nudges n
#             INNER JOIN Prompts p ON n.PromptID = p.PromptID
#             WHERE p.StudentID = %s
#             ORDER BY n.NudgeID ASC  # Assuming NudgeID increments with each new nudge
#         """, (student_id,))
#         nudge = cursor.fetchone()
#         conn.close()
#         # If a nudge is found, display it in the sidebar
#         if nudge:
#             st.sidebar.warning("Nudge Alert!")
#             st.sidebar.info(nudge['NudgeText'])
#             # Log the nudge display
#             log_nudge(nudge['NudgeID'], student_id, nudge['PromptID'])

# # ... (The rest of your helper functions remain unchanged)

# # ... (earlier parts of your code remain unchanged)

# # Update the Chatbot interface logic section
# if 'student_info' in st.session_state and st.session_state['student_info']:
#     student = st.session_state['student_info']
    
#     # Display chat history
#     for idx, msg in enumerate(st.session_state['messages']):
#         st.text_area(f"{msg['sender']}", value=msg['text'], height=75, disabled=True, key=f"msg_{idx}")

#     # Chat message input
#     user_message = st.text_input("Type your message here...", key="user_message_input")
#     send_button = st.button("Send")

#     if send_button and user_message:
#         # Append user message to the chat history
#         st.session_state['messages'].append({'sender': 'You', 'text': user_message})
        
#         # Check if the user is asking about coursework milestones
#         if check_for_milestone_request(user_message):
#             milestones = get_milestones_for_student(student['StudentID'])
#             milestones_response = format_milestones_response(milestones)
#             st.session_state['messages'].append({'sender': 'Agent', 'text': milestones_response})
#         else:
#             # Generate a response from OpenAI's GPT-3.5-turbo
#             openai.api_key = OPENAI_API_KEY
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": user_message}
#                 ]
#             )
#             response_text = response.choices[0].message['content']
#             st.session_state['messages'].append({'sender': 'Agent', 'text': response_text})
        
#         # Always check for any new appropriate nudges, regardless of the message content
#         nudge = get_nudge_if_appropriate(student['StudentID'])
#         if nudge:
#             st.sidebar.warning("Nudge Alert!")
#             st.sidebar.info(nudge['NudgeText'])
#             if 'PromptID' in nudge:
#                 log_nudge(nudge['NudgeID'], student['StudentID'], nudge['PromptID'])
#             else:
#                 # Handle the case where 'PromptID' is not in nudge (perhaps log an error or use a default value)
#                 st.error('Error: Nudge does not contain PromptID.')
#             st.session_state['messages'].append({'sender': 'Nudge', 'text': nudge['NudgeText']})

#         # Clear the input box after sending the message
#         st.experimental_rerun()
        
# ... (rest of your code)


# # UI for simulating date progression (optional, for testing purposes)
# if 'admin' in st.session_state['student_email']:  # Assuming an admin mode for direct date manipulation
#     st.sidebar.title("Simulate Date Progression")
#     days_to_advance = st.sidebar.number_input("Days to advance:", min_value=1, value=1)
#     if st.sidebar.button(f"Advance by {days_to_advance} days"):
#         simulate_time_progression(days=days_to_advance)
#         st.sidebar.success(f"Current simulated date: {st.session_state['simulated_date']}")

# Import required libraries
# import openai
# import streamlit as st
# import mysql.connector
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta

# # Load environment variables
# load_dotenv()

# # Retrieve environment variables
# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_NAME = os.getenv("DB_NAME")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Configure the database connection
# db_config = {
#     'user': DB_USER,
#     'password': DB_PASS,
#     'host': DB_HOST,
#     'database': DB_NAME,
#     'raise_on_warnings': True,
# }

# # Initialize session state variables
# if 'student_info' not in st.session_state:
#     st.session_state['student_info'] = None
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []
# if 'simulated_current_time' not in st.session_state:
#     st.session_state['simulated_current_time'] = datetime.now()

# # Streamlit UI for login and chatbot interaction
# st.title("Nudge Based Motivational Agent")

# # User login using email
# email = st.text_input("Enter your student email", key="email_input")
# login_button = st.button("Login")

# # Function to create database connection
# def create_db_connection():
#     try:
#         conn = mysql.connector.connect(**db_config)
#         return conn
#     except mysql.connector.Error as e:
#         st.error(f"Database connection failed: {e}")
#         return None

# # Function to get student by email
# def get_student_by_email(email):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM students WHERE StudentEmail = %s", (email,))
#         student = cursor.fetchone()
#         conn.close()
#         return student
#     return None

# # Login logic
# if login_button:
#     student = get_student_by_email(email)
#     if student:
#         st.session_state['student_info'] = student
#         st.success(f"Logged in as {student['StudentName']}")
#     else:
#         st.error("Student with this email does not exist.")

# # Function to simulate current time progression
# def simulate_current_time():
#     st.session_state['simulated_current_time'] += timedelta(minutes=5)
#     return st.session_state['simulated_current_time']

# # Function to retrieve and display the latest nudge for the logged-in student
# def display_latest_nudge(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT n.NudgeText
#             FROM Nudges n
#             INNER JOIN Prompts p ON n.PromptID = p.PromptID
#             WHERE p.StudentID = %s
#             ORDER BY n.NudgeID DESC
#             LIMIT 1
#         """, (student_id,))
#         nudge = cursor.fetchone()
#         conn.close()
#         if nudge:
#             st.sidebar.warning("Latest Nudge Alert!")
#             st.sidebar.info(nudge['NudgeText'])

# # Function to send message and get a response from OpenAI's GPT
# def send_message(message, student):
#     openai.api_key = OPENAI_API_KEY
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": message}
#         ]
#     )
#     response_text = response.choices[0].message['content']
#     st.session_state['messages'].append({'sender': 'Agent', 'text': response_text})
#     return response_text

# # Chatbot interface logic
# if 'student_info' in st.session_state and st.session_state['student_info']:
#     student = st.session_state['student_info']

#     # Display chat history
#     for idx, msg in enumerate(st.session_state['messages']):
#         st.text_area(f"{msg['sender']}", value=msg['text'], height=75, disabled=True, key=f"msg_{idx}")

#     # Chat message input
#     user_message = st.text_input("Type your message here...", key="user_message_input")
#     send_button = st.button("Send")

#     if send_button and user_message:
#         # Append user message to the chat history if it's not the last message already
#         if not st.session_state['messages'] or st.session_state['messages'][-1]['text'] != user_message:
#             st.session_state['messages'].append({'sender': 'You', 'text': user_message})
        
#         # Generate a response from OpenAI's GPT and append to chat history
#         if 'last_response' not in st.session_state or st.session_state['last_response'] != user_message:
#             agent_response = send_message(user_message, student)
#             st.session_state['messages'].append({'sender': 'Agent', 'text': agent_response})
#             st.session_state['last_response'] = user_message
        
#         # Clear the input box after sending the message
#         st.experimental_rerun()

# # Function to retrieve and display nudges for logged-in student from the start of the NudgeID
# def display_nudges_from_start(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT n.NudgeID, n.NudgeText
#             FROM Nudges n
#             JOIN Prompts p ON n.PromptID = p.PromptID
#             WHERE p.StudentID = %s
#             ORDER BY n.NudgeID ASC
#         """, (student_id,))
#         nudges = cursor.fetchall()
#         conn.close()

#         # Initialize the last nudge ID if not present in the session state
#         if 'last_nudge_id' not in st.session_state:
#             st.session_state['last_nudge_id'] = 'N000'  # Use a default starting value

#         for nudge in nudges:
#             # Compare strings directly, no int conversion
#             if nudge['NudgeID'] > st.session_state['last_nudge_id']:
#                 st.session_state['last_nudge_id'] = nudge['NudgeID']
#                 st.sidebar.warning("Nudge Alert!")
#                 st.sidebar.info(nudge['NudgeText'])
#                 break  # Break after showing one nudge to not overwhelm the sidebar


# # Call this function where appropriate in your code, likely after logging in
# if 'student_info' in st.session_state and st.session_state['student_info']:
#     display_nudges_from_start(st.session_state['student_info']['StudentID'])


# ... the rest of your existing code ...


# import openai
# import streamlit as st
# import mysql.connector
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta, date
# import time
# import random
# import streamlit as st

# # Load environment variables
# load_dotenv()

# # Environment variables
# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_NAME = os.getenv("DB_NAME")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Database configuration
# db_config = {
#     'user': DB_USER,
#     'password': DB_PASS,
#     'host': DB_HOST,
#     'database': DB_NAME,
#     'raise_on_warnings': True,
# }

# # Initialize session state variables if they don't exist
# if 'student_email' not in st.session_state:
#     st.session_state['student_email'] = None
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []
# if 'simulated_date' not in st.session_state:
#     st.session_state['simulated_date'] = date(2024, 1, 1)  # Set to your project's start date

# # Streamlit UI setup
# st.title("Nudge Based Motivational Agent")

# # User login
# email = st.text_input("Enter your student email", key="email_input")
# login_button = st.button("Login")

# # Database connection
# def create_db_connection():
#     try:
#         return mysql.connector.connect(**db_config)
#     except mysql.connector.Error as e:
#         st.error(f"Database connection failed: {e}")
#         return None

# # Fetch student info by email
# def get_student_by_email(email):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM students WHERE StudentEmail = %s", (email,))
#         student = cursor.fetchone()
#         conn.close()
#         return student

# # Fetch first nudge assigned to the student
# def get_first_nudge(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT n.NudgeID, n.NudgeText, p.PromptID
#             FROM Nudges n
#             JOIN Prompts p ON n.PromptID = p.PromptID
#             WHERE p.StudentID = %s
#             ORDER BY n.NudgeOccurrence ASC
#             LIMIT 1
#         """, (student_id,))
#         nudge = cursor.fetchone()
#         conn.close()
#         return nudge

# # Function to log student's request for personal milestones
# def get_personal_milestones(student_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT cm.CWMilestoneDesc, cm.CWDueDate
#             FROM CWMilestones cm
#             JOIN CWMilestonesStudent cms ON cm.CWMilestoneID = cms.CWMilestoneID
#             WHERE cms.StudentID = %s
#             ORDER BY cm.CWDueDate ASC
#         """, (student_id,))
#         milestones = cursor.fetchall()
#         conn.close()
#         return milestones

# # Formatting function for milestones
# def format_milestones(milestones):
#     if not milestones:
#         return "You have no milestones."
#     response = "Here are your milestones:\n"
#     for milestone in milestones:
#         due_date = milestone['CWDueDate'].strftime('%Y-%m-%d')
#         response += f"- {milestone['CWMilestoneDesc']} due by {due_date}\n"
#     return response

# # Function to trigger nudge based on specific event during chat
# def trigger_nudge(event):
#     # Logic to determine which nudge to trigger based on the event
#     # You can implement this logic as per your requirement
#     pass

# # Function to log the display of a nudge
# def log_nudge(nudge_id, student_id, prompt_id):
#     conn = create_db_connection()
#     if conn:
#         cursor = conn.cursor()
#         current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         # Check if the nudge has already been logged for the student
#         cursor.execute("SELECT COUNT(*) FROM NudgeLog WHERE NudgeID = %s AND StudentID = %s", (nudge_id, student_id))
#         count = cursor.fetchone()[0]
        
#         if count == 0:
#             # Nudge has not been logged yet, proceed with insertion
#             cursor.execute("INSERT INTO NudgeLog (NudgeID, StudentID, PromptID, NudgeDateTime) VALUES (%s, %s, %s, %s)", (nudge_id, student_id, prompt_id, current_datetime))
#             conn.commit()
#             st.success("Nudge logged successfully.")
#         else:
#             st.warning("Nudge already logged for this student.")
        
#         conn.close()

# # Function to display nudge to the user
# def display_nudge(nudge):
#     st.sidebar.warning("Nudge Alert!")
#     st.sidebar.info(nudge['NudgeText'])
#     # Log nudge display
#     log_nudge(nudge['NudgeID'], student_id, nudge['PromptID'])

# # Login functionality
# if login_button:
#     student_info = get_student_by_email(email)
#     if student_info:
#         st.session_state['student_info'] = student_info
#         st.success(f"Logged in as {student_info['StudentName']}")
#     else:
#         st.error("No student found with this email.")

# # Chat functionality
# if 'student_info' in st.session_state and st.session_state['student_info']:
#     student_id = st.session_state['student_info']['StudentID']
#     nudge = get_first_nudge(student_id)

#     # Display nudge if available
#     if nudge:
#         st.sidebar.warning("Nudge Alert!")
#         st.sidebar.info(nudge['NudgeText'])

#     # Display chat history
#     for idx, msg in enumerate(st.session_state['messages']):
#         st.text_area(f"Message {idx+1}", value=msg['text'], height=75, disabled=True, key=f"msg_{idx}")

#     # Message input
#     user_message = st.text_input("Type your message here...", key=f"user_message_input_")

#     send_button = st.button("Send")

#     if send_button and user_message:
#         # Append user message to chat history
#         st.session_state['messages'].append({'sender': 'You', 'text': user_message})
        
#         # Simulate time progression
#         st.session_state['simulated_date'] += timedelta(days=1)

#         # Check for milestone inquiry
#         if any(keyword in user_message.lower() for keyword in ["milestone", "deadline", "due date", "assignment"]):
#             milestones = get_personal_milestones(student_id)
#             milestones_response = format_milestones(milestones)
#             st.session_state['messages'].append({'sender': 'Agent', 'text': milestones_response})
#         else:
#             # Trigger nudge based on user message
#             trigger_nudge(user_message)

#             # Generate response from GPT-3.5-turbo
#             openai.api_key = OPENAI_API_KEY
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": user_message}
#                 ]
#             )
#             response_text = response.choices[0].message['content']
#             st.session_state['messages'].append({'sender': 'Agent', 'text': response_text})

#         # Check for new nudge
#         nudge = get_first_nudge(student_id)

#         if nudge:
#             st.sidebar.warning("Nudge Alert!")
#             st.sidebar.info(nudge['NudgeText'])
#             # Log nudge display
#             log_nudge(nudge['NudgeID'], student_id, nudge['PromptID'])

#         # Clear input box after sending message
#         st.text_input("Type your message here...", key="user_message_input", value="")

# # Save chat history
# st.query_params['messages'] = st.session_state['messages']


import openai
import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, date
import time
import random
import uuid

# Load environment variables
load_dotenv()

# Define avatars for user and bot
USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
# Environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database configuration
db_config = {
    'user': DB_USER,
    'password': DB_PASS,
    'host': DB_HOST,
    'database': DB_NAME,
    'raise_on_warnings': True,
}

# Initialize session state variables if they don't exist
if 'student_info' not in st.session_state:
    st.session_state['student_info'] = None
if 'student_email' not in st.session_state:
    st.session_state['student_email'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'simulated_date' not in st.session_state:
    st.session_state['simulated_date'] = date(2024, 1, 1)
if 'nudge_displayed' not in st.session_state:
    st.session_state['nudge_displayed'] = False
if 'login_successful' not in st.session_state:
    st.session_state['login_successful'] = False
if 'nudges' not in st.session_state:  # This line ensures 'nudges' key is initialized
    st.session_state['nudges'] = []
# Initialize the current nudge index if not already set
if 'current_nudge_index' not in st.session_state:
    st.session_state['current_nudge_index'] = 0
# Initialize session state for the first nudge display
if 'first_nudge_shown' not in st.session_state:
    st.session_state['first_nudge_shown'] = False
if 'message_to_process' not in st.session_state:
    st.session_state['message_to_process'] = ''
if 'send_button_pressed' not in st.session_state:
    st.session_state['send_button_pressed'] = False
if 'last_user_message' not in st.session_state:
    st.session_state['last_user_message'] = ''
    
#Streamlit App Title
st.markdown(
    """
    <style>
        .banner {
            background-color: #f63366; /* Deep pink background */
            color: white;
            padding: 20px 60px; /* More padding for a larger banner */
            border-radius: 20px; /* Rounded corners */
            position: relative;
            overflow: hidden;
            font-size: 3em; /* Larger font size for the title */
            font-weight: bold; /* Bold font weight for the title */
            text-align: center;
            line-height: 1.2; /* Adjust line height for better readability */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* A subtle shadow for depth */
        }
        .banner:before, .banner:after {
            content: "🎓"; /* Graduation cap emojis */
            position: absolute;
            font-size: 3em; /* Larger emojis */
            top: 50%;
            transform: translate(-50%, -50%);
        }
        .banner:before {
            left: 20px; /* Position emoji to the left */
        }
        .banner:after {
            right: 20px; /* Position emoji to the right */
            transform: translate(50%, -50%);
        }
        /* Adding a font from Google Fonts for better typography */
        @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
        .banner {
            font-family: 'Fredoka One', cursive; /* Apply the custom font */
        }
    </style>
    <div class="banner">Study Buddy</div>
    """,
    unsafe_allow_html=True
)


def create_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Fetch student info by email
def get_student_by_email(email):
    conn = create_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE StudentEmail = %s", (email,))
        student = cursor.fetchone()
        conn.close()
        return student

# Fetch first nudge assigned to the student
def fetch_nudges_for_student(student_id):
    conn = create_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT n.NudgeID, n.NudgeText, p.PromptID
            FROM Nudges n
            INNER JOIN Prompts p ON n.PromptID = p.PromptID
            WHERE p.StudentID = %s
            """
            cursor.execute(query, (student_id,))
            nudges = cursor.fetchall()
        except mysql.connector.Error as e:
            st.error(f"Failed to fetch nudges: {e}")
        finally:
            conn.close()
    print("Fetched nudges:", nudges)  # Debugging line
    return nudges


# Function to log student's request for personal milestones
def get_personal_milestones(student_id):
    conn = create_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT cm.CWMilestoneDesc, cm.CWDueDate
            FROM CWMilestones cm
            JOIN CWMilestonesStudent cms ON cm.CWMilestoneID = cms.CWMilestoneID
            WHERE cms.StudentID = %s
            ORDER BY cm.CWDueDate ASC
        """, (student_id,))
        milestones = cursor.fetchall()
        conn.close()
        return milestones

# Formatting function for milestones
def format_milestones(milestones):
    if not milestones:
        return "You have no milestones."
    response = "Here are your milestones:\n"
    for milestone in milestones:
        due_date = milestone['CWDueDate'].strftime('%Y-%m-%d')
        response += f"- {milestone['CWMilestoneDesc']} due by {due_date}\n"
    return response

# Function to log the display of a nudge
def log_nudge(nudge_id, student_id, prompt_id):
    conn = create_db_connection()
    if conn:
        cursor = conn.cursor()
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Check if the nudge has already been logged for the student
        cursor.execute("SELECT COUNT(*) FROM NudgeLog WHERE NudgeID = %s AND StudentID = %s", (nudge_id, student_id))
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Nudge has not been logged yet, proceed with insertion
            cursor.execute("INSERT INTO NudgeLog (NudgeID, StudentID, PromptID, NudgeDateTime) VALUES (%s, %s, %s, %s)", (nudge_id, student_id, prompt_id, current_datetime))
            conn.commit()
            st.success("Nudge logged successfully.")
        else:
            st.warning("Nudge already logged for this student.")
        
        conn.close()

def display_nudge(nudge):
    if nudge and isinstance(nudge, dict):  # Check if nudge is a dictionary
        with st.sidebar:
            st.warning("Nudge Alert!")
            st.info(nudge.get('NudgeText', 'No text available'))  # Use .get() for safer access
            # Optionally, log the nudge display if required
            # This could involve updating the `log_nudge` function or similar logic

# Function to display chat messages with avatars
def display_chat_messages():
    for idx, msg in enumerate(st.session_state['messages']):
        avatar = USER_AVATAR if msg['sender'] == 'You' else BOT_AVATAR
        # Use Markdown to display messages with bold text
        if msg['sender'] == 'You':
            st.markdown(f"{avatar} **You**: {msg['text']}")
        else:
            st.markdown(f"{avatar} **Agent**: {msg['text']}")

        # Show feedback UI for agent messages
        if msg['sender'] == 'Agent':
            feedback_key = f"feedback_{msg['id']}"  # Unique key for feedback state
            chosen_feedback = st.radio("Was this response helpful?", ('Yes', 'Somewhat', 'No'), key=feedback_key)
            
            submit_key = f"submit_{msg['id']}"
            if st.button('Submit Feedback', key=submit_key):
                # Log feedback using the unique message ID
                if log_feedback(st.session_state['student_info']['StudentID'], chosen_feedback, msg['id']):
                    st.success("Thank you for your feedback!")
                else:
                    st.error("Feedback submission failed. Please try again.")

# Improved function to determine the intent of the message and trigger nudges accordingly
def trigger_nudge_based_on_keywords(user_message, student_id):
    """Trigger and display nudges based on the content of the user message."""
    keywords_for_nudge_trigger = ["help", "worried","overwhelmed","amotivated","confused about","stress",
                                  "don't understand", "due date", "struggling", "difficult"]
    if any(keyword in user_message.lower() for keyword in keywords_for_nudge_trigger):
        current_index = st.session_state.get('current_nudge_index', 0)
        nudges = st.session_state.get('nudges', [])
        if nudges:
            if current_index >= len(nudges):
                # Reset the index to 0 when it reaches the end of the nudges list
                current_index = 0
            nudge_to_display = nudges[current_index]
            display_nudge(nudge_to_display)
            # Update the index for the next nudge
            st.session_state['current_nudge_index'] = current_index + 1



# Sidebar Functionality
def sidebar_prompts(student_id):
    with st.sidebar:
        st.write("Suggestions")
        prompts = [
            "What are my upcoming deadlines?",
            "Do you have any study tips for preparing for exams?",
            "What milestones do I need to achieve this semester?",
            "Do you have any tips for managing stress during upcoming submissions?"
        ]
        
        # Iterate through each prompt and create a button in the sidebar for it
        for prompt in prompts:
            if st.button(prompt):
                process_user_message(prompt, student_id)
# Function to consistently populate the sidebar
def populate_sidebar():
    with st.sidebar:
        st.write("Welcome to the Chatbot")
        # Example: Display the first nudge if not shown
        if not st.session_state.get('first_nudge_shown', False) and st.session_state['nudges']:
            display_nudge(st.session_state['nudges'][0])
            # Optionally update the session state if needed
            st.session_state['first_nudge_shown'] = True
        # Example: Dynamically display additional nudges or messages based on session state
        if 'additional_message' in st.session_state:
            st.write(st.session_state['additional_message'])

def is_educational_query(query):
    # Patterns that are clearly educational
    educational_patterns = [
    'data visualization techniques', 'computer engineering fundamentals',
    'machine learning algorithms', 'neural network architecture',
    'stress management for exams', 'database management systems',
    'sql database optimization', 'mysql performance tuning',
    'relational database design', 'noSQL databases',
    'big data analytics', 'cloud computing services',
    'internet of things applications', 'blockchain technology',
    'quantum computing basics', 'cybersecurity measures',
    'ethical hacking strategies', 'artificial intelligence applications',
    'web development frameworks', 'mobile app development',
    'network security protocols', 'software testing methodologies',
    'operating systems concepts', 'distributed computing challenges',
    'parallel processing', 'bioinformatics tools',
    'computational physics models', 'mathematical modeling techniques',
    'statistical analysis methods', 'linear algebra in data science',
    'calculus for engineers', 'discrete mathematics for computer science',
    'digital signal processing', 'embedded systems design',
    'VLSI circuit design', 'wireless communication systems',
    'digital electronics', 'power electronics',
    'computer graphics and visualization', 'game development processes',
    'UI/UX design principles', 'object-oriented programming',
    'functional programming basics', 'version control systems',
    'software project management', 'agile and scrum methodologies',
    'educational technology tools', 'e-learning platforms',
    'virtual reality in education', 'augmented reality development',
    'data mining and warehousing', 'natural language processing',
    'robotics and automation', 'computer vision applications',
    'cloud infrastructure management', 'IT service management',
    'network configuration', 'operational research','computer engineering','DBMS','Dataset Acquisition and Preprocessing',
'CNN Architecture Design','Model Training and Optimization','Final Evaluation and Report Submission','Literature Review on CNNs',
'Data Labelling and Augmentation','CNN Model Training','Performance Analysis and Documentation','Database Schema Design','Implementation of SQL Queries',
'Data Integrity and Security Measures','Project Presentation Preparation','Advanced SQL Functions and Indexing','Stored Procedures and Trigger Creation',
'Performance Tuning and Optimization','Comprehensive Project Report','Data Exploration and Pattern Identification','Creation of Visualisation Mock-ups',
'User Experience Testing','Final Visualisation and Report Submission','Complex Data Analysis','Visual Encoding Strategies','Drafting Visualization Layout','Final Presentation and Submission','exams',
'study', 'exam', 'homework', 'assignment', 'course', 'lecture', 'tutorial',
'education', 'university', 'college', 'school', 'learning', 'motivation',
'stress', 'deadline', 'time management', 'focus', 'concentration',
'mental health', 'well-being', 'anxiety', 'depression', 'support',
'guidance', 'advice', 'tips','data acquisition',
        # Existing technical and educational terms
        'deep learning', 'information management for engineering', 'data visualisation', 'lab',
        'medical imaging', 'tumour classification', 'segmentation', 'image classification', 'cnn',
        'convolutional neural networks', 'dataset acquisition', 'preprocessing', 'architecture design',
        'model training', 'optimization', 'evaluation', 'literature review', 'data labelling', 'augmentation',
        'performance analysis', 'documentation', 'sql project', 'database schema design', 'sql queries',
        'data integrity', 'security measures', 'project presentation', 'advanced sql functions', 'indexing',
        'stored procedures', 'trigger creation', 'performance tuning', 'visualisation analysis and design',
        'addressing complexity', 'data exploration', 'pattern identification', 'creation of visualisation mock-ups',
        'user experience testing', 'final visualisation', 'complex data analysis', 'visual encoding strategies',
        'drafting visualization layout', 'final presentation', 'algorithm', 'data structure', 'software engineering',
        'networking', 'computer architecture', 'operating systems', 'database management', 'machine learning',
        'artificial intelligence', 'cybersecurity', 'cloud computing', 'iot', 'internet of things', 'blockchain',
        'quantum computing', 'big data', 'analytics', 'programming', 'coding', 'java', 'python', 'c++', 'ruby',
        'javascript', 'web development', 'app development', 'network security', 'operational research',
        'ethical hacking', 'cloud services', 'aws', 'azure', 'google cloud', 'virtual reality', 'augmented reality',
        'machine vision', 'robotics', 'drones', 'data mining', 'natural language processing', 'nlp',
        'computer graphics', 'game development', 'ui ux design', 'operating system design', 'compiler design',
        'distributed systems', 'parallel computing', 'quantum programming', 'bioinformatics', 'computational physics',
        'mathematical modeling', 'statistics', 'linear algebra', 'calculus', 'discrete mathematics', 'signal processing',
        'microprocessors', 'embedded systems', 'vlsi design', 'wireless communication', 'mobile computing',
        'digital electronics', 'power electronics',

        # Added general academic terms
        'submission', 'coursework', 'milestones', 'works', 'assignment', 'project', 'research', 'thesis', 'dissertation',
        'paper', 'study', 'exam', 'test', 'quiz', 'review', 'group work', 'presentation', 'lecture', 'tutorial',
        'seminar', 'workshop', 'lab session', 'practical', 'report', 'case study', 'peer review', 'feedback',
        'grade', 'mark', 'score', 'study guide', 'syllabus', 'curriculum', 'educational resource', 'textbook',
        'publication', 'journal', 'article', 'conference', 'symposium', 'academic', 'scholarly', 'peer-reviewed',
        'credit hours', 'degree requirements', 'major', 'minor', 'field of study', 'specialization', 'concentration',
        'academic advisor', 'faculty', 'department', 'scholarship', 'fellowship', 'grant', 'tuition', 'financial aid',
        'enrollment', 'registration', 'admission', 'application', 'orientation', 'commencement', 'graduation','deadlines'
]

    
    # Direct match from expanded educational patterns
    if any(pattern in query.lower() for pattern in educational_patterns):
        return True

    # Fallback mechanism for uncaught queries, maintaining OpenAI API calls
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant skilled in recognizing educational topics and explaining them which are related to any field of study may it be technology,computers,jobs,internships,computer science,computer engineering, data analytics or any other subject of any domain which you know about."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=200
            
        )
        answer = response.choices[0].message['content'].strip().lower()
        return "yes" in answer
    except Exception as e:
        print(f"OpenAI API call error: {e}")
        return False  # In the event of an API error, conservatively assume non-educational

def fetch_subject_specific_deadlines(student_id, subject_query):
    """
    Fetch deadlines for specific subjects based on the student's query.
    This function searches for personalized coursework related to the subject mentioned in the query
    and returns relevant milestones for the specific student.
    """
    conn = create_db_connection()
    deadlines = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT cm.CWMilestoneDesc, cm.CWDueDate, cw.CourseWorkDesc
            FROM CWMilestones cm
            JOIN CWMilestonesStudent cms ON cm.CWMilestoneID = cms.CWMilestoneID
            JOIN CourseWork cw ON cm.CourseWorkID = cw.CourseWorkID
            JOIN courses c ON cw.CourseID = c.CourseID
            WHERE cms.StudentID = %s AND c.CourseDesc LIKE %s
            ORDER BY cm.CWDueDate ASC
            """
            cursor.execute(query, (student_id, '%' + subject_query + '%',))
            deadlines = cursor.fetchall()
        except mysql.connector.Error as e:
            st.error(f"Failed to fetch subject-specific deadlines: {e}")
        finally:
            conn.close()
    return deadlines

def format_subject_specific_deadlines(deadlines):
    """
    Format the fetched subject-specific deadlines into a readable string.
    """
    if not deadlines:
        return "You have no specific deadlines for this subject."
    response = "Here are your specific deadlines for the requested subject:\n"
    for deadline in deadlines:
        due_date = deadline['CWDueDate'].strftime('%Y-%m-%d')
        response += f"- {deadline['CourseWorkDesc']} - {deadline['CWMilestoneDesc']} is due by {due_date}\n"
    return response


def get_student_course_info(student_id):
    conn = create_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT c.CourseDesc
            FROM students s
            JOIN courses c ON s.CourseID = c.CourseID
            WHERE s.StudentID = %s
            """
            cursor.execute(query, (student_id,))
            course_info = cursor.fetchone()
            if course_info:
                return f"You are enrolled in {course_info['CourseDesc']}."
            else:
                return "I couldn't find your course information."
        except mysql.connector.Error as e:
            st.error(f"Failed to fetch student's course information: {e}")
            return "There was an error fetching your course information."
        finally:
            conn.close()
    else:
        return "Unable to connect to the database to retrieve your course information."

def fetch_coursework_and_milestones(student_id):
    """
    Fetch courseworks and their milestones for a specific student.
    """
    conn = create_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT cw.CourseWorkDesc, cm.CWMilestoneDesc
        FROM CWMilestones cm
        JOIN CWMilestonesStudent cms ON cm.CWMilestoneID = cms.CWMilestoneID
        JOIN CourseWork cw ON cm.CourseWorkID = cw.CourseWorkID
        WHERE cms.StudentID = %s
        ORDER BY cw.CourseWorkDesc, cm.CWDueDate
        """
        cursor.execute(query, (student_id,))
        milestones_data = cursor.fetchall()
        conn.close()
        return milestones_data
    
def format_coursework_and_milestones(milestones_data):
    """
    Format the fetched coursework and milestones into a readable string.
    """
    if not milestones_data:
        return "You have no courseworks or milestones assigned."
    
    # Organizing coursework and milestones
    coursework_milestones = {}
    for row in milestones_data:
        if row['CourseWorkDesc'] not in coursework_milestones:
            coursework_milestones[row['CourseWorkDesc']] = []
        coursework_milestones[row['CourseWorkDesc']].append(row['CWMilestoneDesc'])
    
    # Formatting the response
    response = "Here are your courseworks and their milestones:\n"
    for coursework, milestones in coursework_milestones.items():
        response += f"- {coursework}: " + ", ".join(milestones) + "\n"
    
    return response
# Function to log feedback in the database
# Feedback submission function
def log_feedback(student_id, feedback, message_id):
    conn = None
    try:
        conn = create_db_connection()  # Ensure this function correctly establishes a DB connection
        if conn is not None:
            cursor = conn.cursor()
            # Adjust your SQL query to include the message_id
            query = "INSERT INTO feedback (student_id, feedback, message_id, timestamp) VALUES (%s, %s, %s, NOW())"
            cursor.execute(query, (student_id, feedback, message_id))
            conn.commit()
            return True
        else:
            st.error("Failed to connect to the database.")
    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")  # Display any error encountered during DB operations
    finally:
        if conn:
            conn.close()
    return False

# Improved function to process user messages
def process_user_message(user_message, student_id):
    # Detect if the student is asking for their coursework and milestones
    # Generate a unique identifier for this message
    message_id = str(uuid.uuid4())
    if "my courseworks" in user_message.lower() or "my milestones" in user_message.lower():
        # print("Fetching courseworks and milestones...")  # Debugging
        milestones_data = fetch_coursework_and_milestones(student_id)
        response = format_coursework_and_milestones(milestones_data)
        # print(f"Response: {response}")  # Debugging
    # Check for personal information queries such as course information
    elif 'my course' in user_message.lower() or 'which course am i enrolled in' in user_message.lower():
        response = get_student_course_info(student_id)
    elif 'milestone' in user_message.lower() or 'deadline' in user_message.lower():
        milestones = get_personal_milestones(student_id)
        response = format_milestones(milestones)
    elif 'deadline for' in user_message.lower():
        subject_query = user_message.lower().split('deadline for', 1)[1].strip()
        deadlines = fetch_subject_specific_deadlines(student_id, subject_query)
        response = format_subject_specific_deadlines(deadlines)
    elif is_educational_query(user_message):
        # Handle educational, motivational, coursework-related queries with GPT
        try:
            openai.api_key = OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant knowledgeable in education,computer science,jobs,internships,computer engineering, technology,any study field,any academic related questions, including study tips, stress management, and student motivation."},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=300
            )
            response = response.choices[0].message['content'].strip()
        except Exception as e:
            response = "I'm having trouble processing your request right now. Please try again later."
    else:
        # For non-educational queries
        response = "I'm here to assist with educational queries and support related to your studies. Please ask something related to your coursework or educational well-being."

    # Display responses in the chat
    st.session_state['messages'].append({'sender': 'You', 'text': user_message, 'id': message_id})
    st.session_state['messages'].append({'sender': 'Agent', 'text': response, 'id': message_id})

    # Trigger nudges if applicable
    trigger_nudge_based_on_keywords(user_message, student_id)



# Sidebar Functionality
def sidebar_prompts(student_id):
    with st.sidebar:
        st.write("Suggestions")
        prompts = [
            "What are my upcoming deadlines?",
            "Do you have any study tips for preparing for exams?",
            "What milestones do I need to achieve this semester?",
            "Do you have any tips for managing stress during upcoming submissions?"
        ]
        
        # Iterate through each prompt and create a button in the sidebar for it
        for prompt in prompts:
            if st.button(prompt):
                process_user_message(prompt, student_id)
# # Function to collect and process feedback
# def collect_and_process_feedback(student_id):
#     feedback_options = ["Yes", "Somewhat", "No"]
#     selected_feedback = st.radio("Was this response helpful?", feedback_options, key="feedback")

#     if st.button('Submit Feedback'):
#         if log_feedback(student_id, selected_feedback):  # Your existing log_feedback function
#             st.success("Thank you for your feedback!")
#         else:
#             st.error("Feedback submission failed. Please try again.")


# Adjusted User login functionality to display the first nudge upon login
if not st.session_state.get('login_successful', False):
    with st.container():
        st.session_state['student_email'] = st.text_input("Enter your student email", key="unique_email_input")
        if st.button("Login", key="unique_login_button"):
            student_info = get_student_by_email(st.session_state['student_email'])
            if student_info:
                st.session_state['student_info'] = student_info
                st.session_state['login_successful'] = True

                student_name = student_info.get('StudentName', 'there')
                st.markdown(f"""
                    <div style="
                        margin: 1em;
                        background-color: #2c3e50; /* Dark blue background */
                        color: #ecf0f1; /* Light grey text for contrast */
                        padding: 2em 4em; /* Padding for overall indentation */
                        border-radius: 10px;
                        border-left: 5px solid #3498db; /* Accent color */
                        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                        text-align: left; /* Align text to the left */
                        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
                    ">
                        <h2 style="margin: 0; font-size: 2em; font-weight: bold;">Welcome, <span style="color: #ecf0f1;">{student_name}</span>!</h2>
                        <p style="font-size: 1.25em; margin-top: 0.5em; margin-bottom: 0.5em;">I'm your Study Buddy 🎓, ready to help you with your study queries.</p>
                        <p style="font-size: 1.25em; margin: 0;">Go ahead and ask me any question about your academics and it's related issues!</p>
                    </div>
                """, unsafe_allow_html=True)

                # Fetch and display nudges if any
                nudges = fetch_nudges_for_student(student_info['StudentID'])
                if nudges and not st.session_state['first_nudge_shown']:
                    display_nudge(nudges[0])  # Display the first nudge immediately
                    st.session_state['first_nudge_shown'] = True  # Mark the first nudge as shown
                    st.session_state['nudges'] = nudges[1:]  # Store remaining nudges
                    st.session_state['current_nudge_index'] = 0  # Reset index for next nudges
            else:
                st.error("No student found with this email.")
                

# Chat functionality with adjustments for form handling
if st.session_state.get('login_successful', False):
    student_id = st.session_state['student_info']['StudentID']
    # Call the function to display prompts in the sidebar
    populate_sidebar()
    sidebar_prompts(student_id)

    # Process the message if the send button has been pressed
    if 'send_button_pressed' in st.session_state and st.session_state['send_button_pressed']:
        user_message = st.session_state['last_user_message']
        process_user_message(user_message, student_id)

    chat_placeholder = st.empty()

    # Handling user input at the bottom
    with st.form("chat_form", clear_on_submit=True):
        user_message_input = st.text_input("Type your message here...", key="user_message")
        send_button = st.form_submit_button("Send")

    # Process the message if the send button has been pressed
    if send_button and user_message_input:
        # Assuming you have a function `process_user_message` defined somewhere
        process_user_message(user_message_input, student_id)

        user_message_input = ""
    # Now use the chat_placeholder to display the messages
    with chat_placeholder.container():
        # Display all messages
        display_chat_messages()



# Assuming the login check and sidebar population are done above


# Function to handle processing and displaying messages








# Make sure to define display_chat_messages() and other necessary functions above this logic










# Make sure to call display_chat_messages() again if needed to refresh the chat display




    
        # # Check if there are any nudges to display and if a message has just been sent
        #     if st.session_state['nudges']:
        #         # Display the next nudge from the list
        #         current_index = st.session_state['current_nudge_index']
        #         display_nudge(st.session_state['nudges'][current_index])
        #         # Update the index for the next nudge
        #         st.session_state['current_nudge_index'] = (current_index + 1) % len(st.session_state['nudges'])
        # with st.sidebar:
        #     # Display the sidebar content such as user info or other static content
        #     st.write("Sidebar content goes here...")


            # # Rerun the Streamlit script to update the chat history
        # st.experimental_rerun()



# Clear input box after sending message
#         st.text_input("Type your message here...", key="user_message_input", value="")
        
        # Call show_nudges in your main code to display nudges
        # show_nudges()

        # # Clear the user_message_input box after the message is sent
        # if 'user_message_input' in st.session_state:
        #     st.session_state['user_message_input'] = ""
            
        # Clear input box after sending message
        # st.text_input("Type your message here...", key="user_message_input", value="")
        # Display updated chat messages
        # display_chat_messages()  
# # Clear the user_message_input box after the message is sent
# if 'user_message_input' in st.session_state:
#     st.session_state['user_message_input'] = ""

# # Save chat history
# st.query_params['messages'] = st.session_state['messages']

# def is_educational(query):
#     """
#     Check if the query is educational based on the presence of predefined keywords.
#     """
#     educational_keywords = [
#         # Existing technical and educational terms
#         'deep learning', 'information management for engineering', 'data visualisation', 'lab',
#         'medical imaging', 'tumour classification', 'segmentation', 'image classification', 'cnn',
#         'convolutional neural networks', 'dataset acquisition', 'preprocessing', 'architecture design',
#         'model training', 'optimization', 'evaluation', 'literature review', 'data labelling', 'augmentation',
#         'performance analysis', 'documentation', 'sql project', 'database schema design', 'sql queries',
#         'data integrity', 'security measures', 'project presentation', 'advanced sql functions', 'indexing',
#         'stored procedures', 'trigger creation', 'performance tuning', 'visualisation analysis and design',
#         'addressing complexity', 'data exploration', 'pattern identification', 'creation of visualisation mock-ups',
#         'user experience testing', 'final visualisation', 'complex data analysis', 'visual encoding strategies',
#         'drafting visualization layout', 'final presentation', 'algorithm', 'data structure', 'software engineering',
#         'networking', 'computer architecture', 'operating systems', 'database management', 'machine learning',
#         'artificial intelligence', 'cybersecurity', 'cloud computing', 'iot', 'internet of things', 'blockchain',
#         'quantum computing', 'big data', 'analytics', 'programming', 'coding', 'java', 'python', 'c++', 'ruby',
#         'javascript', 'web development', 'app development', 'network security', 'operational research',
#         'ethical hacking', 'cloud services', 'aws', 'azure', 'google cloud', 'virtual reality', 'augmented reality',
#         'machine vision', 'robotics', 'drones', 'data mining', 'natural language processing', 'nlp',
#         'computer graphics', 'game development', 'ui ux design', 'operating system design', 'compiler design',
#         'distributed systems', 'parallel computing', 'quantum programming', 'bioinformatics', 'computational physics',
#         'mathematical modeling', 'statistics', 'linear algebra', 'calculus', 'discrete mathematics', 'signal processing',
#         'microprocessors', 'embedded systems', 'vlsi design', 'wireless communication', 'mobile computing',
#         'digital electronics', 'power electronics',

#         # Added general academic terms
#         'submission', 'coursework', 'milestones', 'works', 'assignment', 'project', 'research', 'thesis', 'dissertation',
#         'paper', 'study', 'exam', 'test', 'quiz', 'review', 'group work', 'presentation', 'lecture', 'tutorial',
#         'seminar', 'workshop', 'lab session', 'practical', 'report', 'case study', 'peer review', 'feedback',
#         'grade', 'mark', 'score', 'study guide', 'syllabus', 'curriculum', 'educational resource', 'textbook',
#         'publication', 'journal', 'article', 'conference', 'symposium', 'academic', 'scholarly', 'peer-reviewed',
#         'credit hours', 'degree requirements', 'major', 'minor', 'field of study', 'specialization', 'concentration',
#         'academic advisor', 'faculty', 'department', 'scholarship', 'fellowship', 'grant', 'tuition', 'financial aid',
#         'enrollment', 'registration', 'admission', 'application', 'orientation', 'commencement', 'graduation','deadlines'
#     ]
#     return any(keyword.lower() in query.lower() for keyword in educational_keywords)