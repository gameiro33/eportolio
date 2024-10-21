from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client. Environment variables avoid hardcoding the API key, hence enhancing security
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Analyze the given file content using OpenAI's GPT model and return a forensic analysis summary. 
# Designed as a function to be called by other classes
def analyze_file(file_content):
    try:
        # Create a chat completion request. 
        # Using the gpt-4o-mini model as it is recent and more affordable than the gpt-4o model. This can be changed easily
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                # When role is system, the AI will follow the instructions provided in the message. 
                # In this case, the AI is a forensic expert
                {"role": "system", "content": "You are a forensic expert. Analyse the given file content and summarize it in 100 words" 
                 + "- you should start with a criminal likelihood score from 1 to 10, formatting it: Criminal Likelihood score: 1/10. "
                 + "If the file is empty, return: The file you specified is empty, please check it."},
                # The file content is provided as a variable called file_content
                # Hence, this agent can be called easily by other classes
                {"role": "user", "content": f"Analyse the following file content: {file_content}"}
            ]
        )

        # Check if the API returned a valid response, if not, return an error message
        if completion.choices and completion.choices[0].message.content:
            return completion.choices[0].message.content
        else:
            return "Error: The API returned an empty response. Please try again later."

    except Exception as e:
        return f"Error: An exception occurred while analyzing the file: {str(e)}"
