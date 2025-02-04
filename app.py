import streamlit as st
import requests

st.markdown(
    """
    <style>
        .title-container {
            text-align: center;
            font-size: 60px;
            font-weight: bold;
        }
        .my-florida {
            color: black;
        }
        .green {
            color: green;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit App Title with formatted text
st.markdown(
    """
    <div class="title-container">
        <span class="my-florida">My Florida</span> <span class="green">Green</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for user input
st.sidebar.header("User Information")
handle = st.sidebar.text_input("Enter Handle (Email):")

# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
if handle:
    user_input = st.chat_input("Type your message...")
    if user_input:
        # Append user message to chat history
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        # Update with correct API endpoint
        api_url = "https://floridagreen-542808340038.us-central1.run.app/api/chatbot-query"
        
        # Request payload
        payload = {
            "query": str(user_input),
            "handle": str(handle)
        }
        
        # Send request to API
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            bot_response = response.json()
            bot_message = bot_response.get("data", {}).get("ai_respone", "No response received.")
            
            # Append bot response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": bot_message})
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    # Display updated chat messages
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def set_background_image(image_path):
    """
    Set a background image for the Streamlit app.
    :param image_path: str, path to the background image
    """
    # Read the image file
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    
    # Encode the image in base64
    import base64
    encoded_image = base64.b64encode(image_bytes).decode()
    
    # Define the CSS to set the background image
    background_image_style = f"""
    <style>
    .stApp {{
        background: url(data:image/jpg;base64,{encoded_image});
        background-size: cover;
    }}
    </style>
    """
    
    # Add the CSS to the Streamlit app
    st.markdown(background_image_style, unsafe_allow_html=True)

# Path to the background image
image_path = "1.jpg"

# Call the function to set the background image
set_background_image(image_path)
