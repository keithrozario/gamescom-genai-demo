import boto3
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from backend_functions.ask_question import create_bedrock_llm, get_opensearch_endpoint, create_langchain_vector_embedding_using_bedrock, get_secret, create_opensearch_vector_search_client

bedrock_model_id = "anthropic.claude-v2"
bedrock_embedding_model_id = "amazon.titan-embed-text-v1"
index_name = 'rag'

bedrock_client = boto3.client("bedrock-runtime")
bedrock_llm = create_bedrock_llm(bedrock_client, bedrock_model_id)
bedrock_embeddings_client = create_langchain_vector_embedding_using_bedrock(bedrock_client, bedrock_embedding_model_id)
opensearch_endpoint = get_opensearch_endpoint(domain_name=index_name)
opensearch_password = get_secret(secret_prefix=index_name)
opensearch_vector_search_client = create_opensearch_vector_search_client(index_name, opensearch_password, bedrock_embeddings_client, opensearch_endpoint)


prompt_template = """ 
You are a very polite customer service agent, who has received the following question from a user. The user is a player of a Game your company makes.
Use the following pieces of context to provide and answer to the customer.

{context}

Question: {question}
Answer:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


qa = RetrievalQA.from_chain_type(llm=bedrock_llm, 
                                    chain_type="stuff", 
                                    retriever=opensearch_vector_search_client.as_retriever(),
                                    return_source_documents=True,
                                    chain_type_kwargs={"prompt": PROMPT, "verbose": True},
                                    verbose=False)


question = st.text_area("Please enter your question below:")
if st.button("Submit Question"):
    response = qa(question, return_only_outputs=False)
    st.write(f"{response.get('result')}")