FROM python:3.10.6-alpine
# Or any preferred Python version.
ADD subscriber.py .
ADD requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir && rm -f requirements.txt
CMD python subscriber.py