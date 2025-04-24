import sys
from openai import AzureOpenAI
import pandas as pd
import csv
import datetime
import os
import PyPDF2

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file, strict=False)
        abstractText = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            abstractText += page.extract_text()
    return abstractText

folder_path = "full articles"
azure_api_key = open("key.txt", "r").read().strip("\n")
azure_api_endpoint = open("endpoint.txt", "r").read().strip("\n")
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
criteria_text = open("criteria.txt", "r").read().strip("\n")
modelName = "gpt4o"
csv_file_name = f"output_{date_time} Model={modelName} allYes.csv"
client = AzureOpenAI(
    api_version="2024-02-01",
    api_key=azure_api_key,
    azure_endpoint=azure_api_endpoint,
)

with open(csv_file_name, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Row Number", "Title", "Question 1", "Question 2", "Question 3", "Question 4", "Question 5", "Question 6", "Question 7", "Question 8", "Question 9", "Full Response"])

    row_number = 1
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            article_text = pdf_to_text(pdf_path)
            df = pd.DataFrame({"Title": [filename], "Article Text": [article_text]})

            for _, row in df.iterrows():
                title = row["Title"]
                fullArticleText = row["Article Text"]
                ChatGPTQuery = criteria_text + "\nArticle: " + fullArticleText

                chatGPTresponse = client.chat.completions.create(
                    model=modelName,
                    messages=[{"role": "user", "content": ChatGPTQuery}],
                )
                response = chatGPTresponse.choices[0].message.content

                question_responses = [""] * 9
                for line in response.split("\n"):
                    for i in range(1, 10):
                        if f"Answer {i}:" in line:
                            question_responses[i-1] = line.split(":")[1].strip()
                question_responses = [val if val else "Not specified" for val in question_responses]

                writer.writerow([row_number, title] + question_responses + [response])
                row_number += 1

os.startfile(csv_file_name)
print("Output saved in", csv_file_name)