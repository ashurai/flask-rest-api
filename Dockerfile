FROM python:3.5

WORKDIR /usr/src/app

COPY requirement.txt requirement.txt

RUN pip install --upgrade pip
RUN pip install -r requirement.txt

COPY . .

RUN useradd -ms /bin/bash search-bookmark
USER search-bookmark

EXPOSE 4000

ENTRYPOINT ["python","index.py"]