import re
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
    writer.writerow(["Row Number", "Title", "Question 1", "Question 2", "Question 3", "Question 4", "Question 5", "Question 6", "Question 7", "Question 8", "Question 9", "Question 1A", "Question 1B", "Question 2A", "Question 2B", "Question 3A", "Question 4A", "Question 4B", "Question 5A", "Question 5B", "Question 6A", "Question 6B", "Question 7A", "Question 7B", "Question 8A", "Full Response"])

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

                answer_keys = [
                    "Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5", "Answer 6", "Answer 7", "Answer 8", "Answer 9",
                    "Answer 1A", "Answer 1B", "Answer 2A", "Answer 2B", "Answer 3A",
                    "Answer 4A", "Answer 4B", "Answer 5A", "Answer 5B", "Answer 6A", "Answer 6B", "Answer 7A", "Answer 7B", "Answer 8A"
                ]
                question_responses = ["Not specified"] * len(answer_keys)
                # Improved extraction logic: robust regex for all answer formats (fix for 1A, 2B, 8A, etc)
                answer_pattern = re.compile(r"^\s*\**\s*(Answer [1-9][AB]?)\s*:?\**\s*(.*)$", re.IGNORECASE)
                for line in response.split("\n"):
                    match = answer_pattern.match(line.strip())
                    if match:
                        key = match.group(1).strip()
                        answer = match.group(2).strip()
                        if key in answer_keys:
                            idx = answer_keys.index(key)
                            question_responses[idx] = answer
                writer.writerow([row_number, title] + question_responses + [response])
                row_number += 1

os.startfile(csv_file_name)
print("Output saved in", csv_file_name)