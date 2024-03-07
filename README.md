# MovieFinder- project proposal

MovieFinder is a python package which can be used to view and utilize the IMDB database. 

IMDB hold information regarding titles from various media such as movies, tv, short videos etc. The package focuses only on movie titles. 

In this repository you can find several files:
1. MovieFinder.py - The package, containing all relevant tools for viewing and analyzing the database. 
2. FindMovies.py - an example use of the FindMovies() function, the main tool of the package.
3. Result.csv - the expected output of using the FindMovies.py script
4. DataAnalysis.ipynb - a jupyter notebook with examples and use of the code, with basic analysis of movies.


## IMPORTANT!
Since the IMDB dataset is too heavy to be saved in this repository, when first using theh packge one must set downloadIMDB to 'True'.

# Detailed description of the package:
The general work flow of the package is as follows:
1. Download the data ( must for first time use)
2. Read the data zipped files
3. Pre-process of the data
4. Filtration of the data based on the user prefrences
5. Sorting the data based on the user prefrences
6. Printing the top hits (number selected by the user)
7. saving the list of movies as a csv file

## FindMovies function
All these actions are combined and utilized by the the main function of the package called "FindMovies".

The FindMovies function is designed to retrieve information about movies based on specified criteria. 

The function takes various parameters to filter and customize the search, providing flexibility for users to narrow down their results. 

Here's a summary of the key parameters:

downloadIMDB: Boolean flag to enable/disable downloading IMDb data for the movies (default is True).

1.  maxyear: Filters movies released before this specified year (default is current year)
2.  minyear: Filters movies released after this specified year (default is 1900)
3.  genres: Filters movies based on specified genres (optional).
4.  minVotes: Filters movies with a minimum number of votes (default is 0).
5.  minRating: Filters movies with a minimum IMDb rating (default is 0).
6.  maxRuntime: Filters movies with a runtime less than or equal to this value (default is 500 minutes).
7.  verbose: Boolean flag to enable/disable verbose mode for additional output (default is False).
8.  sortBy: Vector which specifies the sorting criteria for the results (default is by start year, number of votes, and average rating).
9.  sortAscending: Boolean vector which specifies whether the sorting would be in ascending or descending order (True for ascending, False for descending)
9.  director: Specifies the director name ID to filter movies (optional).
10. English: Boolean flag to filter only English-language movies (default is True).
11. TopX: Specifies the maximum number of top movies to retrieve (default is 10).
12. blockbuster: Boolean flag to filter only blockbuster movies (default is False).

Notes:
The directors name must be spelled correctly with capitalization. For example: 'Steven Spielberg'

The genres parameter accepts the following strings: 'Drama', 'Crime', 'Action', 'Adventure',
'Biography', 'History', 'Sci-Fi', 'Romance', 'Fantasy', 'Mystery', 'Thriller', 'War', 'Family',
'Animation', 'Western', 'Comedy', 'Music', 'Horror', 'Film-Noir', 'Musical', 'Sport', 'Documentary'

## Other functions:
download_file(outp)

download_file(name):
download the relevant files from IMDB and saves them gz compressed in the same folder. 

open_file(name):
Reads the compressed files. 

preprcosData(titles, ratings, crew):
combines the different datasets and performs basic preprocessing. 

filtertitles(titles, maxyear= None,minyear= float(1900),  maxRuntime= float(300),
            genre = None, minVotes = float(0), minRating= float(0),
             English = True, verbose = False):
#enables the filtraion of the dataset based on user prefrences. 

get_director_ID(csv_file, director):
searches for the director IMDB ID based on the name set by the user. 

filterDirector(titles, directorID):
filters the data to keep only titles of a specific director

printMovies(titles, TopX = 10):
prints a selected number of titles from the top of the list. 
