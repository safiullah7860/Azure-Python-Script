import sys
from openai import AzureOpenAI
import pandas as pd
import csv
import datetime
import os
import PyPDF2

def pdf_to_text(pdf_path):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        abstractText = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            abstractText += page.extract_text()

    # Return the extracted text as a string
    return abstractText

# Folder containing the PDF files
folder_path = "full articles"

# Create a DataFrame to store the results
df = pd.DataFrame(columns=["Title", "Article Text"])

# Iterate through the first PDF file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        article_text = pdf_to_text(pdf_path)
        df = pd.concat([df, pd.DataFrame({"Title": [filename], "Article Text": [article_text]})], ignore_index=True)
        break

# Save the DataFrame to a CSV file
input_file = "articles_summary.csv"
df.to_csv(input_file, index=False)

print(f"Output saved in {input_file}")

azure_api_key = open("key.txt", "r").read().strip("\n")
azure_api_endpoint = open("endpoint.txt", "r").read().strip("\n")
# Get the current date and time in a format that is compatible with the CSV file name
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
criteria_text = open("criteria.txt", "r").read().strip("\n")
modelName = "gpt4o"
csv_file_name = f"output_{date_time} Model={modelName} allYes.csv"
client = AzureOpenAI(
    api_version="2024-02-01",
    api_key=azure_api_key,
    azure_endpoint=azure_api_endpoint,
)

# Open the CSV file in write mode
with open(csv_file_name, "w", newline="") as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Row Number", "Title", "Question 1", "Question 2", "Question 3", "Question 4",
                     "Question 5", "Full Response"])

    # Read the CSV file into a DataFrame (2-d, tabular data)
    df = pd.read_csv("articles_summary.csv")

    # Process the DataFrame contents
    for row in df.iterrows():
        row_number = row[0] + 1  # Adjust row numbering to start from 1
        title = row[1]["Title"]
        fullArticleText = row[1]["Article Text"]

        # Combine criteria, title of the article, and article into a single query
        ChatGPTQuery = criteria_text + "\nArticle: " + fullArticleText

        chatGPTresponse = client.chat.completions.create(
            model=modelName,
            messages=[
                {
                    "role": "user",
                    "content": ChatGPTQuery,
                },
            ],
        )
        response = chatGPTresponse.choices[0].message.content

        # Split The response into lines and extract criteria values
        question_responses = [""] * 5

        for line in response.split("\n"):
            for i in range(1, 6):
                if f"Answer {i}:" in line:
                    question_responses[i-1] = line.split(":")[1].strip()

        # Check if any criteria values are still empty (for the last line)
        question_responses = [val if val else "Not specified" for val in question_responses]

        # Write the row to the CSV file
        writer.writerow([row_number, title] + question_responses + [response])

os.startfile(csv_file_name)

print("Output saved in", csv_file_name)