# QA Bot with Retrieval-Augmented Generation (RAG)
This repository contains a QA Bot built using Retrieval-Augmented Generation (RAG) model architecture. The system allows users to upload documents and ask questions about the content in real-time. The bot uses the Cohere API to generate embeddings and retrieve relevant answers from a vector database.

## Table of Contents<br>
1.Project Overview<br>
2.Features<br>
3.Tech Stack<br>
4.Setup Instructions<br>
5.Usage Instructions<br>
6.Deployment with Docker<br>
7.Example Queries<br>
8.Contributing<br>
9.License<br>
## Project Overview<br>
This project implements a QA bot that can answer questions about uploaded documents. The system uses a Retrieval-Augmented Generation (RAG) approach, combining document embeddings (retrieved via Cohere API) with a generative model to provide meaningful and context-aware answers. The bot can handle large documents and process multiple queries efficiently.

## Features<br>
1.Upload document functionality<br>
2.Real-time QA system with accurate responses<br>
3.Uses Cohere API for document embeddings<br>
4.Efficient retrieval with a vector database (e.g., Pinecone)<br>
5.Frontend interface built with Streamlit or Gradio<br>

## Tech Stack<br>
1.**Backend:** Python, Cohere API, Pinecone (for vector storage)<br>
2.**Frontend:** Streamlit / Gradio (for real-time interaction)<br>
3.**Containerization:** Docker<br>
4.**Deployment:** GitHub repository and Docker-based deployment<br>

## Setup Instructions<br>
1. Clone the Repository<br>
git clone https://github.com/Shilpi1307/QA_BOT.git<br>
cd QA_BOT<br>
2. Create and Activate Virtual Environment<br>
python -m venv venv<br>
source venv/bin/activate  # On Windows use: venv\Scripts\activate<br>
3. Install Dependencies<br>
pip install -r requirements.txt<br>
4. Set Up Cohere API Key<br>
You will need a Cohere API key to run this project. Obtain the API key from Cohere's website. Once you have it, you can either:<nr>
Set it as an environment variable:<br>
export COHERE_API_KEY=your-api-key<br>
5. Set Up Pinecone <br>
If you are using Pinecone as your vector database, you will need to initialize Pinecone with an API key. Follow Pinecone’s documentation to set it up: Pinecone Documentation https://docs.pinecone.io/guides/get-started/quickstart#next-steps.

## Usage Instructions<br>
1. Running the QA Bot<br>
You can run the bot either with Streamlit or Gradio.<br>
**For Streamlit:** streamlit run app.py<br>
**For Gradio:** python app_gradio.py<br>
2. Interacting with the Bot
Once the app is running, a web interface will be available where you can:<br>
**Upload Documents:**Upload text files or PDFs that the bot will analyze.<br>
**Ask Questions:** Enter questions related to the content of the uploaded document, and the bot will provide context-based answers.<br>

## Deployment with Docker<br>
1. Build the Docker Image<br>
Make sure you have Docker installed and running on your machine. Then, build the Docker image using the following command:<br>
docker build -t qa-bot:latest .<br>
2. Run the Docker Container<br>
To run the application inside a Docker container:<br>
docker run -p 8501:8501 -e COHERE_API_KEY=your-api-key qa-bot:latest <br>
This will start the application, and it will be accessible at http://localhost:8501.<br>

## Example Queries<br>
Here are some example queries you can try after uploading a document:<br>

1."What is the main topic of the document?"<br>
2."Summarize the document for me."<br>
3."What are the key points discussed in the third section?"<br>

## Contributing<br>
If you want to contribute to this project, feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.<br>

## Steps to contribute:<br>
1.Fork this repository<br>
2.Create a new branch (git checkout -b feature-branch)<br>
3.Commit your changes (git commit -m 'Add new feature')<br>
4.Push to the branch (git push origin feature-branch)<br>
5.Open a pull request<br>
## License<br>
This project is licensed under the MIT License. See the LICENSE file for details.

