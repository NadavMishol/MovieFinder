import MovieFinder as mf

mf.FindMovies(downloadIMDB=False,verbose=False,maxyear=2020, genres = 'Sci-Fi',TopX=10, minVotes = 100000, minRating= 8.0, English = True)