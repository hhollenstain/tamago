FROM python:3.6-alpine

COPY . /app
WORKDIR /app

RUN apk add ffmpeg gcc musl-dev libffi-dev make opus-dev
RUN pip install -e "."

CMD ["tamago"]
