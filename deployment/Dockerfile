FROM python:3.11-slim
WORKDIR /app
COPY deployment/requirements.txt deployment/requirements.txt
RUN pip install --no-cache-dir -r deployment/requirements.txt && pip install --no-cache-dir "torch>=2.3,<3" --index-url https://download.pytorch.org/whl/cpu
COPY src/ src/
COPY inference/ inference/
COPY deployment/ deployment/
COPY ui/ ui/
COPY tokenizer/ tokenizer/
COPY checkpoints/model.pt checkpoints/model.pt
ENV PORT=8000
ENV CHECKPOINT_PATH=checkpoints/model.pt
EXPOSE 8000
# Model va sahifa bitta port orqali ochiladi.
CMD ["sh", "-c", "uvicorn deployment.app:app --host 0.0.0.0 --port ${PORT}"]
