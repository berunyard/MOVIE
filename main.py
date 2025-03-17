import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kaggle.api.kaggle_api_extended import KaggleApi

#autenticação da api
api = KaggleApi()
api.authenticate()

#baixa o dataset e descompacta
dataset_name = "tmdb/tmdb-movie-metadata"
download_path = "datasets/"  # Caminho onde o dataset será salvo

api.dataset_download_files(dataset_name, path=download_path, unzip=True)

#print(f"Dataset baixado para: {download_path}")

df = pd.read_csv("C:/Users/Pichau/Desktop/DESKTOP/PROJETOS/MOVIE/datasets/tmdb_5000_movies.csv")
df.head()  # Ver as primeiras linhas

# verifica se há valores nulos
df.isnull().sum()
# remove as linhas com valores nulos
df = df.dropna()
# preenche valores nulos na coluna 'budget' com a média
df['budget'] = df['budget'].fillna(df['budget'].mean()) 
# verificando e removendo duplicados
df = df.drop_duplicates()  # remove linhas duplicadas
# converte para datetime
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')  


#VISUALIZAÇÃO DE DADOS!

#distribuição das avaliações (nota média)
plt.figure(figsize=(10,6))
sns.histplot(df['vote_average'], kde=True, bins=30, color='blue')
plt.title('Distribuição das Notas Médias dos Filmes')
plt.xlabel('Nota Média')
plt.ylabel('Frequência')
plt.show()

#top 10 filmes mais bem avaliados
top_rated = df.sort_values(by='vote_average', ascending=False).head(10)
plt.figure(figsize=(12,6))
sns.barplot(x='vote_average', y='title', data=top_rated, palette='viridis')
plt.title('Top 10 Filmes Mais Bem Avaliados')
plt.xlabel('Nota Média')
plt.ylabel('Filme')
plt.show()

#evolução das avaliações ao longo dos anos
df['release_year'] = df['release_date'].dt.year
avg_ratings_per_year = df.groupby('release_year')['vote_average'].mean()

plt.figure(figsize=(12,6))
sns.lineplot(x=avg_ratings_per_year.index, y=avg_ratings_per_year.values, color='green')
plt.title('Evolução das Avaliações de Filmes ao Longo dos Anos')
plt.xlabel('Ano')
plt.ylabel('Nota Média')
plt.show()

#distribuição dos gêneros de filmes
#convertendo os gêneros de uma lista para uma string e dividindo as palavras
df['genres'] = df['genres'].apply(lambda x: x.split('|') if isinstance(x, str) else [])
all_genres = [genre for sublist in df['genres'] for genre in sublist]

plt.figure(figsize=(12,6))
sns.countplot(y=all_genres, order=pd.Series(all_genres).value_counts().index, palette='Set2')
plt.title('Distribuição dos Gêneros de Filmes')
plt.xlabel('Frequência')
plt.ylabel('Gênero')
plt.show()

#relação entre orçamento e bilheteria
plt.figure(figsize=(10,6))
sns.scatterplot(x='budget', y='revenue', data=df, alpha=0.5)
plt.title('Relação entre Orçamento e Bilheteira dos Filmes')
plt.xlabel('Orçamento')
plt.ylabel('Bilheteira')
plt.show()
