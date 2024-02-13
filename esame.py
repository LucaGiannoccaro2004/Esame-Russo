class CSVFile:

    def __init__(self, name):
        self.name = name
        self.can_read = True
        try:
            file = open(self.name, 'r')
            file.readline()
        except Exception as e:
            self.can_read = False
            print('Errore in apertura del file: "{}"'.format(e))


    def get_data(self):
        if not self.can_read:
            print('Errore, file non aperto o illeggibile')
            return None
        else:
            data = []
            my_file = open(self.name, 'r')
            for line in my_file:
                elements = line.split(',')
                elements[-1] = elements[-1].strip()
                if elements[0] != 'date':
                    data.append(elements)
            my_file.close()
            return data
        
class CSVTimeSeriesFile(CSVFile):
    pass

class ExamException(Exception):
    pass

def compute_increments(time_series, first_year, last_year):
    validate_parameters(time_series, first_year, last_year)
    means = compute_means(time_series, first_year, last_year)
    return compute_differces(means)

def compute_differces(means):
    differences = {}
    years = list(means.keys())
    for i in range(len(years) - 1):
        date_string = f"{years[i]}-{years[i+1]}"
        differences[date_string] = means[years[i+1]] - means[years[i]]
    return differences
        

def validate_parameters(time_series, first_year, last_year):
    if not isinstance(first_year, str):
        raise ExamException("Errore, 'first_year' deve essere una stringa")
    if not isinstance(last_year, str):
        raise ExamException("Errore, 'last_year' deve essere una stringa")
    # check if first_year and last_year are valid numbers
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
    if years_mean.get(int(first_year)) is None:
        raise ExamException("Errore, 'first_year' non presente nel dataset")
    if years_mean.get(int(last_year)) is None:
        raise ExamException("Errore, 'last_year' non presente nel dataset")
    return years_mean
csv = CSVTimeSeriesFile(name="data.csv")
data = csv.get_data()
print(data)
result = compute_increments(data, first_year="1949", last_year="1951")
[print(f"{key}: {value}") for key, value in result.items()]
