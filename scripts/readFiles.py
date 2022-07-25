import csv
import json
import os
import ast

FILENAMES = ['movies_metadata', 'credits', 'keywords', 'links']
FILENAME_IGNORING_FOR_NOW = ['ratings']

def getColumnMapFromRow(row, columns):
    movieMap = {}
    for column in columns:
        movieMap[column] = row[columns.index(column)]
    return movieMap

#  ===================================================================
#  GETTING AND PROCESSING CREDITS
# ===================================================================
def getCredits(row, columns):
    creditMap = getColumnMapFromRow(row, columns)
    movieId = row[columns.index('id')]
    return {movieId: creditMap}

def processCredits(mappedRows):
    processedRows = []
    for mappedRow in mappedRows:
        outerDict = {}
        innerDict = {}
        outerDictKey = list(mappedRow.keys())[0]
        crew = mappedRow[outerDictKey]['crew']
        for crewMember in crew.split("},"):
            if "'Director'" in crewMember:
                name = crewMember.split("'name': ")[1].split(", '")[0]
                innerDict['director'] = name.strip("''")
        outerDict[outerDictKey] = innerDict
        processedRows.append(outerDict)
    return processedRows
# ===================================================================

# ===================================================================
# GETTING AND PROCESSING KEYWORDS
# ===================================================================
def getKeywords(row, columns):
    keywordMap = getColumnMapFromRow(row, columns)
    movieId = row[columns.index('id')]
    return {movieId: keywordMap}

def processKeywords(mappedRows):
    processedRows = []
    for mappedRow in mappedRows:
        outerDict = {}
        innerDict = {}
        outerDictKey = list(mappedRow.keys())[0]
        keywords = ast.literal_eval(mappedRow[outerDictKey]['keywords'])
        listOfKeywords = []
        for keyword in keywords:
            listOfKeywords.append(keyword['name'])
        innerDict['keywords'] = listOfKeywords
        outerDict[outerDictKey] = innerDict
        processedRows.append(outerDict)
    return processedRows
# ===================================================================

# ===================================================================
# GETTING AND PROCESSING MOVIE METADATA
# ===================================================================
def getMoviesMetaData(row, columns):
    movieMap = getColumnMapFromRow(row, columns)
    movieId = row[columns.index('id')]
    return {movieId: movieMap}

def getCSVToDBNameForMovies(CSVName):
    nameMap = {'id': 'movieId', \
        'vote_average': 'rating', \
        'title': 'title', \
        'release_date': 'year', # process this \ 
        'revenue': 'revenue', \
        'runtime': 'runtime', \
        'tagline': 'tagline', \
        'language': 'language', \
        'poster_path': 'posterPath', \
        'overview': 'overview', \
        'vote_count': 'voteCount', \
        'genres': 'genre', \
        'original_language': 'language'}
    if CSVName not in nameMap.keys():
        return None
    return nameMap[CSVName]

def processMoviesMetaData(mappedRows):
    processedRows = []
    for mappedRow in mappedRows:
        outerDict = {}
        innerDict = {}
        outerDictKey = list(mappedRow.keys())[0]
        for key in mappedRow[outerDictKey].keys():
            innerDictKey = getCSVToDBNameForMovies(key)
            if innerDictKey is None:
                continue
            genres = []
            if key == 'genres':
                try:
                    genreData = ast.literal_eval(mappedRow[outerDictKey][key])
                    for genre in genreData:
                        genres.append(genre['name'])
                    mappedRow[outerDictKey][key] = genres
                except:
                    print("PRINT PRINT: ", mappedRow[outerDictKey][key])
            innerDict[innerDictKey] = mappedRow[outerDictKey][key]
        outerDict[outerDictKey] = innerDict
        processedRows.append(outerDict)
    return processedRows
# ===================================================================

# ===================================================================
# GETTING AND PROCESSING LINKS
# ===================================================================
def getLinks(row, columns):
    linkMap = getColumnMapFromRow(row, columns)
    movieId = row[columns.index('tmdbId')]
    return {movieId: linkMap}

