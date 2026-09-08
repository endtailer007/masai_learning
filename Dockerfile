FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

COPY RAG_chatbot/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY RAG_chatbot/streamlit_app.py ./streamlit_app.py
COPY RAG_chatbot/data ./data

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]

# Build command:
#docker build -t nova-tech-rag-bot .

# Run command:
# docker run -d -p 10000:8501 -e GEMINI_API_KEY=your_gemini_api_key nova-tech-rag-bot
