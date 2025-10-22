FROM python
COPY . .
RUN apt-get update
RUN apt-get install build-essential python3-dev libffi-dev libzmq3-dev -y
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "main.py"]
