import os
import openai
import time
from dotenv import load_dotenv

class AzureOpenAIChat:
    def __init__(self):
        """
        Initialize the AzureOpenAIChat class.
        Load environment variables and create the OpenAI client.
        """
        load_dotenv()
        
        # Initialize configuration from environment variables
        self.endpoint = os.getenv("ENDPOINT_URL")
        self.deployment = os.getenv("DEPLOYMENT_NAME")
        self.search_endpoint = os.getenv("SEARCH_ENDPOINT")
        self.search_key = os.getenv("SEARCH_KEY")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        # Create the OpenAI client
        self.client = self.create_client()

    def create_client(self):
        """
        Create and return the OpenAI client using the API key.
        """
        return openai.AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version="2024-05-01-preview",
        )

    def get_completion(self, user_message):
        """
        Send a user message to the OpenAI API and return the completion.
        Implement retry mechanism with exponential backoff for rate limit errors.
        """
        max_retries = 5
        retry_delay = 1  # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                return self.client.chat.completions.create(
                    model=self.deployment,
                    messages=[{
                        "role": "user",
                        "content": user_message
                    }],
                    max_tokens=4096,
                    temperature=0,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    stream=False,
                    extra_body={
                        "data_sources": [{
                            "type": "azure_search",
                            "parameters": {
                                "endpoint": f"{self.search_endpoint}",
                                "index_name": "cv",
                                "semantic_configuration": "default",
                                "query_type": "semantic",
                                "fields_mapping": {},
                                "in_scope": True,
                                "role_information": "You are an AI assistant that helps people find information.",
                                "filter": None,
                                "strictness": 3,
                                "top_n_documents": 5,
                                "authentication": {
                                    "type": "api_key",
                                    "key": f"{self.search_key}"
                                }
                            }
                        }]
                    }
                )
            except openai.RateLimitError as e:
                print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            except openai.OpenAIError as e:
                print(f"An error occurred: {e}")
                break

    def start_chat(self):
        """
        Start an open chat session.
        """
        print("Starting chat session. Type 'exit' or 'quit' to end the session.")
        try:
            while True:
                # Take user input
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                # Get completion from OpenAI API
                completion = self.get_completion(user_input)
                
                # Print AI response
                if completion:
                    print("AI: ", completion.choices[0].message.content)
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nExiting...")

def main():
    """
    Create an instance of AzureOpenAIChat and start the chat session.
    """
    print("Azure OpenAI Chat Demo Staring...")
    chat = AzureOpenAIChat()
    chat.start_chat()

if __name__ == "__main__":
    main()