def processLinks(mappedRows):
    processedRows = []
    for mappedRow in mappedRows:
        outerDict = {}
        innerDict = {}
        outerDictKey = list(mappedRow.keys())[0]
        imdbId = mappedRow[outerDictKey]['imdbId']
        imdbLink = "https://www.imdb.com/title/tt" + imdbId + "/"
        innerDict['imdbLink'] = imdbLink
        outerDict[outerDictKey] = innerDict
        processedRows.append(outerDict)
    return processedRows
# ===================================================================


# ===================================================================
# GETTING AND PROCESSING RATINGS
# ===================================================================
def getRatings(row, columns):
    ratingMap = getColumnMapFromRow(row, columns)
    movieId = row[columns.index('movieId')]
    return {movieId: ratingMap}

def processRatings(mappedRows):
    processedRows = []
    for mappedRow in mappedRows:
        outerDict = {}
        innerDict = {}
        outerDictKey = list(mappedRow.keys())[0]
        innerDict['userRatingId'] = mappedRow[outerDictKey]['userId']
        innerDict['rating'] = mappedRow[outerDictKey]['rating']
        innerDict['movieId'] = mappedRow[outerDictKey]['movieId']
        innerDict['timestamp'] = mappedRow[outerDictKey]['timestamp']
        outerDictKey = outerDictKey + "-" + innerDict['userRatingId']
        outerDict[outerDictKey] = innerDict
        processedRows.append(outerDict)
    return processedRows
# ===================================================================


# ===================================================================
# DEFINING FACTORIES
# ===================================================================
def getGetterFunction(fileName):
    getterFactory = {'credits': getCredits,\
                        'keywords': getKeywords,\
                            'links': getLinks,\
                              'movies_metadata': getMoviesMetaData,\
                                 'ratings':getRatings}
    return getterFactory[fileName]

def getProcessFunction(fileName):
    processFactory = {'credits': processCredits,\
                        'keywords': processKeywords,\
                            'links': processLinks,\
                              'movies_metadata': processMoviesMetaData,\
                                 'ratings':processRatings}
    return processFactory[fileName]
# ===================================================================

def linkData(processedData):
    newProcessedData = []
    creditsData = {}
    for entry in processedData['credits']:
        key = list(entry.keys())[0]
        creditsData[key] = entry[key]
    keywordsData = {}
    for entry in processedData['keywords']:
        key = list(entry.keys())[0]
        keywordsData[key] = entry[key]
    linksData = {}
    for entry in processedData['links']:
        key = list(entry.keys())[0]
        linksData[key] = entry[key]
    for row in processedData['movies_metadata']:
        movieId = list(row.keys())[0]
        try:
            row[movieId]['director'] = creditsData[movieId]['director']
        except:
            row[movieId]['director'] = ""
        try:
            row[movieId]['keywords'] = keywordsData[movieId]['keywords']
        except:
            row[movieId]['keywords'] = []
        row[movieId]['imdbLink'] = linksData[movieId]['imdbLink']
        newProcessedData.append({movieId: row[movieId]})
    return newProcessedData

if __name__ == "__main__":
    processedData = {}
    for file in FILENAMES:
        with open(os.path.join(os.getcwd(), file + ".csv"), 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=",")
            columns = []
            getterFunction = getGetterFunction(file)
            processorFunction = getProcessFunction(file)
            isColumnNamesRow = True
            mappedRows = []
            for row in csv_reader:
                if isColumnNamesRow:
                    isColumnNamesRow = False
                    columns = row
                    continue
                try:
                    mappedRow = getterFunction(row, columns)
                except:
                    print("Issue with file: %s" % file)
                    print("Issue with row: ", row)
                    
                mappedRows.append(mappedRow)
            processedRows = processorFunction(mappedRows)
            processedData[file] = processedRows
    linkedData = linkData(processedData)
    with open('linkedData', 'w', encoding='utf-8') as fout:
        json.dump(linkedData, fout)