from openai import AzureOpenAI
import pandas as pd
import csv
import datetime
import os
azure_api_key = open("key.txt", "r").read().strip("\n")
azure_api_endpoint = open("endpoint.txt", "r").read().strip("\n")
# Get the current date and time in a format that is compatible with the CSV file name
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
criteria_text = open("criteria.txt", "r").read().strip("\n")
csv_file_name = f"output_{date_time}.csv"
client = AzureOpenAI(
    api_version="2024-02-01",
    api_key = azure_api_key,
    azure_endpoint=azure_api_endpoint,
)

# Open the CSV file in write mode
with open(csv_file_name, "w", newline="") as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Row Number", "Title", "Criteria 1", "Criteria 2", "Criteria 3", "Criteria 4",
                     "Criteria 1 Met", "Criteria 2 Met", "Criteria 3 Met", "Criteria 4 Met", "Full Response", "Y/N"])

    # Read the CSV file into a DataFrame (2-d, tabular data)
    df = pd.read_csv("input.csv")

    # Process the DataFrame contents
    for row in df.iterrows():
        row_number = row[0] + 1  # Adjust row numbering to start from 1
        title = row[1]["Title"]
        abstract = row[1]["Abstract"]

        # Combine criteria, title of the article, and abstract into a single query
        ChatGPTQuery = criteria_text + "\ntitle: " + title + "\nabstract:" + abstract

        # Get the full ChatGPT response
        # change the variable "repsonse" to the following to change temperature
        '''response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": ChatGPTQuery}], temperature = 0.1,
        ).choices[0].message.content'''
        # make sure to change the temperature to whatever you desire

        chatGPTresponse = client.chat.completions.create(
            model="gpt4",  # e.g. gpt-35-instant
            messages=[
                {
                    "role": "user",
                    "content": criteria_text,
                },
            ],
        )
        response = chatGPTresponse.choices[0].message.content

        # Extract the first word of the response for Y/N column
        yn_value = 1 if response.split()[0].lower() == "yes" else 0

        # Split The response into lines and extract criteria values
        criteria_values = [""] * 4
        criteria_met_values = [0] * 4

        for line in response.split("\n"):
            if "Criteria 1:" in line:
                criteria_values[0] = line.split(":")[1].strip()
                criteria_met_values[0] = 1 if "YES" in criteria_values[0] else 0
            elif "Criteria 2:" in line:
                criteria_values[1] = line.split(":")[1].strip()
                criteria_met_values[1] = 1 if "YES" in criteria_values[1] else 0
            elif "Criteria 3:" in line:
                criteria_values[2] = line.split(":")[1].strip()
                criteria_met_values[2] = 1 if "YES" in criteria_values[2] else 0
            elif "Criteria 4:" in line:
                criteria_values[3] = line.split(":")[1].strip()
                criteria_met_values[3] = 1 if "YES" in criteria_values[3] else 0

        # Check if any criteria values are still empty (for the last line)
        criteria_values = [val if val else "Not specified" for val in criteria_values]

        # Check if all criteria are met and update the Y/N column
        yn_value = 1 if all(criteria_met_values) else 0

        # Write the row to the CSV file
        writer.writerow([row_number, title] + criteria_values + criteria_met_values + [response, yn_value])


os.startfile(csv_file_name)

# print('\n'+ response)
print("Output saved in", csv_file_name)