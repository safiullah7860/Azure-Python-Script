from openai import AzureOpenAI
azure_api_key = open("key.txt", "r").read().strip("\n")
azure_api_endpoint = open("endpoint.txt", "r").read().strip("\n")
client = AzureOpenAI(
    # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
    api_version="2023-07-01-preview",
    api_key = azure_api_key,
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    azure_endpoint=azure_api_endpoint,
)

completion = client.chat.completions.create(
    model="FirstModel",  # e.g. gpt-35-instant
    messages=[
        {
            "role": "user",
            "content": "Hello, what version are you on",
        },
    ],
)

print(completion.model_dump_json(indent=2))