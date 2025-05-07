import os
import json
import time
from dotenv import load_dotenv
from openai import AzureOpenAI
from openai.types.chat import ChatCompletion

def call_openai_with_retry(client, deployment, messages, extra_body, retries=5):
    for i in range(retries):
        try:
            response: ChatCompletion = client.chat.completions.create(
                model=deployment,
                temperature=0.5,
                max_tokens=1000,
                messages=messages,
                extra_body=extra_body
            )
            return response
        except Exception as ex:
            # Detect rate limit
            if '429' in str(ex):
                wait = (2 ** i) + 1
                print(f"[Retry {i+1}/{retries}] Rate limit hit. Waiting {wait} seconds...")
                time.sleep(wait)
            else:
                print(f"Non-retriable error: {ex}")
                raise
    raise Exception("Max retries exceeded")

def main():
    try:
        show_citations = False

        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        azure_search_key = os.getenv("AZURE_SEARCH_KEY")
        azure_search_index = os.getenv("AZURE_SEARCH_INDEX")

        
        client = AzureOpenAI(
            base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_deployment}/extensions",
            api_key=azure_oai_key,
            api_version="2023-09-01-preview"
        )

        text = input('\nEnter a question:\n')

        extension_config = {
            "dataSources": [{
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": azure_search_endpoint,
                    "key": azure_search_key,
                    "indexName": azure_search_index
                }
            }]
        }

        messages = [
            {"role": "system", "content": "You are a helpful travel agent"},
            {"role": "user", "content": text}
        ]

        print("...Sending the following request to Azure OpenAI endpoint...")
        print("Request: " + text + "\n")

        response = call_openai_with_retry(client, azure_oai_deployment, messages, extension_config)

        print("Response: " + response.choices[0].message.content + "\n")

        if show_citations:
            print("Citations:")
            citations = response.choices[0].message.context["messages"][0]["content"]
            citation_json = json.loads(citations)
            for c in citation_json["citations"]:
                print("  Title: " + c['title'] + "\n    URL: " + c['url'])

    except Exception as ex:
        print(f"[Fatal Error] {ex}")

if __name__ == '__main__':
    main()