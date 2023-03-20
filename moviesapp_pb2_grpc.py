# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import moviesapp_pb2 as moviesapp__pb2


class MovieStub(object):
    """The service definition.

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetMovies = channel.unary_stream(
                '/mycrudgrpc.Movie/GetMovies',
                request_serializer=moviesapp__pb2.Empty.SerializeToString,
                response_deserializer=moviesapp__pb2.MovieInfo.FromString,
                )
        self.GetMovie = channel.unary_unary(
                '/mycrudgrpc.Movie/GetMovie',
                request_serializer=moviesapp__pb2.Uuid.SerializeToString,
                response_deserializer=moviesapp__pb2.MovieInfo.FromString,
                )
        self.CreateMovie = channel.unary_unary(
                '/mycrudgrpc.Movie/CreateMovie',
                request_serializer=moviesapp__pb2.MovieInfo.SerializeToString,
                response_deserializer=moviesapp__pb2.Uuid.FromString,
                )
        self.UpdateMovie = channel.unary_unary(
                '/mycrudgrpc.Movie/UpdateMovie',
                request_serializer=moviesapp__pb2.MovieInfo.SerializeToString,
                response_deserializer=moviesapp__pb2.Status.FromString,
                )
        self.DeleteMovie = channel.unary_unary(
                '/mycrudgrpc.Movie/DeleteMovie',
                request_serializer=moviesapp__pb2.Uuid.SerializeToString,
                response_deserializer=moviesapp__pb2.Status.FromString,
                )


class MovieServicer(object):
    """The service definition.

    """

    def GetMovies(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMovie(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateMovie(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateMovie(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteMovie(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MovieServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetMovies': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMovies,
                    request_deserializer=moviesapp__pb2.Empty.FromString,
                    response_serializer=moviesapp__pb2.MovieInfo.SerializeToString,
            ),
            'GetMovie': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMovie,
                    request_deserializer=moviesapp__pb2.Uuid.FromString,
                    response_serializer=moviesapp__pb2.MovieInfo.SerializeToString,
            ),
            'CreateMovie': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateMovie,
                    request_deserializer=moviesapp__pb2.MovieInfo.FromString,
                    response_serializer=moviesapp__pb2.Uuid.SerializeToString,
            ),
            'UpdateMovie': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateMovie,
                    request_deserializer=moviesapp__pb2.MovieInfo.FromString,
                    response_serializer=moviesapp__pb2.Status.SerializeToString,
            ),
            'DeleteMovie': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteMovie,
                    request_deserializer=moviesapp__pb2.Uuid.FromString,
                    response_serializer=moviesapp__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mycrudgrpc.Movie', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Movie(object):
    """The service definition.

    """

    @staticmethod
    def GetMovies(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mycrudgrpc.Movie/GetMovies',
            moviesapp__pb2.Empty.SerializeToString,
            moviesapp__pb2.MovieInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMovie(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mycrudgrpc.Movie/GetMovie',
            moviesapp__pb2.Uuid.SerializeToString,
            moviesapp__pb2.MovieInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateMovie(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mycrudgrpc.Movie/CreateMovie',
            moviesapp__pb2.MovieInfo.SerializeToString,
            moviesapp__pb2.Uuid.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateMovie(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mycrudgrpc.Movie/UpdateMovie',
            moviesapp__pb2.MovieInfo.SerializeToString,
            moviesapp__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteMovie(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mycrudgrpc.Movie/DeleteMovie',
            moviesapp__pb2.Uuid.SerializeToString,
            moviesapp__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
