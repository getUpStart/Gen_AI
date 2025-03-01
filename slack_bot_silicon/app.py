import streamlit as st
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import openai
from openai.error import OpenAIError

# Set up the OpenAI API key (replace with your actual key)
openai.api_key = "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"

# Initialize Slack client with your bot token (replace with your actual Slack token)
slack_token = 'xoxb-8511974076759-8527548612163-Pt74f3Trjv5nGgAJZemDhySN'
client = WebClient(token=slack_token)

# Streamlit App Layout
def app():
    st.title("Slack Thread Question Answering App")

    # User Input for Slack Channel
    channel_id = st.text_input("Enter the Slack Channel ID:")

    # Fetch Slack Thread Data on Button Click
    if st.button("Fetch Slack Thread Data"):
        messages = fetch_all_messages(channel_id)
        if messages:
            st.session_state.messages = messages  # Save fetched messages to session state
            st.write("Fetched Slack Messages:")
            st.write(messages)

    # Ask a Question
    question = st.text_input("Ask a question about the messages:")
    if question:
        if 'messages' in st.session_state:  # Check if messages are stored in session state
            answer = answer_question_from_messages(st.session_state.messages, question)
            st.write(f"Answer: {answer}")
        else:
            st.write("Please fetch the Slack messages first.")

# Fetch All Slack Messages (with pagination, including replies)
def fetch_all_messages(channel_id):
    try:
        all_messages = []
        response = client.conversations_history(channel=channel_id)
        all_messages.extend(response['messages'])

        # Pagination: Fetch more messages if necessary
        while 'response_metadata' in response and 'next_cursor' in response['response_metadata']:
            next_cursor = response['response_metadata']['next_cursor']
            response = client.conversations_history(channel=channel_id, cursor=next_cursor)
            all_messages.extend(response['messages'])

        # For each message, check if it has replies, and fetch them if present
        threaded_messages = []
        for message in all_messages:
            if 'thread_ts' in message:  # Check if the message is part of a thread
                thread_response = client.conversations_replies(
                    channel=channel_id,
                    ts=message['thread_ts']  # This is the timestamp of the parent message
                )
                threaded_messages.extend(thread_response['messages'])  # Add replies to the list
            else:
                threaded_messages.append(message)  # If no replies, just add the parent message
        
        return threaded_messages

    except SlackApiError as e:
        st.error(f"Error fetching messages: {e.response['error']}")
        return None

# Process Slack Messages to Answer a Question
def create_qa_prompt(messages):
    # Format the context from Slack messages
    context = ""
    chunk_size = 2000  # Max tokens the model can handle, adjust as necessary
    current_chunk = ""

    for msg in messages:
        current_chunk += msg.get('text', '') + "\n"
        if len(current_chunk) > chunk_size:
            context += current_chunk
            current_chunk = ""
    
    if current_chunk:
        context += current_chunk

    # Construct the prompt to pass to the model
    prompt = f"""
    Below are the Slack messages related to issue troubleshooting:
    {context}

    Answer the following question based on the messages:
    """
    return prompt

def answer_question_from_messages(messages, question):
    try:
        prompt = create_qa_prompt(messages)
        prompt += f"\n\nQuestion: {question}\nAnswer:"

        # Use openai.ChatCompletion.create to query the model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']

    except OpenAIError as e:
        # Handle OpenAI-specific errors
        st.error(f"An error occurred while querying OpenAI: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        st.error(f"An unexpected error occurred: {e}")
        return None

# Run the Streamlit app
if __name__ == "__main__":
    app()
