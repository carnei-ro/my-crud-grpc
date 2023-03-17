# my-crud-grpc

This is a simple CRUD application using gRPC, data is store "in memory".

Followed the tutorial from [here](https://www.youtube.com/watch?v=4gsDeKVfUUI)

## How to run

### Server

```bash
cd server
go run main.go
```

### Client

```bash
# reflection:
grpcurl -plaintext localhost:50051 list

# listing all:
grpcurl -plaintext localhost:50051 mycrudgrpc.Movie/GetMovies

# adding a movie:
grpcurl -plaintext -d '{"title": "Titanic", "description": "In 1912, the Titanic, the world s most luxurious passenger ship, set out across the Atlantic for New York City. It would never see it s destination.", "director":{"name":"James","surname":"Cameron"}}' localhost:50051 mycrudgrpc.Movie/CreateMovie

# updating a movie:
grpcurl -plaintext -d '{"uuid": "f86cb45c-b9db-4240-a131-513a39838d3e", "title": "Titanic", "description": "In 1912, the Titanic, the world s most luxurious passenger ship, set out across the Atlantic for New York City. It would never see it s destination.", "director":{"name":"James","surname":"Camaleon"}}' localhost:50051 mycrudgrpc.Movie/UpdateMovie

# getting a movie:
grpcurl -plaintext -d '{"uuid": "f86cb45c-b9db-4240-a131-513a39838d3e"}' localhost:50051 mycrudgrpc.Movie/GetMovie

# deleting a movie:
grpcurl -plaintext -d '{"uuid": "f86cb45c-b9db-4240-a131-513a39838d3e"}' localhost:50051 mycrudgrpc.Movie/DeleteMovie
```

