# Retrieval-Augmented Generation(RAG) System Using Azure OpenAI

This project demonstrates implementation of Retrieval-Augmented Generation (RAG) using **Azure OpenAI**, **Azure AI Search**, and **Azure Storage Account**. The system enhances AI-generated responses by retrieving relevant data from a hotel dataset stored in Azure and combining it with the output from GPT-3.5-turbo.

## Description

The goal of this project is to provide more accurate and relevant responses to user queries by:

1. Retrieving relevant hotel data from a dataset stored in Azure.
2. Using the **text-embedding-ada-002** model to create embeddings for semantic search.
3. Enhancing the final answer using **GPT-3.5-turbo** via Azure OpenAI.

The dataset used includes hotel information across several countries.

## How I Built This

1. **Azure Setup**:
   - Created an **Azure Resource Group**.
   - Set up the following services:
     - **Azure OpenAI** (for GPT-3.5-turbo and text-embedding-ada-002).
     - **Azure AI Search**.
     - **Azure Storage Account** (uploaded the hotel dataset here).

2. **Model Deployment**:
   - Deployed `gpt-35-turbo` and `text-embedding-ada-002` using **Azure AI Foundry**.

3. **Application Setup**:
   - Created a simple `app.py` in **VS Code**.
   - Created a `.env` file to store API keys and endpoints.
   - Wrote logic in `app.py` to:
     - Generate embeddings,
     - Query the AI Search index,
     - Generate a final response using GPT.

4. **Execution**:
   - Run the app locally via terminal:
     ```bash
     python app.py
     ```

## Files

- `app.py` – The main script that:
  - Reads user input,
  - Retrieves relevant data using embeddings and Azure AI Search,
  - Sends combined prompt to GPT-3.5-turbo for response.
  
- `.env` – Contains all secret keys and endpoints:
