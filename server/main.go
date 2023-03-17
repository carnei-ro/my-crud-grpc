package main

import (
	"context"
	"log"
	"net"

	pb "github.com/carnei-ro/my-crud-grpc/protos"
	"github.com/google/uuid"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/reflection"
	"google.golang.org/grpc/status"
)

const (
	port = ":50051"
)

// this is a mock database
var movies []*pb.MovieInfo

type movieServer struct {
	pb.UnimplementedMovieServer
}

func main() {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterMovieServer(s, &movieServer{})
	reflection.Register(s) // grpcurl -plaintext localhost:50051 list

	log.Printf("Server listening on port %s", port)

	// create some mock data
	initMovies()

	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

func initMovies() {
	movies = append(movies, &pb.MovieInfo{
		Uuid:        uuid.New().String(),
		Title:       "The Matrix",
		Description: "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
		Director: &pb.Director{
			Name:    "Lana",
			Surname: "Wachowski",
		},
	})
	movies = append(movies, &pb.MovieInfo{
		Uuid:        uuid.New().String(),
		Title:       "The Matrix Reloaded",
		Description: "Neo and the rebel leaders estimate that they have 72 hours until 250,000 probes discover Zion and destroy it and its inhabitants. During this, Neo must decide how he can save Trinity from a dark fate in his dreams.",
		Director: &pb.Director{
			Name:    "Lana",
			Surname: "Wachowski",
		},
	})
}

func (s *movieServer) GetMovies(in *pb.Empty, stream pb.Movie_GetMoviesServer) error {
	log.Printf("GetMovies - Received 'in': %v", in)

	for _, movie := range movies {
		if err := stream.Send(movie); err != nil {
			return err
		}
	}
	return nil
}

func (s *movieServer) GetMovie(ctx context.Context, in *pb.Uuid) (*pb.MovieInfo, error) {
	log.Printf("GetMovie - Received 'in': %v", in)

	for _, movie := range movies {
		if movie.GetUuid() == in.GetUuid() {
			return movie, nil
		}
	}
	return nil, nil
}

func (s *movieServer) CreateMovie(ctx context.Context, in *pb.MovieInfo) (*pb.Uuid, error) {
	log.Printf("CreateMovie - Received 'in': %v", in)

	in.Uuid = uuid.New().String()
	movies = append(movies, in)
	return &pb.Uuid{Uuid: in.GetUuid()}, nil
}

func (s *movieServer) UpdateMovie(ctx context.Context, in *pb.MovieInfo) (*pb.Status, error) {
	log.Printf("UpdateMovie - Received 'in': %v", in)

	for i, movie := range movies {
		if movie.GetUuid() == in.GetUuid() {
			movies[i] = in
			return &pb.Status{Success: true}, nil
		}
	}
	return nil, status.Error(codes.NotFound, "id was not found")
}

func (s *movieServer) DeleteMovie(ctx context.Context, in *pb.Uuid) (*pb.Status, error) {
	log.Printf("DeleteMovie - Received 'in': %v", in)

	for i, movie := range movies {
		if movie.GetUuid() == in.GetUuid() {
			movies = append(movies[:i], movies[i+1:]...)
			return &pb.Status{Success: true}, nil
		}
	}
	return nil, status.Error(codes.NotFound, "id was not found")
}
