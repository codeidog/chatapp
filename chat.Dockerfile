FROM python:3.8.6-alpine3.12 as build
RUN apk add --no-cache gcc libffi-dev openssl-dev musl-dev
WORKDIR /app
RUN python3 -m venv venv
ENV PATH=:/app/venv/bin:$PATH
RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN chmod u+x entrypoint.sh

FROM python:3.8.6-alpine3.12 as run
RUN adduser -HD -u 1000 chat
COPY --from=build --chown=chat:chat /app /app
WORKDIR /app
USER chat
ENV PATH=:/app/venv/bin:$PATH
ENTRYPOINT ["entrypoint.sh"]
