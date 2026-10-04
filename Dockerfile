FROM python:3.12-slim
WORKDIR /app
COPY . .
ENV PYTHONPATH=/app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 6379
CMD ["python","-m","pyredis"]
