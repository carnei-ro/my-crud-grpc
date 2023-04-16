FROM python:3.11 AS builder

RUN apt update && \
  apt install -y build-essential && \
  pip install -U setuptools pip && \
  python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONASYNCIODEBUG=1

WORKDIR /protoc

COPY requirements.txt .
COPY protos ./protos
RUN pip install -r requirements.txt --use-pep517
RUN git clone https://github.com/googleapis/googleapis.git
RUN python -m grpc_tools.protoc -I googleapis -I protos --python_out=. --grpc_python_out=. --include_imports --include_source_info --descriptor_set_out=proto.descriptor protos/moviesapp.proto

FROM python:3.11 AS app

WORKDIR /app

ENV APP_DIR=/app \
    APP_USER=app \
    PATH="/opt/venv/bin:$PATH"

RUN set -ex \
 && addgroup --gid 673 "$APP_USER" \
 && adduser --no-create-home --uid=673 --gid=673 "$APP_USER"

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /protoc/*.py "$APP_DIR/"
COPY --from=builder /protoc/proto.descriptor "$APP_DIR/"

COPY main.py "$APP_DIR"

USER "$APP_USER"

ENTRYPOINT ["python", "/app/main.py"]

EXPOSE 50051
