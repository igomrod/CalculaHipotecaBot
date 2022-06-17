FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN useradd -ms /bin/bash app
USER app
WORKDIR /home/app/

COPY . .

# run test
RUN pip3 install -r ./tests/requirements.txt
RUN python3 -m pytest -p no:cacheprovider

CMD [ "python3", "cli.py"]
