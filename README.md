# my-crud-grpc

This is a simple CRUD application using gRPC, data is store "in memory".

Followed the tutorial from [here](https://www.youtube.com/watch?v=4gsDeKVfUUI), re-implemented it using Python.

## How to run

### Server

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Client

```bash
# reflection:
grpcurl -plaintext localhost:50051 list

# listing all:
grpcurl -plaintext localhost:50051 mycrudgrpc.Movie/GetMovies

# adding a movie:
grpcurl -plaintext -d '{"title": "Titanic", "description": "In 1912, the Titanic, the world s most luxurious passenger ship, set out across the Atlantic for New York City. It would never see it s destination.", "director":{"name":"James","surname":"Cameron"}}' localhost:50051 mycrudgrpc.Movie/CreateMovie

# updating a movie (uuid from previous command):
grpcurl -plaintext -d '{"uuid": "f86cb45c-b9db-4240-a131-513a39838d3e", "title": "Titanic", "description": "In 1912, the Titanic, the world s most luxurious passenger ship, set out across the Atlantic for New York City. It would never see it s destination.", "director":{"name":"James","surname":"Camaleon"}}' localhost:50051 mycrudgrpc.Movie/UpdateMovie

# getting a movie (uuid from adding movie command):
grpcurl -plaintext -d '{"uuid": "f86cb45c-b9db-4240-a131-513a39838d3e"}' localhost:50051 mycrudgrpc.Movie/GetMovie

# deleting a movie (uuid from adding movie command):
grpcurl -plaintext -d '{"uuid": "f86cb45c-b9db-4240-a131-513a39838d3e"}' localhost:50051 mycrudgrpc.Movie/DeleteMovie
```

## Proxy to convert gRPC to REST

Using Kong to convert gRPC to REST.

### Run Kong

```bash
docker run -it --rm \
  -p 8000:8000 \
  -p 8001:8001 \
  -e KONG_DATABASE=off \
  -e KONG_DECLARATIVE_CONFIG=/tmp/kong.yaml \
  -e "KONG_ADMIN_LISTEN=0.0.0.0:8001" \
  -v ./kong/kong.yaml:/tmp/kong.yaml \
  -v ./protos:/tmp/protos \
  kong:3
```

### Run gRPC server

```bash
docker build -t leandrocarneiro/crud-grpc-python .

docker run -it --rm --name=moviesapp \
  -p 50051:50051 \
  leandrocarneiro/crud-grpc-python:latest
```

### curl (and jq) as client

```bash
# listing all (TODO: this is not returning a json array, but one json object per "line". maybe because it is a stream?):
curl -s localhost:8000/v1/movies | jq .

# adding a movie:
curl -s -X POST localhost:8000/v1/movies \
  -H "Content-Type: application/json" \
  -d '{"title": "Titanic", "description": "In 1912, the Titanic, the world s most luxurious passenger ship, set out across the Atlantic for New York City. It would never see it s destination.", "director":{"name":"James","surname":"Cameron"}}' | jq .

# updating a movie (uuid from previous command):
curl -s -X PUT localhost:8000/v1/movies/5e5cd7f4-14d5-4040-b983-4e592092fb58 \
  -H "Content-Type: application/json" \
  -d '{"title": "Titanic", "description": "In 1912, the Titanic, the world s most luxurious passenger ship, set out across the Atlantic for New York City. It would never see it s destination.", "director":{"name":"James","surname":"Camaleon"}}' | jq .

# getting a movie (uuid from adding movie command):
curl -s localhost:8000/v1/movies/5e5cd7f4-14d5-4040-b983-4e592092fb58 | jq .

# deleting a movie (uuid from adding movie command):
curl -s -X DELETE localhost:8000/v1/movies/5e5cd7f4-14d5-4040-b983-4e592092fb58 | jq .
```

## Istio and gRPC

Note we are outputing the "Proto Descriptor" file from the gRPC server when building the image (see `Dockerfile`). (Note: flags `--include_imports` and `--include_source_info` are needed to make the file compatible with Envoy.)

```bash
python -m grpc_tools.protoc \
  -I googleapis -I protos \
  --python_out=. \
  --grpc_python_out=. \
  --include_imports \
  --include_source_info \
  # here \/
  --descriptor_set_out=proto.descriptor \
  protos/moviesapp.proto
```

This file is used by the Envoy proxy to convert the gRPC request to HTTP/1.1.

The filter supports passing the proto descriptor file in two ways:

- As a file in the local file system, using the `filename` field in the proto descriptor set configuration.
- As a base64-encoded string, using the `inline_bytes` field in the proto descriptor set configuration.

Let's use the second option, as it is easier to configure. Get the file from the container and convert it to base64.

```bash
docker run -it --rm --entrypoint=/bin/bash leandrocarneiro/my-crud-grpc:python -c "cat /app/proto.descriptor | base64 -w0"
```

Then use it in the `EnvoyFilter` resource, as `protoDescriptorBin` config.

Check the `k8s-manifests` folder for the `EnvoyFilter` resource.
