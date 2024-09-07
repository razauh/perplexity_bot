
# Perplexity_Bot - Query LLMs Without GPUs

Are you looking to leverage the power of Large Language Models (LLMs) but don't have the GPU resources to run them locally? **Perplexity_Bot** is your solution! This project provides a FastAPI-based interface to interact with state-of-the-art LLMs served by Perplexity. Deploy it easily, ask your questions, and receive intelligent responses without the need for expensive hardware!

## 📌 Features
- **No GPU Required:** Run queries against LLMs served by Perplexity, eliminating the need for local GPU resources.
- **Flexible API:** A generalized FastAPI endpoint that allows you to submit any question and receive insightful answers.
- **Asynchronous Processing:** Efficiently handles multiple requests using asynchronous capabilities.
- **Dynamic and Scalable:** Easily deploy on any server or cloud environment.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- FastAPI and Uvicorn
- Playwright

## Installation

### Clone the Repository:
```bash
git clone https://github.com/razauh/perplexity_bot.git
cd perplexity_bot
```

### Install the Required Packages:
```bash
pip install fastapi uvicorn playwright
playwright install
```

### Run the API:
```bash
uvicorn perplexity_bot:app --reload
```
Your API will be running on [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## 📝 How to Use

### Submit a Query: 
Send a POST request to `/ask` with a JSON body containing your question:

```json
{
    "question": "Your question here"
}
```

### Example using curl:
```bash
curl -X 'POST' 
  'http://127.0.0.1:8000/ask' 
  -H 'Content-Type: application/json' 
  -d '{"question": "What is the main focus of the Python file in the TensorFlow issue?"}'
```

## 🌍 Why Use Perplexity_Bot?

- **No Need for Costly GPUs:** Utilize the power of Perplexity's LLMs without local computational resources.
- **Developer-Friendly:** Easily integrate this API into your existing applications or tools.
- **Real-Time Interactions:** Get real-time answers to your questions with state-of-the-art LLMs.

## 🙌 Contributing

We welcome contributions to make Perplexity_Bot even better! Feel free to fork the repository, make changes, and submit a pull request.
