FROM python

RUN apt-get update && apt-get install build-essential python3-dev libffi-dev libzmq3-dev -y

WORKDIR /usr/src/app
EXPOSE 5000

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]