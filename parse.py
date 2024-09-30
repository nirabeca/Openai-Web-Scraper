from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv("keys.env")

# Set OpenAI API key
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_openai(dom_chunks, parse_description):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = template.format(dom_content=chunk, parse_description=parse_description)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use gpt-4 if available
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000  # Adjust based on needs
        )

        # Access the response object correctly based on the new API
        result = response.choices[0].message.content
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(result)

    return "\n".join(parsed_results)

# Example usage:
# dom_chunks = ["..."]  # Replace with actual DOM content chunks
# parse_description = "Extract the following information: ..."
# parsed_data = parse_with_openai(dom_chunks, parse_description)
# print(parsed_data)
