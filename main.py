from concurrent import futures
import time
import logging
from grpc_reflection.v1alpha import reflection
from uuid import uuid4
from os import getenv

import grpc

import moviesapp_pb2
import moviesapp_pb2_grpc

from json import loads

MOVIES_DICT = loads('''[
    {
        "uuid": "47334661-39ab-4667-9586-7e41e8e6c391",
        "title": "The Matrix",
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "director": {
            "name": "Lana",
            "surname": "Wachowski"
        }
    },
    {
        "uuid": "3de10bb5-b388-4158-b167-dd0680934052",
        "title": "The Matrix Reloaded",
        "description": "Neo and the rebel leaders estimate that they have 72 hours until 250,000 probes discover Zion and destroy it and its inhabitants. During this, Neo must decide how he can save Trinity from a dark fate in his dreams.",
        "director": {
            "name": "Lana",
            "surname": "Wachowski"
        }
    }
]''')

MOVIES = []


class MovieServicer(moviesapp_pb2_grpc.MovieServicer):
    def GetMovies(self, request, context):
        logging.info("Getting movies")
        for movie in MOVIES:
            yield movie

    def GetMovie(self, request, context):
        logging.info("Getting movie: %s", request)
        for movie in MOVIES:
            if movie.uuid == request.uuid:
                return movie
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details(f'Movie with uuid {request.uuid} not found!')
        return moviesapp_pb2.Empty()

    def CreateMovie(self, request, context):
        logging.info("Creating movie: %s", request)
        request.uuid = str(uuid4())
        movie = moviesapp_pb2.MovieInfo(
            uuid=request.uuid, title=request.title, description=request.description, director=request.director)
        MOVIES.append(movie)
        return movie

    def UpdateMovie(self, request, context):
        logging.info("Updating movie: %s", request)
        for movie in MOVIES:
            if movie.uuid == request.uuid:
                movie.title = request.title
                movie.description = request.description
                movie.director.name = request.director.name
                movie.director.surname = request.director.surname
                return moviesapp_pb2.Status(success=True)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details(f'Movie with uuid {request.uuid} not found!')
        return moviesapp_pb2.Status(success=False)

    def DeleteMovie(self, request, context):
        logging.info("Deleting movie: %s", request)
        for movie in MOVIES:
            if movie.uuid == request.uuid:
                MOVIES.remove(movie)
                return moviesapp_pb2.Status(success=True)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details(f'Movie with uuid {request.uuid} not found!')
        return moviesapp_pb2.Status(success=False)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    moviesapp_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    BIND_ADDR = getenv('BIND_ADDR', '0.0.0.0:50051')
    server.add_insecure_port(BIND_ADDR)
    SERVICE_NAMES = (
        moviesapp_pb2.DESCRIPTOR.services_by_name['Movie'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    logging.info("Starting server. Listening on %s.", BIND_ADDR)
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    for movie in MOVIES_DICT:
        m = moviesapp_pb2.MovieInfo()
        m.uuid = movie["uuid"]
        m.title = movie["title"]
        m.description = movie["description"]
        m.director.name = movie["director"]["name"]
        m.director.surname = movie["director"]["surname"]
        MOVIES.append(m)
    serve()
