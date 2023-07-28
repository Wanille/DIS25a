import csv
import re

# example: 
# {'': '9', 
#  'Title': '10. Fight Club (1999)', 
#  'Certificate': 'R', 
#  'Duration': '139 min', 
#  'Genre': 'Crime, Drama', 
#  'Rate': '8.8', 
#  'Metascore': '66', 
#  'Description': 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.', 
#  'Cast': 'Director: David Fincher | Stars: Brad Pitt, Edward Norton, Meat Loaf, Zach Grenier', 
#  'Info': 'Votes: 1,820,268 | Gross: $37.03M'
#  }


def parse_cast(cast_str):
    # Director: Director Name | Cast: Actor 1, Actor 2, Actor 3
    cast = cast_str.split('|')
    cast_dict = {"Director": [], "Stars": []}
    for c in cast:
        role = c.split(':')
        cast_dict[role[0].strip().rstrip()] = [r.strip().rstrip() for r in role[1].strip().split(',')]
    return cast_dict

def parse_genres(genre_str):
    return [g.strip() for g in genre_str.split(',')]

def parse_runtime(runtime_str):
    return int(runtime_str.split(' ')[0])

def parse_rate(rate_str):
    return float(rate_str)

def parse_metascore(metascore_str):
    try:
        return int(metascore_str)
    except:
        return None

def parse_info(info_str):
    info = info_str.split('|')
    info_dict = {}
    for i in info:
        role = i.split(':')
        info_dict[role[0].strip()] = role[1].strip()
    return info_dict

def parse_year(title):
    try:
        return int(title.split('(')[1].split(')')[0])
    except:
        return None

def parse_title(title):
    return ' '.join(title.split(' ')[1:-1])


def parse_row(row):
    row['rank'] = int(row[''])
    del row[''] 
    row['Cast'] = parse_cast(row['Cast'])
    row['Genre'] = parse_genres(row['Genre'])
    row['Duration'] = parse_runtime(row['Duration'])
    row['Rate'] = parse_rate(row['Rate'])
    row['Metascore'] = parse_metascore(row['Metascore'])
    row['Info'] = parse_info(row['Info'])
    row['Year'] = parse_year(row['Title'])
    row['Title'] = parse_title(row['Title'])
    row["lower"] = {
        "Title": row["Title"].lower(),
        "Cast": {
            "Director": [d.lower() for d in row['Cast']['Director']],
            "Stars": [c.lower() for c in row['Cast']['Stars']]
        },
        "Genre": [g.lower() for g in row['Genre']],
        "Description": row['Description'].lower()
    }
    return row

def get_recommendation(director=None, actor=None, runtime=None, genre=None, year=None, rate=None):
    with open('imdb.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        recommendations = []
        for row in reader:
            movie = parse_row(row)
            if director and director not in movie['lower']['Cast']['Director']:
                continue
            if actor and actor not in movie['lower']['Cast']['Stars']:
                continue
            if runtime and runtime <= movie['Duration']:
                continue
            if genre and genre not in movie['lower']['Genre']:
                continue
            if year and year != movie['Year']:
                continue
            if rate and rate > movie['Rate']:
                continue

            del movie['lower']
            recommendations.append(movie)
        return recommendations

def recommend_by_str(text):
    #text examples
    # Recommend me a horror movie from 2010 with a runtime of 120 minutes
    # Recommend me a movie from 2010 with a runtime of 120 minutes
    # Recommend me a movie from 2010
    # Recommend me a movie with a runtime of 120 minutes
    # Recommend me a movie

    text = text.lower()
    director = None
    if (m := re.match(r'.*director: ([\w\s]+),?', text)):
        director = m.group(1)
    actor = None
    if (m := re.match(r'.*actor: ([\w+\s]+),?', text)):
        actor = m.group(1)
    runtime = None
    if (m := re.match(r'.*runtime: (\d+),?', text)):
        try:
            runtime = int(m.group(1))
        except:
            pass
    genre = None
    if (m := re.match(r'.*genre: (\w+),?', text)):
        genre = m.group(1)
    year = None
    if (m := re.match(r'.*year: (\d+),?', text)):
        try:
            year = int(m.group(1))
        except:
            pass

    rate = None
    if (m := re.match(r'.*rating: (\d+),?', text)):
        try:
            rate = float(m.group(1))
        except:
            pass

    # print(director, actor, runtime, genre, year, rate)

    return get_recommendation(director=director, actor=actor, runtime=runtime, genre=genre, year=year, rate=rate)