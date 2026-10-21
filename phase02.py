from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

BASIS = Path(__file__).parent

def lade_daten():
    movies = pd.read_csv(BASIS / "movies.csv")
    ratings = pd.read_csv(BASIS / "ratings.csv")
    return movies, ratings

def daten_prufen(movies, ratings):
    for name, df in [("movies", movies), ("ratings", ratings)]:
        print(f"{name}")
        print(df.head())
        print(f"\nForm (Zeilen, Spalten): {df.shape}")
        print(f"Fehlende Werte pro Spalte:\n{df.isna().sum()}")
        print(f"Doppelte Zeilen: {df.duplicated().sum()}")

    print("\nStatistik der Bewertungen")
    print(ratings["rating"].describe())

def bereinigen(movies, ratings):
    movies = movies.drop_duplicates()
    ratings = ratings.drop_duplicates().dropna(subset=["rating"]).copy()

    ratings["datum"] = pd.to_datetime(ratings["timestamp"], unit="s")
    ratings["bewertungsjahr"] = ratings["datum"].dt.year

    jahr = movies["title"].str.extract(r"\((\d{4})\)\s*$", expand=False)
    movies["erscheinungsjahr"] = pd.to_numeric(jahr)

    return movies, ratings

def zusammenfuhren(movies, ratings):
    df = ratings.merge(movies, on="movieId", how="inner")
    return df

def top_filme(df, top = 10, min_bewertungen = 20):
    stats = df.groupby("title")["rating"].agg(durchschnitt="mean", anzahl="count")
    stats = stats[stats["anzahl"] >= min_bewertungen]
    return stats.sort_values("durchschnitt", ascending=False).head(top)

def genre_statistik(df):
    df_genre = df.assign(genre=df["genres"].str.split("|")).explode("genre")
    stats = df_genre.groupby("genre")["rating"].agg(anzahl="count", durchschnitt="mean")
    return stats.sort_values("anzahl", ascending=False)

def diagramme_erstellen(df, genre_stats):
    """Drei Diagramme: Verteilung der Bewertungen, Genres, Bewertungen pro Jahr."""
    # 1. Verteilung der Bewertungen
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    df["rating"].value_counts().sort_index().plot(kind="bar", ax=ax1)
    ax1.set_title("Verteilung der Bewertungen")
    ax1.set_xlabel("Bewertung")
    ax1.set_ylabel("Anzahl")
    fig1.tight_layout()
    fig1.savefig(BASIS / "diagramm_bewertungen.png")
 
    # 2. Beliebteste Genres
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    genre_stats["anzahl"].head(10).sort_values().plot(kind="barh", ax=ax2)
    ax2.set_title("Top 10 Genres nach Anzahl Bewertungen")
    ax2.set_xlabel("Anzahl Bewertungen")
    fig2.tight_layout()
    fig2.savefig(BASIS / "diagramm_genres.png")
 
    # 3. Bewertungen über die Zeit
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    df.groupby("bewertungsjahr").size().plot(ax=ax3, marker="o")
    ax3.set_title("Anzahl Bewertungen pro Jahr")
    ax3.set_xlabel("Jahr")
    ax3.set_ylabel("Anzahl")
    fig3.tight_layout()
    fig3.savefig(BASIS / "diagramm_zeitverlauf.png")


def main():
    movies, ratings = lade_daten()
    daten_prufen(movies, ratings)
    movies, ratings = bereinigen(movies, ratings)
    df = zusammenfuhren(movies, ratings)
 
    print(f"\nAnzahl Filme: {movies.shape[0]}")
    print(f"Anzahl Bewertungen: {ratings.shape[0]}")
    print(f"Zusammengeführte Tabelle: {df.shape}")
 
    print("\nTop 10 Filme (mind. 20 Bewertungen):")
    print(top_filme(df).round(2))
 
    genre_stats = genre_statistik(df)
    print("\nBewertungen pro Genre:")
    print(genre_stats.round(2))
 
    diagramme_erstellen(df, genre_stats)
    print("\nDiagramme wurden als PNG im Skript-Ordner gespeichert.")
    plt.show()
    
if __name__ == "__main__":
    main()
