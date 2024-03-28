import openai
import re
from src.Prompts import classification_prompt
from src.Prompts import generation_prompt
from src.Prompts import genre_summary_prompt
import time
import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
import random

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

from pinecone import Pinecone

# initialize connection to pinecone
api_key = os.getenv("pinecone_api_key")

# configure client
pc = Pinecone(api_key=api_key)


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

from langchain.vectorstores import Pinecone

text_field = "text"

# switch back to normal index for langchain
index_name = "bookstore-chatbot"
index = pc.Index(index_name)

vectorstore = Pinecone(index, embeddings.embed_query, text_field)

messages = {
    "BUY": "Sure, you can buy a book by adding it to the cart and checking out",
    "RETURN": "You can return any book to us within thirty days of purchasing it.",
    "AVAILABILITY": "We have most of the books in our inventory. Please contact us for more information at 77314382",
    "ADDRESS": "We are located in 111 W Ave, Surrey, BC",
    "STOP": "Thank you for using our online services!",
    "TIMINGS": "We are open from 9am-5pm everyday",
    "DELIVERY": "We can deliver certain books. Please contact us for more information",
    "NUMBER": "You can reach us at 77314382.",
    "OTHER": "Sorry, I am unsure how to answer that. You can get in touch with us at 77314382",
}


class Model:
    """A simple example class"""

    def __init__(self):
        self.data = []

    def f(self, req):

        return final_function(req.text, req.lead_id)


def call_vectordb(text):

    query = text
    result = vectorstore.similarity_search(
        query, k=1  # our search query  # return 1 most relevant docs
    )
    return result


def call_recommendation(text):

    query = text
    result = vectorstore.similarity_search(
        query, k=3  # our search query  # return 3 most relevant docs
    )
    return result


def extract_labels(text):
    """Receives a text and extract a list of labels from it using Open AI"""
    in_progress = True
    counter = 0
    labels = []
    while in_progress:
        try:
            prompt = classification_prompt.format(text=text)

            answer = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a classification model that classifies the text into labels: \
                              RECOMMENDATION, GENRE, SUMMARY, BUY, NUMBER, RETURN, AVAILABILITY, ADDRESS, STOP, TIMINGS, DELIVERY, OTHER. \nKeeping in mind the prompt's label mapper and the examples",
                    },
                    {"role": "user", "content": f"{prompt}"},
                ],
                temperature=0.15,
            )

            labels = answer.choices[0].message.content

            labels = labels.split(", ")

            if len(labels) > 0:
                in_progress = False

        except Exception as prompt_exteption:
            print(
                "3.0 Exception while classification using OpenAi API", prompt_exteption
            )
            time.sleep(1.5)
        finally:
            if counter >= 10:
                in_progress = False
            counter = counter + 1
    return labels


def generate_response(
    inquiry_message,
    context,
    followup_question,
):
    prompt = generation_prompt.format(
        context=context,
        inquiry_message=inquiry_message,
        followup_question=followup_question,
    )

    in_progress = True
    counter = 0
    response = ""
    while in_progress:
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cool human book sales representative who provides a "
                        "engaging good and concise answer for the book using only the information given to you.",
                    },
                    {"role": "user", "content": f"{prompt}"},
                ],
                temperature=0.20,
            )

            response = response.choices[0].message.content
            response = response.replace('"', "")
            if response.strip() != "":
                in_progress = False

        except Exception as response_exception:
            print(
                "4.7 Exception while generating response using openai",
                response_exception,
            )
            time.sleep(1.5)
        finally:
            if counter >= 10:
                in_progress = False
            counter = counter + 1

    return response


def is_genre_summary(inquiry_message):
    prompt = genre_summary_prompt.format(inquiry_message=inquiry_message)

    in_progress = True
    counter = 0
    response = ""
    while in_progress:
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a model that paraphrases the inquiry message only to include include messages related to Summary or Genre or Recommendation of a book",
                    },
                    {"role": "user", "content": f"{prompt}"},
                ],
                temperature=0.20,
            )

            response = response.choices[0].message.content
            response = response.replace('"', "")
            response = response.replace("'", "")
            if response.strip() != "":
                in_progress = False

        except Exception as response_exception:
            print(
                "4.7 Exception while generating response using openai",
                response_exception,
            )
            time.sleep(1.5)
        finally:
            if counter >= 10:
                in_progress = False
            counter = counter + 1

    return response


def final_function(text, id=None):
    context_messages = []

    Label_list = extract_labels(text)
    print(Label_list)

    if (
        "RECOMMENDATION" in Label_list
        or "GENRE" in Label_list
        or "SUMMARY" in Label_list
    ):
        # Append the message from the result of vector_db function
        print(text)
        modified_text = is_genre_summary(text)
        print(modified_text)
        if (
            modified_text == "FALSE"
            or modified_text == "False"
            or modified_text is False
        ) and len(
            Label_list
        ) >= 1:  # If result is "FALSE" and 'BOOK_ENQUIRY' is the only label
            Label_list.append("OTHER")
            labels_to_remove = ["RECOMMENDATION", "GENRE", "SUMMARY"]

            for label in labels_to_remove:
                if label in Label_list:
                    Label_list.remove(label)
        else:
            if "RECOMMENDATION" in Label_list:
                recommendation_result = call_recommendation(modified_text)
                print(recommendation_result)
                context_messages.append(recommendation_result)
            else:
                book_enquiry_result = call_vectordb(modified_text)
                print(book_enquiry_result)
                context_messages.append(book_enquiry_result)
    print(Label_list)
    # If 'OTHER' is not present or is the only label, add the corresponding message
    if "OTHER" in Label_list and len(Label_list) > 1:
        for label in Label_list:
            if label != "OTHER":
                context_messages.append(messages[label])

    else:
        for label in Label_list:
            if label not in ["RECOMMENDATION", "GENRE", "SUMMARY"]:
                context_messages.append(messages[label])

    # Print or use context_messages as needed
    print(context_messages)

    inquiry_message = text
    context = context_messages
    followup_questions = [
        "Do you have more questions?",
        "Is there anything else you'd like to know?",
        "Would you like more information?",
        "Do you need assistance with anything else?",
    ]

    # Randomly select a follow-up question
    random_followup_question = random.choice(followup_questions)
    chat_response = generate_response(
        inquiry_message,
        context,
        random_followup_question,
    )
    chat_response = chat_response.replace("\n\n", "")
    chat_response = chat_response.replace("\n", "")

    chat_response = chat_response.replace(": [", ": ")
    chat_response = chat_response.replace("[", "")
    chat_response = chat_response.replace("]. ", ". ")
    chat_response = chat_response.replace("].", ". ")
    chat_response = chat_response.replace("]", ". ")
    return chat_response
