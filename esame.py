# ==============================
#             CLASSES
# ==============================
#       ExamException Class
# ==============================
class ExamException(Exception):
    pass

# ==============================
#    CSVTimeSeriesFile Class
# ==============================
class CSVTimeSeriesFile():

    def __init__(self, name):
        # Creation of the "name" attribute
        self.name = name

    def get_data(self):
        # Creation of two lists: a list and a list of list
        list = []
        listoflist = []
        # File opening
        try:
            file = open(self.name, 'r')
        except ExamException:
            print ('The file does not exist!')
            return None
        # File reading, line by line
        for line in file:
            # Creation of elements with lines splitted on ","
            elements = line.split(',')
            # Deleting undesired characters (newline e spaces)
            elements[-1] = elements[-1].strip()
            # If header is not processed, add elements to the list
            if elements[0] != 'date':
                # Conversion of the second column from string type to numerical type
                elements[1] = float(elements[1])
                list.append(elements)
        # File closing
        file.close()
        # Adding elements of the list to the list of list
        listoflist.extend(list)
        return listoflist

# ==============================
#            METHODS
# ==============================
#          DSMV method
# ==============================
def detect_similar_monthly_variations(list, years):
    first_year_monthly_variations = []
    second_year_monthly_variations = []
    for i, year in enumerate(years):
        for couple in list:
            if str(year) in couple[0]:
                if i == 0:
                    first_year_monthly_variations.append(couple[1])
                else:
                    second_year_monthly_variations.append(couple[1])

    for number in range(len(first_year_monthly_variations) - 1):
        first_year_monthly_variations[number] = abs(first_year_monthly_variations[number] - first_year_monthly_variations[number + 1])
    first_year_monthly_variations = first_year_monthly_variations[0 : - 1]

    for number in range(len(second_year_monthly_variations) - 1):
        second_year_monthly_variations[number] = abs(second_year_monthly_variations[number] - second_year_monthly_variations[number + 1])
    second_year_monthly_variations = second_year_monthly_variations[0 : - 1]

    similar_monthly_variations = []
    for value in range(len(first_year_monthly_variations)):
        if abs(first_year_monthly_variations[value] - second_year_monthly_variations[value]) <= 2:
            similar_monthly_variations.append(True)
        else:
            similar_monthly_variations.append(False)
    
    return similar_monthly_variations

# ==============================
#            PROGRAM
# ==============================
#          Main Program
# ==============================
time_series_file = CSVTimeSeriesFile(name = 'data.csv')

time_series = time_series_file.get_data()

print('Dati contenuti nel file: "{}"'.format(time_series))

result = detect_similar_monthly_variations(time_series, [1949, 1950])

print('Dati contenuti nel file: "{}"'.format(result))