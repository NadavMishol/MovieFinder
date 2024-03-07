import gzip
import shutil
import requests
import pandas as pd
import csv
from io import StringIO
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os



def download_file(name):
    url = 'https://datasets.imdbws.com/'+name+'.tsv.gz'
    response = requests.get(url)

    if response.status_code == 200:
        with open(name+'.tsv.gz', 'wb') as f:
            f.write(response.content)
    else:
        print('Request failed with status code:', response.status_code)

def open_file(name,cols_to_read = None):
    file = name+'.tsv.gz'
    with gzip.open(file, 'rt', encoding='utf-8') as gz_file:
        df = pd.read_csv(gz_file, delimiter='\t', na_values='\\N', usecols = cols_to_read)    

    return df

def preprcosData(titles, ratings, crew):
    titles = titles[titles['titleType'] == 'movie'] #remove all non-movie titles
    titles = titles.merge(ratings, on='tconst', how='inner')
    titles = titles.merge(crew, on='tconst', how='inner')
    titles['runtimeMinutes'] = pd.to_numeric(titles['runtimeMinutes'], errors='coerce')
    titles = titles.dropna()

    # Convert data types
    titles['startYear'] = titles['startYear'].astype(int)
    titles['averageRating'] = titles['averageRating'].astype(float)
    titles['numVotes'] = titles['numVotes'].astype(int)


    del ratings
    del crew
    
    # Filter the data by removing NAs and unwanted values
    titles = titles.dropna(subset=['startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'directors'])

    return titles

def filtertitles(titles,
                    maxyear= None,
                    minyear= float(1900),
                    maxRuntime= float(300),
                    genre = None,
                    minVotes = float(0),
                    minRating= float(0),
                    English = True,
                    verbose = False):

    #Filter max year
    if maxyear == None:
        titles = titles[titles['startYear'] <= datetime.now().year]
        if verbose:
            print('max year: this year')
    else:
        titles = titles[titles['startYear'] <= maxyear]
        if verbose:
            print('max year:', maxyear)
    if verbose:
        print('# titles:', len(titles))

    #Filter min year
    titles = titles[titles['startYear'] >= minyear]
    if verbose:
        print('min year:', minyear)
        print('# titles:', len(titles))

    #Filter max runtime    
    titles = titles[titles['runtimeMinutes'] <= maxRuntime]
    if verbose:
        print('max runtime:', maxRuntime)
        print('# titles:', len(titles))

    #Filter number of votes
    titles = titles[titles['numVotes'] >= minVotes]
    if verbose:
        print('min votes:', minVotes)
        print('# titles:', len(titles))

    #filter rating
    titles = titles[titles['averageRating'] >= minRating]
    if verbose:
        print('minimum rating:', minRating)
        print('# titles:', len(titles))

    #filter language
    if English:
        titles = titles[titles['primaryTitle'] == titles['originalTitle']]
        if verbose:
            print('only English movies')
            print('# titles:', len(titles))


    #filter by genre
    if genre is not None:
        titles = titles[titles['genres'].str.contains(genre)]
        if verbose:
            print('genre:', genre)
            print('# titles:', len(titles))


    return titles

def get_director_ID(csv_file, director):
    # Read the file in chunks
    chunk_size = 10000
    for chunk in pd.read_csv(csv_file, chunksize=chunk_size, delimiter='\t', usecols=['nconst', 'primaryName'], na_values='\\N'):
        # Search within the chunk
        subset = chunk[chunk['primaryName'] == director]
        if not subset.empty:
            # Return the 'nconst' value from the first matching row found
            return subset['nconst'].iloc[0]

    # Return None if no match is found
    print('ERROR: director'+director+' not found')
    return None

def filterDirector(titles, directorID):
    
    if directorID is not None:
        titles = titles[titles['directors'].str.contains(directorID)]
        print('director:', directorID)
    else:
        print('ERROR: director not found')
        titles = None

    return titles

def printMovies(titles, TopX = 10):
    results = titles.head(TopX)
    print('Best movies:')
    num = 1
    for row in results.iterrows():
        print('======================'+str(num)+'=======================')
        print(row[1]['primaryTitle'],
              '\nYear', row[1]['startYear'],
              '\nRating',row[1]['averageRating'],
             '\nVotes',row[1]['numVotes'],
             '\ngenres', row[1]['genres'])
        num += 1
    return

def FindMovies(
               director = None,
               maxyear= None,
                minyear= float(1900),
                maxRuntime= float(500),
                genres = None,
                minVotes = float(0),
                minRating= float(0),
                English = True,
                sortBy = ['averageRating','numVotes','startYear'],
                sortAscending = [False, False, True], 
                TopX = 10,
                downloadIMDB = True,
                verbose = False,
                blockbuster = False):
    

    #Download the data from IMDB
    if downloadIMDB:
        for file in ['title.basics', 'title.ratings', 'title.crew', 'name.basics']:
            print('Downloading', file, 'from IMDB...')
            download_file(file)
    else:
        print('Using locally available data')
        if not os.path.exists('title.basics.tsv.gz') or not os.path.exists('title.ratings.tsv.gz') or not os.path.exists('name.basics.tsv.gz'):
            print('ERROR: Locally available data not found. Please set downloadIMDB to True or download the data manually from https://www.imdb.com/interfaces/ and place the files in the current directory.')
            return

    # Loading the data
    print('Loading titles...')
    titles = open_file('title.basics',cols_to_read = ['tconst','titleType','primaryTitle','originalTitle','startYear','runtimeMinutes','genres'])
    print('Loading ratings...')
    ratings = open_file('title.ratings',cols_to_read = ['tconst','averageRating','numVotes'])
    print('Loading crew...')
    crew = open_file('title.crew',cols_to_read = ['tconst','directors'])

    # Preprocessing the data
    titles = preprcosData(titles, ratings, crew)

    #Filter the data
    if blockbuster:
        minVotes = 1000000
        English = True
    titles = filtertitles(titles, maxyear, minyear, maxRuntime, genres, minVotes, minRating, English,verbose = verbose)

    #Filter the director
    if director is not None:
        directorID = get_director_ID('name.basics.tsv.gz', director)
        titles = filterDirector(titles, directorID)

    #Sort the data
    titles = titles.sort_values(by=sortBy, ascending = sortAscending)

    #save resuls as csv
    titles.to_csv('Movies.csv', index=False)


    #return the top X movies
    results = titles.head(TopX)

    #print results
    printMovies(titles, TopX = TopX)


    return results
         