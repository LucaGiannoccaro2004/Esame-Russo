import re 

class CSVFile:

    def __init__(self, name):
        self.name = name
        self.can_read = True
        try:
            file = open(self.name, 'r')
            file.readline()
        except Exception as e:
            self.can_read = False
  
class CSVTimeSeriesFile(CSVFile):
     
     def get_data(self):
        if not self.can_read:
            raise ExamException("Errore, file inesistente o non leggibile")
        data = []
        year = None
        month = None
        my_file = open(self.name, 'r')
        for line in my_file:
            elements = line.split(',')
            elements[-1] = elements[-1].strip()
            if elements[0] != 'date' :
                if re.match(r'^\d{4}-\d{2}$', elements[0]) and elements[1].isdigit():
                    if year is not None:
                        if int(elements[0].split('-')[0]) < year:
                            raise ExamException("Errore, timestamp non ordinato")
                        elif int(elements[0].split('-')[0]) == year:
                            if int(elements[0].split('-')[1]) < month:
                                raise ExamException("Errore, timestamp non ordinato")
                    year = int(elements[0].split('-')[0])
                    month = int(elements[0].split('-')[1])
                    data.append(elements)
        my_file.close()
        if has_duplicates(data):
            raise ExamException("Errore, timestamp duplicati")
        return data
        
def has_duplicates(list_of_lists):
    seen = set()
    for sublist in list_of_lists:
        sublist_tuple = tuple(sublist)
        if sublist_tuple in seen:
            return True
        seen.add(sublist_tuple)
    return False

class ExamException(Exception):
    pass

def compute_increments(time_series, first_year, last_year):
    validate_parameters(first_year, last_year)
    means = compute_means(time_series, first_year, last_year)
    return compute_differces(means)

def compute_differces(means):
    differences = {}
    years = list(means.keys())
    for i in range(len(years) - 1):
        date_string = f"{years[i]}-{years[i+1]}"
        differences[date_string] = means[years[i+1]] - means[years[i]]
    return differences
        
def validate_parameters(first_year, last_year):
    if not isinstance(first_year, str):
        raise ExamException("Errore, 'first_year' deve essere una stringa")
    if not isinstance(last_year, str):
        raise ExamException("Errore, 'last_year' deve essere una stringa")
    try:
        int(first_year)
    except:
        raise ExamException("Errore, 'first_year' deve essere una stringa contenente un numero")
    try:
        int(last_year)
    except:
        raise ExamException("Errore, 'last_year' deve essere una stringa contenente un numero")
    if int(first_year) > int(last_year):
        raise ExamException("Errore, 'first_year' deve essere minore di 'last_year'")

def compute_means(time_series, first_year, last_year):
    years_mean = {}
    year_cursor = int(first_year)
    existing_months = 0
    for line in time_series:
        date = line[0].split("-")
        if int(date[0]) <= int(last_year):
            if int(date[0]) > year_cursor:
                year_cursor = int(date[0])
                existing_months = 0
            if int(date[0]) == year_cursor:
                existing_months +=1
                if years_mean.get(year_cursor) is None:
                    years_mean[year_cursor] = 0
                years_mean[year_cursor] = (years_mean[year_cursor] * (existing_months - 1) + int(line[1]))/existing_months
    if int(last_year) == int(first_year) + 1 and not (years_mean.get(int(first_year)) is None and years_mean.get(int(last_year)) is None):
        years_mean = {}
    else:
        if years_mean.get(int(first_year)) is None:
            raise ExamException("Errore, 'first_year' non presente nel dataset")
        if years_mean.get(int(last_year)) is None:
            raise ExamException("Errore, 'last_year' non presente nel dataset")
    return years_mean

