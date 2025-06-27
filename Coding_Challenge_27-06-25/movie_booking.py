movies = {
    "Pushpa": 150,
    "Dangal": 180,
    "Bahubali": 200,
    "RRR": 120
}

def show_movies():
    print("Available Movies:")
    for i, (movie, price) in enumerate(movies.items(), 1):
        print(f"{i}. {movie} - ₹{price}")

def book_movie():
    show_movies()
    choice = int(input("Select movie number: "))
    movie_list = list(movies.keys())
    
    if 1 <= choice <= len(movie_list):
        selected_movie = movie_list[choice - 1]
        num_tickets = int(input("Enter number of tickets: "))
        total = calculate_amount(selected_movie, num_tickets)
        print(f"Booking confirmed for '{selected_movie}' - Total: ₹{total}")
        return selected_movie, total
    else:
        print("Invalid selection.")
        return None, 0

def calculate_amount(movie, tickets):
    return movies[movie] * tickets

if __name__ == "__main__":
    book_movie()
