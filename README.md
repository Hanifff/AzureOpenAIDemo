# Azure OpenAI Chat Demo

This project demonstrates how to create an interactive chat session using Azure OpenAI and Azure Cognitive Search. The chat session allows users to input queries and receive responses from the AI, with the ability to handle rate limit errors gracefully.

## Features

- Interactive chat session with Azure OpenAI
- Integration with Azure Cognitive Search for enhanced responses
- Retry mechanism with exponential backoff for rate limit errors
- Graceful exit on `Ctrl+C`

## Prerequisites

- Python 3.6 or higher
- Azure OpenAI API key
- Azure Cognitive Search endpoint and key

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-repo/azure-openai-chat-demo.git
    cd azure-openai-chat-demo
    ```

2. **Create a virtual environment and activate it:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the project root and add your Azure credentials:**
    ```env
    ENDPOINT_URL=https://your-openai-endpoint.openai.azure.com/
    DEPLOYMENT_NAME=your-deployment-name
    SEARCH_ENDPOINT=https://your-search-endpoint.search.windows.net
    SEARCH_KEY=your-search-key
    AZURE_OPENAI_API_KEY=your-openai-api-key
    ```

## Usage

1. **Run the chat application:**
    ```sh
    python main.py
    ```

2. **Interact with the chat session:**
    - Type your queries and press `Enter` to receive responses from the AI.
    - Type `exit` or `quit` to end the session.
    - Press `Ctrl+C` to exit the session gracefully.

## Code Overview

### `AzureOpenAIChat` Class

- **`__init__` Method:**
    Initializes the class, loads environment variables, and creates the OpenAI client.

- **`create_client` Method:**
    Creates and returns the OpenAI client using the API key.

- **`get_completion` Method:**
    Sends a user message to the OpenAI API and returns the completion. Implements a retry mechanism with exponential backoff for rate limit errors.

- **`start_chat` Method:**
    Starts an open chat session, taking user input in a loop and printing the AI's response. Exits gracefully on `Ctrl+C`.

### `main` Function

- Creates an instance of the `AzureOpenAIChat` class and starts the chat session.

## Example

```sh
$ python main.py
Azure OpenAI Chat Demo Starting...
Starting chat session. Type 'exit' or 'quit' to end the session.
You: What are the differences between Azure Machine Learning and Azure AI services?
AI: Azure Machine Learning is a cloud-based service for building, training, and deploying machine learning models. Azure AI services provide pre-built AI capabilities such as vision, speech, language, and decision-making.

You: exit
Exiting...