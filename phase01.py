import csv
from collections import defaultdict
from pathlib import Path

BASIS = Path(__file__).parent

def load_movie(path="movies.csv"):
    movies = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["movieId"]] = {
                "title": row["title"],
                "genres": row["genres"].split("|"),
            }
    return movies

def load_ratings(path="ratings.csv"):
    ratings = []
    with open(path, newline = "", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ratings.append(
                {
                "userId":row["userId"],
                "movieId":row["movieId"],
                "rating": float(row["rating"])
                }
            )
    return ratings

def top_filme(movies, ratings, top_n=10, min_bewertungen = 20):
    summen = defaultdict(float)
    anzahl = defaultdict(int)
    for r in ratings:
        summen[r["movieId"]] += r["rating"]
        anzahl[r["movieId"]] += 1

    ergebnis = []
    for movie_id, summe in summen.items():
        anz = anzahl[movie_id]
        if anz >= min_bewertungen and movie_id in movies:
            durchschnitt = summe / anz
            titel = movies[movie_id]["title"]
            ergebnis.append((titel, durchschnitt, anz))

    ergebnis.sort(key=lambda x: x[1], reverse=True)
    return ergebnis[:top_n]

def bewertung_pro_genre(movies, ratings):
    genre_counts = defaultdict(int)
    for r in ratings:
        movie_id = r["movieId"]
        if movie_id in movies:
            for genre in movies[movie_id]["genres"]:
                genre_counts[genre] += 1
    return dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True))

def main():
    movies = load_movie(BASIS / "movies.csv")
    ratings = load_ratings(BASIS / "ratings.csv")

    print(f"Anzahl Filme: {len(movies)}")
    print(f"Anzahl Bewertungen: {len(ratings)}")

    print("\nTop 10 Filme nach Durchschnittsbewertung (mindestens 20 Bewertungen):")
    for titel, durchschnitt, anzahl in top_filme(movies, ratings):
        print(f"{titel}: {durchschnitt:.2f} ({anzahl} Bewertungen)")

    print("\nAnzahl Bewertungen pro Genre:")
    for genre, count in bewertung_pro_genre(movies, ratings).items():
        print(f"{genre}: {count} Bewertungen")

if __name__ == "__main__":
    main()
