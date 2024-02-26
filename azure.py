from openai import AzureOpenAI
import pandas as pd
import csv
import datetime
import os
azure_api_key = open("key.txt", "r").read().strip("\n")
azure_api_endpoint = open("endpoint.txt", "r").read().strip("\n")
client = AzureOpenAI(
    api_version="2023-07-01-preview",
    api_key = azure_api_key,
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

# Access the response content directly
response = completion.choices[0].message.content

print('\n'+ response)