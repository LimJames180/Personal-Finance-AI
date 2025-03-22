import cohere
import json

import os
from dotenv import load_dotenv


from datetime import datetime

# Get today's date
today = datetime.today()

# Format the date as YYYY-MM-DD
formatted_date = today.strftime("Todays Date is %Y-%m-%d")

load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('COHERE_API_KEY')

schema = {"type": "json_object", "schema":{
  "title": "BasicTransaction",
  "type": "object",
  "properties": {
    "amount": {
      "type": "number",
      "description": "The amount of money involved in the transaction."
    },
    "category": {
      "type": "string",
      "enum": [
        "Food",
        "Housing",
        "Transportation",
        "Health",
        "Entertainment",
        "Shopping",
        "Bills",
        "Travel",
        "Education",
        "Finance",
        "Donations",
        "Miscellaneous",
        "Income"
      ],
      "description": "The category of the transaction."
    },
    "date": {
      "type": "string",
      "description": "The date of the transaction in YYYY-MM-DD format."
    },
    "description": {
      "type": "string",
      "description": "A short description of the transaction."
    },
    "type": {
      "type": "string",
      "enum": ["expense", "income"],
      "description": "Type of the transaction."
    }
  },
  "required": ["amount", "category", "date", "type"],
  "additionalProperties": False
}

}

co = cohere.ClientV2(api_key=api_key)

def aitransaction(text):

  res = co.chat(
      model="command-a-03-2025",
      messages=[
          {
              "role": "user",
              "content": formatted_date + text,

          }
      ],
      response_format=schema
  ,
  )
  return json.loads(res.message.content[0].text)
