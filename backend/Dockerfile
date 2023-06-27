FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /backend
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod o+x /entrypoint.sh

ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]