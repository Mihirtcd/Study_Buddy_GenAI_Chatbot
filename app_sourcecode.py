

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
        
# Steps to run the program and have the chatbot working:
# 1.Need to have the .env file ready as follows:
# OPENAI_API_KEY="xxxxxxxxxx"
# DB_HOST="localhost"
# DB_USER="root"
# DB_PASS="xxcxxxxxx"
# DB_NAME="Nudge_Based_MotivationalAgent"
# 2.Have the simulated database prepared using the sql script code i have written below.
# 3.need to follow requirements.txt file:
# streamlit
# python-dotenv
# openai
# 4.after all these steps are complete just run this code script by typing:
# (streamlit run app.py) in your system.[name this code script as app.py]


# SQL Script containing code for MySQL database of Study-Buddy
'''
CREATE DATABASE IF NOT EXISTS Nudge_Based_MotivationalAgent;first write this and then move forward.


CREATE TABLE students (
StudentID INT PRIMARY KEY,
StudentName VARCHAR(255),
PerformanceLevel DECIMAL(3,2),
CourseID VARCHAR(20),
MotivationLevelForCW DECIMAL(3,2),
StudentEmail VARCHAR(255)
);
INSERT INTO students (StudentID, StudentName, PerformanceLevel, CourseID,
MotivationLevelForCW, StudentEmail) VALUES
(21355017, 'Yashraj Saluja', 6.5, 'EEU44C16-202324', 7.5, 'salujay@tcd.ie'),
(21355018, 'Deepak Bhatt', 5.25, 'CSU44D01-202324', 5, 'bhattdeepak780@gmail.com'),
(21355019, 'Sanaya Gupta', 7.5, 'EEU44C16-202324', 8, 'Guptas6@tcd.ie'),
(21355020, 'Mohak Bhatia', 4.75, 'CSU44056-202324', 5.5, ‘MBHATIA@tcd.ie');
CREATE TABLE courses (
CourseID VARCHAR(20) PRIMARY KEY,
CourseDesc VARCHAR(255) NOT NULL
);
INSERT INTO courses (CourseID, CourseDesc) VALUES
('EEU44C16-202324', 'DEEP LEARNING AND ITS APPLICATIONS'),
('CSU44D01-202324', 'INFORMATION MANAGEMENT FOR ENGINEERING'),
('CSU44056-202324', 'DATA VISUALISATION');
CREATE TABLE CourseWork (
CourseWorkID VARCHAR(10) PRIMARY KEY,
CourseWorkDesc varchar(500) NOT NULL,
CourseID VARCHAR(20) NOT NULL,
FOREIGN KEY (CourseID) REFERENCES courses(CourseID)
);
INSERT INTO CourseWork (CourseWorkID, CourseWorkDesc, CourseID) VALUES
('CW001', 'Lab 6: a medical imaging problem with tumour classification and segmentation.',
'EEU44C16-202324'),
('CW002', 'Lab 5: Image classification using CNN', 'EEU44C16-202324'),
('CW003', 'SQL Project-1', 'CSU44D01-202324'),
('CW004', 'SQL Project-2', 'CSU44D01-202324'),
('CW005', 'Assignment 3 - Visualisation Analysis and Design', 'CSU44056-202324'),
('CW006', 'Assignment 4 - Addressing Complexity', ‘CSU44056-202324');
CREATE TABLE CWMilestones (
CWMilestoneID VARCHAR(10) PRIMARY KEY,
CWMilestoneDesc Varchar(255) not null,
CWDueDate DATE not null,
CWMilestoneSequence INT,
CourseWorkID VARCHAR(10) not null,
FOREIGN KEY (CourseWorkID) REFERENCES CourseWork(CourseWorkID)
);
INSERT INTO CWMilestones (CWMilestoneID, CWMilestoneDesc, CWDueDate,
CWMilestoneSequence, CourseWorkID) VALUES
('CWM001', 'Dataset Acquisition and Preprocessing', '2024-03-10', 1, 'CW001'),
('CWM002', 'CNN Architecture Design', '2024-03-24', 2, 'CW001'),
('CWM003', 'Model Training and Optimization', '2024-04-07', 3, 'CW001'),
('CWM004', 'Final Evaluation and Report Submission', '2024-04-21', 4, 'CW001'),
('CWM005', 'Literature Review on CNNs', '2024-03-15', 1, 'CW002'),
('CWM006', 'Data Labelling and Augmentation', '2024-03-29', 2, 'CW002'),
('CWM007', 'CNN Model Training', '2024-04-12', 3, 'CW002'),
('CWM008', 'Performance Analysis and Documentation', '2024-04-26', 4, 'CW002'),
('CWM009', 'Database Schema Design', '2024-03-11', 1, 'CW003'),
('CWM0010', 'Implementation of SQL Queries', '2024-03-25', 2, 'CW003'),
('CWM0011', 'Data Integrity and Security Measures', '2024-04-08', 3, 'CW003'),
('CWM0012', 'Project Presentation Preparation', '2024-04-22', 4, 'CW003'),
('CWM0013', 'Advanced SQL Functions and Indexing', '2024-03-18', 1, 'CW004'),
('CWM0014', 'Stored Procedures and Trigger Creation', '2024-04-01', 2, 'CW004'),
('CWM0015', 'Performance Tuning and Optimization', '2024-04-15', 3, 'CW004'),
('CWM0016', 'Comprehensive Project Report', '2024-04-29', 4, 'CW004'),
('CWM0017', 'Data Exploration and Pattern Identification', '2024-03-12', 1, 'CW005'),
('CWM0018', 'Creation of Visualisation Mock-ups', '2024-03-26', 2, 'CW005'),
('CWM0019', 'User Experience Testing', '2024-04-09', 3, 'CW005'),
('CWM0020', 'Final Visualisation and Report Submission', '2024-04-23', 4, 'CW005'),
('CWM0021', 'Complex Data Analysis', '2024-03-15', 1, 'CW006'),
('CWM0022', 'Visual Encoding Strategies', '2024-03-29', 2, 'CW006'),
('CWM0023', 'Drafting Visualization Layout', '2024-04-05', 3, 'CW006'),
('CWM0024', 'Final Presentation and Submission', '2024-04-12', 4, ‘CW006');
CREATE TABLE CWMilestonesStudent (
CWMilestoneID VARCHAR(10),
CWDueDate DATE not null,
CWSubmitDate DATE not null,
CWMilestoneSequence INT,
CourseWorkID VARCHAR(10),
StudentID INT not null,
PRIMARY KEY (CWMilestoneID, StudentID),
FOREIGN KEY (CourseWorkID) REFERENCES CourseWork(CourseWorkID),
FOREIGN KEY (StudentID) REFERENCES students(StudentID)
);
INSERT INTO CWMilestonesStudent (CWMilestoneID, CWDueDate, CWSubmitDate,
CWMilestoneSequence, CourseWorkID, StudentID) VALUES
('CWM001', '2024-03-10', '2024-03-05', 1, 'CW001', 21355017),
('CWM002', '2024-03-17', '2024-03-12', 2, 'CW001', 21355017),
('CWM003', '2024-03-24', '2024-03-19', 3, 'CW001', 21355017),
('CWM004', '2024-03-31', '2024-03-26', 4, 'CW001', 21355017),
('CWM005', '2024-04-07', '2024-04-02', 1, 'CW002', 21355017),
('CWM006', '2024-04-14', '2024-04-09', 2, 'CW002', 21355017),
('CWM007', '2024-04-21', '2024-04-16', 3, 'CW002', 21355017),
('CWM008', '2024-04-28', '2024-04-23', 4, 'CW002', 21355017),
('CWM001', '2024-03-10', '2024-03-05', 1, 'CW001', 21355019),
('CWM002', '2024-03-17', '2024-03-12', 2, 'CW001', 21355019),
('CWM003', '2024-03-24', '2024-03-19', 3, 'CW001', 21355019),
('CWM004', '2024-03-31', '2024-03-26', 4, 'CW001', 21355019),
('CWM005', '2024-04-07', '2024-04-02', 1, 'CW002', 21355019),
('CWM006', '2024-04-14', '2024-04-09', 2, 'CW002', 21355019),
('CWM007', '2024-04-21', '2024-04-16', 3, 'CW002', 21355019),
('CWM008', '2024-04-28', '2024-04-23', 4, 'CW002', 21355019),
('CWM009', '2024-03-11', '2024-03-10', 1, 'CW003', 21355018),
('CWM0010', '2024-03-25', '2024-03-24', 2, 'CW003', 21355018),
('CWM0011', '2024-04-08', '2024-04-07', 3, 'CW003', 21355018),
('CWM0012', '2024-04-22', '2024-04-21', 4, 'CW003', 21355018),
('CWM0013', '2024-03-18', '2024-03-17', 1, 'CW004', 21355018),
('CWM0014', '2024-04-01', '2024-03-31', 2, 'CW004', 21355018),
('CWM0015', '2024-04-15', '2024-04-14', 3, 'CW004', 21355018),
('CWM0016', '2024-04-29', '2024-04-28', 4, 'CW004', 21355018),
('CWM0017', '2024-03-12', '2024-03-11', 1, 'CW005', 21355020),
('CWM0018', '2024-03-26', '2024-03-25', 2, 'CW005', 21355020),
('CWM0019', '2024-04-09', '2024-04-08', 3, 'CW005', 21355020),
('CWM0020', '2024-04-23', '2024-04-22', 4, 'CW005', 21355020),
('CWM0021', '2024-03-15', '2024-03-14', 1, 'CW006', 21355020),
('CWM0022', '2024-03-29', '2024-03-28', 2, 'CW006', 21355020),
('CWM0023', '2024-04-12', '2024-04-11', 3, 'CW006', 21355020),
('CWM0024', '2024-04-26', '2024-04-25', 4, 'CW006', 21355020);
CREATE TABLE Prompts (
PromptID VARCHAR(10) PRIMARY KEY,
PromptDesc TEXT,
CourseWorkID VARCHAR(10),
Remarks VARCHAR(255),
StudentID INT,
FOREIGN KEY (CourseWorkID) REFERENCES
CourseWork(CourseWorkID),
FOREIGN KEY (StudentID) REFERENCES
students(StudentID)
);
INSERT INTO Prompts (PromptID, PromptDesc, CourseWorkID,
Remarks, StudentID) VALUES
('P001', "Yashraj is doing well with his 'DEEP LEARNING
AND ITS APPLICATIONS' Lab 6 milestones. Encourage him to
keep up the excellent work and remind him that consistent
effort in data preprocessing will pay off as the 10-day
deadline approaches.", 'CW001', '10 days before M1
deadline', 21355017),
('P002', "With the model development milestone for Lab 6
due next week, let Yashraj know that his dedication is
impressive and that he's on the right track to succeed.",
'CW001', '7 days before M2 deadline', 21355017),
('P003', "As Yashraj prepares to finalize his model
evaluation for Lab 6, motivate him to give his best and
remind him that every detail counts with the deadline
just a day away.", 'CW001', '1 day before M3 deadline',
21355017),
('P004', "Yashraj is about to complete his Lab 6
assignment. Encourage him to cross the finish line with
confidence and to ensure all his hard work is reflected
in his final submission due tomorrow.", 'CW001', '1 day
before final submission', 21355017),
('P005', "Yashraj has been proactive with his CNN design
for Lab 5. Send him a motivational nudge to continue
refining his work and to keep the innovative spirit high
as the 10-day deadline looms.", 'CW002', '10 days before
M1 deadline', 21355017),
('P006', "The training setup deadline for Yashraj's Lab 5
project is approaching in a week. Encourage him to stay
focused, as his methodical approach is leading to
promising results.", 'CW002', '7 days before M2
deadline', 21355017),
('P007', "Yashraj's diligence in the Lab 5 hyperparameter
tuning is commendable. With the deadline coming up
tomorrow, motivate him to make the final adjustments for
optimal performance.", 'CW002', '1 day before M3
deadline', 21355017),
('P008', "It's the day before Yashraj's Lab 5 project
submission. Inspire him to take pride in his achievements
and to present his work with the assurance that comes
from thorough preparation.", 'CW002', '1 day before final
submission', 21355017),
('P009', "Deepak is lagging behind on the database schema
design for SQL Project-1. Encourage him to engage deeply
with the data relationships and provide substantial
support to uplift his understanding.", 'CW003', '10 days
before M1 deadline', 21355018),
('P010', "Deepak has not yet started on his SQL queries
for Project-1. Stress the importance of beginning this
task immediately and offer guidance to formulate precise
queries.", 'CW003', '14 days before M2 deadline',
21355018),
('P011', "As the data integrity milestone for SQL
Project-1 is fast approaching, remind Deepak of the
critical nature of this task. Offer strategies to secure
and validate his data accurately.", 'CW003', '18 days
before M3 deadline', 21355018),
('P012', "With the final presentation of SQL Project-1
nearing, Deepak requires a nudge to compile his findings
diligently. Emphasize the need for early preparation to
ensure a comprehensive presentation.", 'CW003', '21 days
before final submission', 21355018),
('P013', "Deepak's understanding of advanced SQL
functions in Project-2 needs reinforcing. Push him to
embrace this learning opportunity with enthusiasm and a
proactive approach.", 'CW004', '10 days before M1
deadline', 21355018),
('P014', "Deepak's progress on stored procedures for SQL
Project-2 is falling short. Urge him to refine his
procedures and triggers, ensuring they effectively
automate database operations.", 'CW004', '14 days before
M2 deadline', 21355018),
('P015', "The performance tuning milestone for SQL
Project-2 is crucial for Deepak. Motivate him to
prioritize this task, focusing on query optimization to
achieve peak performance.", 'CW004', '18 days before M3
deadline', 21355018),
('P016', "It's essential for Deepak to begin compiling
his report for SQL Project-2 well ahead of the deadline.
Encourage him to document each aspect of his project,
reflecting on his learnings and challenges.", 'CW004',
'21 days before final submission', 21355018),
('P017', "Deepak's immediate action is needed as the SQL
Project-1 schema design deadline is almost here. Offer
him substantial motivation to finalize his schema design
promptly.", 'CW003', '2 days before M1 deadline',
21355018),
('P018', "With SQL Project-1 query implementation due
shortly, Deepak requires an urgent reminder to accelerate
his work and focus intensely on crafting well-structured
queries.", 'CW003', '3 days before M2 deadline',
21355018),
('P019', "As SQL Project-2's advanced functions milestone
is upcoming, Deepak needs an urgent push to delve into
complex SQL functionalities and innovate his approach to
database management.", 'CW004', '2 days before M1
deadline', 21355018),
('P020', "Deepak is nearing the deadline for his SQL
Project-2 stored procedures milestone. Encourage him to
work diligently on perfecting his database triggers and
procedures.", 'CW004', '3 days before M2 deadline',
21355018),
('P021', "Sanaya's analytical approach in Lab 6 has been
impressive. Encourage her to keep up the meticulous data
preprocessing as the due date nears.", 'CW001', '1 week
before M1 deadline', 21355019),
('P022', "Sanaya's innovative ideas for the architecture
design milestone of Lab 6 are promising. Let's give her a
nudge to start crystallizing her vision into a solid
model architecture.", 'CW001', '5 days before M2
deadline', 21355019),
('P023', "As the optimization deadline for Lab 6 looms,
remind Sanaya that her keen eye for detail will serve her
well in refining the model to perfection.", 'CW001', '1
day before M3 deadline', 21355019),
('P024', "Sanaya's proactive engagement in Lab 5 has set
a solid foundation. A nudge to initiate the data
labelling ahead of schedule could further her progress.",
'CW002', '1 week before M1 deadline', 21355019),
('P025', "With the performance analysis milestone for Lab
5 due soon, Sanaya's ability to interpret data will be
key. Encourage her to start preparing her analysis
review.", 'CW002', '5 days before M2 deadline',
21355019),
('P026', "Sanaya's methodical work ethic will be crucial
for the upcoming model training in Lab 5. A reminder to
plan her training schedule could boost her efficiency.",
'CW002', '1 day before M3 deadline', 21355019),
('P027', "The final evaluation of Lab 6 is nearing, and
it's crucial for Sanaya to start preparing her
presentation and report. Encourage her to align her
findings with the coursework objectives.", 'CW001', '10
days before M4 deadline', 21355019),
('P028', "As Sanaya wraps up her work in Lab 5, a
reminder to be thorough in her performance documentation
will ensure she captures all her hard work and
insights.", 'CW002', '10 days before M4 deadline',
21355019),
('P029', "Mohak is showing a need for increased support
in visualisation concepts. Suggest reinforcing
foundational knowledge to build confidence.", 'CW005',
'14 days before M1 deadline', 21355020),
('P030', "Encourage Mohak to start early on the
'Visualisation Analysis and Design' assignment. Offer
resources to enhance his understanding of design
principles.", 'CW005', '10 days before M1 deadline',
21355020),
('P031', "As the deadline approaches, remind Mohak to
review visualisation best practices. Highlight the
importance of clear and concise data representation.",
'CW005', '5 days before M1 deadline', 21355020),
('P032', "Motivate Mohak to finalize his Assignment 3
with detailed attention to user feedback and data
accuracy. Stress the value of iterative improvement.",
'CW005', '1 day before M1 deadline', 21355020),
('P033', "With 'Addressing Complexity' on the horizon,
encourage Mohak to brainstorm creative ways to simplify
complex data for better understanding.", 'CW006', '14
days before M2 deadline', 21355020),
('P034', "Recommend that Mohak outlines his approach for
Assignment 4, focusing on clarity and structure. Offer
guidance on tackling complex datasets.", 'CW006', '10
days before M2 deadline', 21355020),
('P035', "Prompt Mohak to seek peer feedback on his
visualisation drafts to gain diverse perspectives and
improve his work before the submission.", 'CW006', '5
days before M2 deadline', 21355020),
('P036', "Encourage Mohak to do a final review of his
work for coherence and impact. Suggest he ensures his
visualisations tell a compelling story.", 'CW006', '1 day
before M2 deadline', 21355020),
('P037', "Review Mohak's recent coursework submissions.
If there are missed deadlines, we need to address this
immediately with an appropriate series of nudges.",
'CW005', 'After missed deadline', 21355020),
('P038', "Check Mohak's engagement with the coursework
material. His recent pattern of missed deadlines suggests
he might benefit from additional reminders and
resources.", 'CW005', 'Pattern of missed deadlines',
21355020),
('P039', "Mohak has missed a deadline. Let's ensure he
receives a nudge to reassess his schedule and prioritize
upcoming coursework tasks.", 'CW005', 'Immediate action
post deadline', 21355020),
('P040', "Monitor Mohak's interaction with the coursework
after the missed deadline to provide targeted nudges for
his course recovery plan.", 'CW006', 'Monitoring post
missed deadline', 21355020),
('P041', "Given Mohak's recent missed deadline, it's
crucial to send nudges that encourage him to communicate
any obstacles he's facing with his coursework.", 'CW006',
'Encouragement to communicate', 21355020);
CREATE TABLE Nudges (
NudgeID VARCHAR(10) PRIMARY KEY,
PromptID VARCHAR(10),
NudgeText TEXT,
Nudge4DeterioratingStudent BOOLEAN,
Nudge4ImprovingStudent BOOLEAN,
NudgeOccurrence VARCHAR(255),
CourseWorkID VARCHAR(10),
Remarks TEXT,
FOREIGN KEY (PromptID) REFERENCES Prompts(PromptID),
FOREIGN KEY (CourseWorkID) REFERENCES
CourseWork(CourseWorkID));
INSERT INTO Nudges (NudgeID, PromptID, NudgeText,
Nudge4DeterioratingStudent, Nudge4ImprovingStudent,
NudgeOccurrence, CourseWorkID, Remarks) VALUES
('N101', 'P001', "Yashraj, each step you've taken in Lab
6 brings you closer to mastery. Keep the energy high,
you're creating something great!", TRUE, FALSE, '10 days
before M1 deadline', 'CW001', 'Motivation for M1'),
('N102', 'P002', "The progress you're making on Lab 6's
model development is impressive, Yashraj! Each refinement
is a step towards excellence.", TRUE, FALSE, '7 days
before M2 deadline', 'CW001', 'Encouragement for M2'),
('N103', 'P003', "Your dedication to Lab 6 shines
through, Yashraj! With one day to model evaluation, your
hard work is about to pay off.", TRUE, FALSE, '1 day
before M3 deadline', 'CW001', 'Last push for M3'),
('N104', 'P004', "Yashraj, your Lab 6 journey culminates
tomorrow. Review your work with pride, and submit with
confidence!", TRUE, FALSE, '1 day before final
submission', 'CW001', 'Reminder for final check'),
('N105', 'P005', "Your innovative spirit is evident in
your Lab 5 CNN design, Yashraj. As you finalize your
design, remember that every challenge is an opportunity
to learn and grow.", TRUE, FALSE, '10 days before M1
deadline', 'CW002', 'Motivation for M1'),
('N106', 'P006', "One week to go, Yashraj, and your Lab 5
training setup is shaping up well. Keep tuning and
testing - your thoroughness will lead to success!", TRUE,
FALSE, '7 days before M2 deadline', 'CW002',
'Encouragement for M2'),
('N107', 'P007', "Hyperparameter tuning is an art, and
Yashraj, you're the artist. With one day left for Lab 5,
it's time to put the finishing touches on your
masterpiece.", TRUE, FALSE, '1 day before M3 deadline',
'CW002', 'Last push for M3'),
('N108', 'P008', "It's time to shine, Yashraj! Your hard
work for Lab 5 culminates in tomorrow's submission. Go
over your project, knowing each part reflects your growth
and learning.", TRUE, FALSE, '1 day before final
submission', 'CW002', 'Reminder for final check'),
('N109', 'P009', "Deepak, your potential is clear, and
now is the time to harness it. Dive into the database
schema with determination. We believe in you!", TRUE,
FALSE, '10 days before M1 deadline', 'CW003', 'High
urgency for schema design'),
('N110', 'P010', "You've got this, Deepak! Structured
queries are the backbone of your project. Start shaping
them today, and you'll see progress in no time.", TRUE,
FALSE, '14 days before M2 deadline', 'CW003',
'Encouragement for query formulation'),
('N111', 'P011', "The clock is ticking, and your focus on
data integrity is more important than ever. Let's ensure
your data is secure and accurate, step by step.", TRUE,
FALSE, '18 days before M3 deadline', 'CW003', 'Urgent
action for data integrity'),
('N112', 'P012', "It's presentation time soon! Gather
your insights and present them with the clarity they
deserve. Your hard work will speak for itself.", TRUE,
FALSE, '21 days before final submission', 'CW003',
'Motivation for final presentation prep'),
('N113', 'P013', "Advanced SQL functions are your next
conquest. Approach them with curiosity and the drive to
solve problems, and you'll master them.", TRUE, FALSE,
'10 days before M1 deadline', 'CW004', 'Positive push for
learning advanced SQL'),
('N114', 'P014', "Stored procedures can streamline your
work, and you have the capability to optimize them. Let's
get those triggers working perfectly!", TRUE, FALSE, '14
days before M2 deadline', 'CW004', 'Support for procedure
refinement'),
('N115', 'P015', "Optimization is an art, and you are the
artist. Tune those queries and watch the performance
soar. We're here to help you make it happen.", TRUE,
FALSE, '18 days before M3 deadline', 'CW004',
'Encouragement for performance tuning'),
('N116', 'P016', "Documenting your project is documenting
your journey. Start early and showcase your technical
journey and growth.", TRUE, FALSE, '21 days before final
submission', 'CW004', 'Highlighting the importance of the
report'),
('N117', 'P017', "The schema design deadline is just
around the corner. It's time to buckle down and bring all
the pieces together. You're not alone, and we're all
rooting for you!", TRUE, FALSE, '2 days before M1
deadline', 'CW003', 'Last-minute motivation for M1'),
('N118', 'P018', "SQL queries are the next hurdle. You
have the strength to clear it with flying colors. Begin
now, and the clarity will come.", TRUE, FALSE, '3 days
before M2 deadline', 'CW003', 'Encouragement for starting
queries'),
('N119', 'P019', "Now is the moment to delve into SQL's
advanced functionalities. Tackle this challenge with the
knowledge that you can overcome it.", TRUE, FALSE, '2
days before M1 deadline', 'CW004', 'Urgent motivation for
M1'),
('N120', 'P020', "You're close to mastering stored
procedures. Dedicate yourself to perfecting them and
trust in the process. Your efforts will pay off!", TRUE,
FALSE, '3 days before M2 deadline', 'CW004', 'Support for
meeting M2 deadline'),
('N121', 'P021', "Sanaya, your analytical prowess in Lab
6 has been exceptional. Keep up the precise data
preprocessing as the deadline approaches. Your attention
to detail will set your work apart.", FALSE, TRUE, '1
week before M1 deadline', 'CW001', 'M1 encouragement'),
('N122', 'P022', "Creativity is your strong suit, Sanaya.
With the architecture design milestone coming up, it's
time to solidify your innovative model architecture for
Lab 6.", FALSE, TRUE, '5 days before M2 deadline',
'CW001', 'M2 motivation'),
('N123', 'P023', "The finish line for Lab 6's model
optimization is in sight, Sanaya. Your consistent
dedication will ensure a refined and validated model.
Just a little further!", FALSE, TRUE, '1 day before M3
deadline', 'CW001', 'M3 final push'),
('N124', 'P024', "Proactivity defines you, Sanaya.
Initiating the data labeling for Lab 5 ahead of time is a
smart move that will contribute greatly to your project's
success.", FALSE, TRUE, '1 week before M1 deadline',
'CW002', 'M1 head start'),
('N125', 'P025', "Insightful analysis is a cornerstone of
your work, Sanaya. As you prepare for the performance
analysis milestone in Lab 5, your ability to decipher
complex data will be invaluable.", FALSE, TRUE, '5 days
before M2 deadline', 'CW002', 'M2 strategic
encouragement'),
('N126', 'P026', "Efficiency is in your nature, Sanaya.
Strategically planning the model training for Lab 5 will
amplify your effectiveness. You're on the right track!",
FALSE, TRUE, '1 day before M3 deadline', 'CW002', 'M3
efficiency boost'),
('N127', 'P027', "Sanaya, your final evaluation for Lab 6
is just around the corner. Align your presentation and
report with the coursework objectives to showcase the
depth of your understanding.", FALSE, TRUE, '10 days
before M4 deadline', 'CW001', 'M4 preparation'),
('N128', 'P028', "All your hard work in Lab 5 culminates
with the documentation, Sanaya. Ensure your performance
analysis is as thorough and insightful as your research
has been.", FALSE, TRUE, '10 days before M4 deadline',
'CW002', 'M4 comprehensive review'),
('N129', 'P029', "Mohak, your journey through
visualization concepts is about to take an upward swing.
Let's reinforce those fundamentals together and watch
your confidence soar.", TRUE, FALSE, '14 days before M1
deadline', 'CW005', 'Reinforcement of basics'),
('N130', 'P030', "There's an artist in you, Mohak,
waiting to master the canvas of 'Visualisation Analysis
and Design'. An early start could be the brushstroke that
leads to a masterpiece.", TRUE, FALSE, '10 days before M1
deadline', 'CW005', 'Encouragement for early start'),
('N131', 'P031', "With the M1 deadline on the horizon,
Mohak, let's ensure your data speaks volumes through
clarity and precision. Your insights are too valuable to
be lost in translation.", TRUE, FALSE, '5 days before M1
deadline', 'CW005', 'Importance of clear data
representation'),
('N132', 'P032', "The finishing touches can turn a good
project into an exceptional one, Mohak. Your attention to
detail and user feedback could be what sets your
Assignment 3 apart.", TRUE, FALSE, '1 day before M1
deadline', 'CW005', 'Motivation for excellence'),
('N133', 'P033', "Complex data is just a puzzle waiting
to be solved, Mohak. Let's approach it creatively and
find the simplicity on the other side. Your ideas can
make data digestible for everyone.", TRUE, FALSE, '14
days before M2 deadline', 'CW006', 'Encouragement for
innovative thinking'),
('N134', 'P034', "Structure is the foundation of clarity,
Mohak. As you outline your approach for Assignment 4,
remember that your strategic planning today will
illuminate the path for tomorrow.", TRUE, FALSE, '10 days
before M2 deadline', 'CW006', 'Guidance on planning'),
('N135', 'P035', "Feedback is the mirror that reflects
the brilliance of your work, Mohak. Seek out diverse
perspectives to polish your visualizations to their
brightest shine.", TRUE, FALSE, '5 days before M2
deadline', 'CW006', 'Encouragement to seek feedback'),
('N136', 'P036', "Every data story you tell, Mohak, has
the power to change perspectives. Let's make sure your
final review for Assignment 4 resonates with clarity and
impact.", TRUE, FALSE, '1 day before M2 deadline',
'CW006', 'Final review encouragement'),
('N137', 'P037', "It's time to regroup and refocus,
Mohak. Missed deadlines are just detours on your path to
success. Let's address this together and get back on
track.", TRUE, FALSE, 'After missed deadline', 'CW005',
'Support after missed deadline'),
('N138', 'P038', "Mohak, let's turn missed deadlines into
learning moments. Together, we can reassess your
engagement and ensure that you have all the resources for
a strong comeback.", TRUE, FALSE, 'Pattern of missed
deadlines', 'CW005', 'Offer of additional resources'),
('N139', 'P039', "A missed deadline isn't the end, Mohak—
it's a new beginning. Let's prioritize your upcoming
tasks and carve out a schedule that brings out the best
in you.", TRUE, FALSE, 'Immediate action post deadline',
'CW005', 'Prioritization and scheduling'),
('N140', 'P040', "Keeping the momentum is key, Mohak.
Post-deadline, let's actively engage with the coursework
to outline a recovery plan that plays to your
strengths.", TRUE, FALSE, 'Monitoring post missed
deadline', 'CW006', 'Course recovery plan'),
('N141', 'P041', "Communication opens doors, Mohak. If
you're encountering barriers, let's discuss them early
on. Together, we can overcome any obstacle and keep you
moving forward.", TRUE, FALSE, 'Encouragement to
communicate', 'CW006', 'Open dialogue and support');
UPDATE Nudges
SET
Nudge4DeterioratingStudent = FALSE,
Nudge4ImprovingStudent = TRUE
WHERE
NudgeID IN ('N101', 'N102', 'N103', 'N104', 'N105',
'N106', 'N107', ‘N108');
CREATE TABLE NudgeLog (
NudgeID VARCHAR(10) not null,
StudentID INT not null,
PromptID VARCHAR(10) not null,
NudgeDateTime DATETIME,
PRIMARY KEY (NudgeID),
FOREIGN KEY (StudentID) REFERENCES
Students(StudentID),
FOREIGN KEY (PromptID) REFERENCES Prompts(PromptID)
);
INSERT INTO NudgeLog (NudgeID, StudentID, PromptID,
NudgeDateTime) VALUES
('N101', 21355017, 'P001', '2024-02-28 10:00:00'),
('N102', 21355017, 'P002', '2024-03-17 11:15:00'),
('N103', 21355017, 'P003', '2024-04-06 09:45:00'),
('N104', 21355017, 'P004', '2024-04-20 08:30:00'),
('N105', 21355017, 'P005', '2024-03-05 15:00:00'),
('N106', 21355017, 'P006', '2024-03-22 14:00:00'),
('N107', 21355017, 'P007', '2024-04-11 10:30:00'),
('N108', 21355017, 'P008', '2024-04-25 16:45:00'),
('N109', 21355018, 'P009', '2024-03-01 11:00:00'),
('N110', 21355018, 'P010', '2024-03-11 13:30:00'),
('N111', 21355018, 'P011', '2024-03-21 09:50:00'),
('N112', 21355018, 'P012', '2024-04-01 08:20:00'),
('N113', 21355018, 'P013', '2024-03-08 10:10:00'),
('N114', 21355018, 'P014', '2024-03-18 14:25:00'),
('N115', 21355018, 'P015', '2024-03-28 09:40:00'),
('N116', 21355018, 'P016', '2024-04-08 16:15:00'),
('N117', 21355018, 'P017', '2024-03-10 15:05:00'),
('N118', 21355018, 'P018', '2024-03-23 13:45:00'),
('N119', 21355018, 'P019', '2024-03-16 11:25:00'),
('N120', 21355018, 'P020', '2024-03-29 12:35:00'),
('N121', 21355019, 'P021', '2024-03-03 10:20:00'),
('N122', 21355019, 'P022', '2024-03-19 11:10:00'),
('N123', 21355019, 'P023', '2024-04-06 09:55:00'),
('N124', 21355019, 'P024', '2024-03-05 14:50:00'),
('N125', 21355019, 'P025', '2024-03-24 15:30:00'),
('N126', 21355019, 'P026', '2024-04-11 10:40:00'),
('N127', 21355019, 'P027', '2024-04-11 08:45:00'),
('N128', 21355019, 'P028', '2024-04-16 16:00:00'),
('N129', 21355020, 'P029', '2024-03-01 09:30:00'),
('N130', 21355020, 'P030', '2024-03-16 14:10:00'),
('N131', 21355020, 'P031', '2024-04-04 11:20:00'),
('N132', 21355020, 'P032', '2024-04-22 08:50:00'),
('N133', 21355020, 'P033', '2024-03-14 11:15:00'),
('N134', 21355020, 'P034', '2024-03-20 15:40:00'),
('N135', 21355020, 'P035', '2024-03-24 14:05:00'),
('N136', 21355020, 'P036', '2024-04-04 09:20:00'),
('N137', 21355020, 'P037', '2024-04-24 10:00:00'),
('N138', 21355020, 'P038', '2024-04-27 14:00:00'),
('N139', 21355020, 'P039', '2024-04-25 09:00:00'),
('N140', 21355020, 'P040', '2024-04-30 11:00:00'),
('N141', 21355020, 'P041', '2024-05-03 15:00:00');
CREATE TABLE feedback (
id INT AUTO_INCREMENT ,-- PRIMARY KEY,
student_id INT,
feedback Varchar(50),
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
primary key (id),
foreign key (student_id) references
students(StudentID)
);
ALTER TABLE feedback ADD COLUMN message_id VARCHAR(255);'''


