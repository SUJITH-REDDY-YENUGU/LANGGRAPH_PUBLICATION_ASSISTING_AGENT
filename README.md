
```markdown
# 📚 Publication Assisting Agent (LangGraph + FastAPI)

This repository contains the **FastAPI backend** powered by **LangGraph** and **LangChain**, deployed on Hugging Face Spaces.  
It processes uploaded `.txt` files using a Groq API key and generates structured outputs:

- ✅ Title  
- ✅ TLDR (summary)  
- ✅ Tags  
- ✅ References (valid HTTPS links)  
- ✅ Review status & feedback  

---

## 🚀 Live Deployment

👉 Hugging Face Space: [Sujith2121/publication-assisting-agent](https://huggingface.co/spaces/Sujith2121/publication-assisting-agent)  
👉 Swagger Docs: [hf.space/docs](https://Sujith2121-publication-assisting-agent.hf.space/docs)

---

## 📂 Project Structure

```
langgraph_app/
├── app.py              # FastAPI entrypoint
├── requirements.txt    # Dependencies
├── Dockerfile          # Hugging Face Spaces build
└── README.md           # Documentation
```

---

## 🔧 How to run locally

Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open the API docs at:  
👉 `http://localhost:8000/docs`

---

## 🛠️ API Usage

### Endpoint: `/process`

**Method:** `POST`  
**Params:**
- `file`: `.txt` file (multipart form upload)
- `groq_api_key`: string (your Groq API key)

**Response JSON:**
```json
{
  "title": "Navigating the Promise and Peril of Artificial Intelligence",
  "tldr": "• AI is transforming industries worldwide...\n• Challenges include ethical concerns...",
  "tags": ["Artificial Intelligence", "Industry Transformation", "Data Analysis"],
  "references": [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://www.bbc.com/news/technology-57890794"
  ],
  "review_status": "approved",
  "review_feedback": null
}
```

---

## ⚡ Notes

- Only `.txt` files are supported.  
- Requires a valid **Groq API key**.  
- Designed with **LangGraph retry logic** for robust workflow execution.  
- Deployed on Hugging Face Spaces with Docker for reproducibility.

---

## 📜 License

MIT License
```

---
