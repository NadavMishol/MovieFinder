# MovieFinder- project proposal

I will write a program script that does the following:
1.	Download the most recent version of movies dataset from IMDB in this address:https://developer.imdb.com/non-commercial-datasets/
2.	Filter the movies based on a set amount of parameters.
3.	Print a list of relevant movies which answer the conditions set by the user

Steps the program should follow:
1.	Accept optional user-set conditions like: date, genre, participating actors, director, minimum rotten-tomatoes rate
2.	Download the most recent version of the data
3.	Unzip it
4.	Filter the data according to the user preferences
5.	Sort it according to the the user preferences
6.	Generate a response of top X matches 
7.	The response will include the title of the movie, it’s rate a link to the IMDB page. 


Pseudo-code:
1. def MovieFinder(type = 'movie',
                    averageRating  = 7.5,
                    MinNumVotes  = 1000,
                    releaseMin = 2014,
                    releasMax = 2024,
                    MinRuntime = 90,
                    actor = any,
                    isAdult = 0,
                    original = 0,
                    genres = 'all',
                    orderBy = 'rating')

2.  Download title.basics.tsv.gz
3.  def filter type
4.  def filter averageRating
5.  def filter releaseMax
6.  def filter actor
7.  def filter isAdult
8.  def filter original
9.  def filter genres
10. def filter minRuntime


3.  for parameter in parameters:
        if filter: 
            filter

4. if orderBy:
    sort()

5. def print_title:
    based on title ID
6. for title 1:10:
    print(title)
