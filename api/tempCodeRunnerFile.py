movie_id = "1234"  # Invalid UUID format
uuid_str = str(uuid.UUID(int=int(movie_id)))
print(uuid_str)  # Prints "00000000-0000-0000-0000-0000000004d2"