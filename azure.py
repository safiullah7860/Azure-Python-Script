from openai import AzureOpenAI
import pandas as pd
import csv
import datetime
import os
azure_api_key = open("key.txt", "r").read().strip("\n")  #api key
azure_api_endpoint = open("endpoint.txt", "r").read().strip("\n") #endpoint url
criteria_text = open("criteria.txt", "r").read().strip("\n") #criteria to feed chatgpt
# Get the current date and time in a format that is compatible with the CSV file name:
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
csv_file_name = f"output_{date_time}.csv"
client = AzureOpenAI(
    api_version="2023-07-01-preview",
    api_key = azure_api_key,
    azure_endpoint=azure_api_endpoint,
)

completion = client.chat.completions.create(
    model="FirstModel", 
    messages=[
        {
            "role": "user",
            "content": "Hello, what version are you on",
        },
    ],
)

response = completion.choices[0].message.content

print('\n'+ response) #gives output in non-JSON format
os.startfile(csv_file_name)

print("Output saved in", csv_file_name)