import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os


genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
llm = None

def classify_books(book_name_list):
    prompt_template = PromptTemplate.from_template('''You are a classifier that classifies books as fiction or non-fiction: {books} .Output should be an array with each row as  [book name , classification]''')


    prompt = prompt_template.format(books=", ".join(book_name_list))

    response = llm.invoke(prompt)
    response_array = [row.split(', ') for row in response.content.strip('[]').split('], [')]
    return response_array



if __name__ ==  "services.classifier":

    llm = ChatGoogleGenerativeAI(model="gemini-pro")





