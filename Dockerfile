FROM python:3.6-alpine

COPY . /app
WORKDIR /app

RUN apk add ffmpeg gcc musl-dev libffi-dev git make opus-dev
RUN make live

CMD ["tamago"]
