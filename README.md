# RAG Workshop

RAG (Retrieval Augmented Generation), is an advanced AI architecture that combines the power of information retrieval with generative AI models. The key idea is to enhance the generative AI model's output by retrieving relevant information from a collection of documents or data sources. This approach improves the accuracy and relevance of the generated content by grounding it in real-world data.

The purpose of this repository is to reflect the RAG process in a hands-on workshop, following the best practices, along with tools and techniques for testing and evaluation.

This document is divided in sections that follow the standard order of implementation for an end-to-end implementation of a RAG solution for learning purposes.

## How to use this repository

This repository is designed as a comprehensive learning resource for building a Retrieval-Augmented Generation (RAG) implementation using Generative AI models and a search engine. Whether you're new to these concepts or looking to refine your skills, you can tailor your experience based on your needs. You have the flexibility to dive into specific sections, utilizing the specific notebooks and guidance provided to explore particular topics in depth. This approach allows you to leverage the repository's resources to address specific challenges or questions you might encounter in your projects.

Alternatively, if you're aiming for a holistic understanding of RAG implementations, you can follow the repository in a sequential manner. By proceeding through the sections in order, you'll gain a step-by-step overview of the entire process, from foundational concepts to advanced techniques. This pathway is ideal for those who want a complete end-to-end review, ensuring a thorough grasp of how to build and optimize RAG systems. Whichever approach you choose, this repository serves as a valuable educational tool to enhance your knowledge and skills in this cutting-edge area.

The examples of data sources connections can be customized to your own sources:
- Connection to PostgreSQL database: you can configure the connection parámeters to your dabase in the .env file
- Database connection thru a API REST endpoint: in the repo is included a sample SQLite database and a small endpoint configuration with flask.
- Sample PDF files in the 'docs' folder.

**Presentation with RAG explaination and Workshop details**
[RAG_workshop.pdf](RAG_workshop.pdf)

## Key components:
- **Indexing**: create AI Search indexes, process documents chunking and indexing them. In this repo there are three examples of data sources to index:
   + a PostgreSQL database accessed thru its host, user and password.
   + a SQLite database accessed thru an endpoint configured with flask.
   + PDF files in the 'docs' folder.
- **Search and Retrieval**: The solution retrieves with hybrid search with Semantic ranker of Azure AI Search the most relevant indexed documents or chunks to the user's question. This step ensures that the generated responses are informed by curated information.
- **Augmentation**: The retrieved information is then reviewed semantically compared with the user's question to select only the most relevant chunks. This augmentation helps in producing contextually accurate and informative responses.
- **Answer Generation**: Finally, the generative AI model, in this case Azure Open AI GPT model, generate responses or content based on the context provided by the most relevant chunks. Two options are included: with and without conversation history in the response generation.
- **Evaluation**: analyze the answers and the context to evaluate the similarity with a ground truth (with expected answers to specific questions) and if the answer was grounded on the context or not.
- **Demo Application**: A simple web demo application (rag_chat.py) is provided to query the indexed contents.
   + To start the application, run the following command: streamlit run rag_chat.py
   <img src="./Demo_RAG_chat.gif" alt="Demo RAG chat"/>

## How RAG works in Azure
In this implementation, we leverage Azure AI Services to build a RAG solution. The key services for this repository are:
- **Azure AI Search**: A robust search service that helps retrieve relevant information from a large corpus, ensuring that the generative model has access to the most pertinent data. More info: https://learn.microsoft.com/en-us/azure/search/
- **Azure Open AI Service**: Provides state-of-the-art generative models capable of understanding and generating human-like text. More info: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- **Azure Document Intelligence**: converts PDF files to markdown format and makes OCR of images. More info: https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence

The repository follows a structured process, and it is meant to be used to implement an end-to-end RAG solution.

The following diagram represents the reference standard process that encompasses many of the different aspects to consider for a successful implementation of this solution:

<img src="./images/anatomy_of_rag.png" alt="Anatomy of RAG"/>

## Table of contents
<!--ts-->
   * [1. Indexing](./1-indexing/indexing.ipynb)

   * [2. 3. 4. Search, Augmentation and Answer generation](./2_3_4_search_augment_generate/search_augment_generate.ipynb)

   * [5. Evaluation](./5_evaluation/evaluation.ipynb)

   * [6. Demo RAG chat](./6_demo_rag_chat/README.md)

<!--te-->

## Prerequisites
+ An Azure subscription, with [access to Azure OpenAI](https://aka.ms/oai/access).
+ An Azure OpenAI service with the service name and an API key.
+ An instance of GPT-4o model on the Azure OpenAI Service.
+ An instance of Azure AI Search.
+ An instance Document Intelligence service.

I used Python 3.12.10, [Visual Studio Code with the Python extension](https://code.visualstudio.com/docs/python/python-tutorial), and the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) to test the notebooks.

### Set up a Python virtual environment in Visual Studio Code

1. Open the Command Palette (Ctrl+Shift+P).
2. Search for **Python: Create Environment**.
3. Select **Venv**.
4. Select a Python interpreter. Choose 3.12 or later.

It can take a minute to set up. If you run into problems, see [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments).

### Environment Configuration

Create a `.env` file in the root directory of your project with the following content. You can use the provided [`.env-sample`](.env-sample) as a template:

**Azure OpenAI configuration variables**
```
AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
AZURE_OPENAI_DEPLOYMENT_NAME=<your_azure_openai_deployment_name>
AZURE_OPENAI_API_VERSION=<your_azure_openai_api_version>
```

**Azure AI Search configuration variables**
```
SEARCH_SERVICE_ENDPOINT="https://<your_ai_search_service>.search.windows.net"
SEARCH_INDEX_NAME=<your_index_name>
SEARCH_SERVICE_QUERY_KEY="you_ai_search_key"
```

**Azure Document Intelligence variables**
```
DOC_INTEL_ENDPOINT=<your_document_intelligence_end_point>
DOC_INTEL_KEY=<your_document_intelligence_key>
```

**PostgreSQL Database Connection**
```
PG_HOST=<your-pg-host>
PG_PORT=<your-pg-port>
PG_USER=<your-pg-user>
PG_PASSWORD=<your-pg-password>
PG_DATABASE=<your-pg-database>
```

**SQLite Database endpoint**
```
SQLITE_ENDPOINT=http://127.0.0.1:5000/sqlite-query
SQLITE_USER=<your_user>
SQLITE_PASSWORD=<your_password>
```
The needed libraries are specified in [requirements.txt](requirements.txt).