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
            print('The file does not exist!')
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
                try:
                    elements[1] = float(elements[1])
                except ExamException as e:
                    print('Errore in conversione del valore "{}" a numerico: "{}"'.format(elements[1], e))
                    break
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
    # Creation of two lists, one per year
    first_year_monthly_variations = []
    second_year_monthly_variations = []
    # Loop for each year
    for i, year in enumerate(years):
        # Loop for each couple in input list
        for couple in list:
            # If that year is in the couple, add element to the years list
            if str(year) in couple[0]:
                # If it is processing the first year, add element to the first year list
                if i == 0:
                    first_year_monthly_variations.append(couple[1])
                # If it is processing the second year, add element to the second year list
                else:
                    second_year_monthly_variations.append(couple[1])
    # Calculation of the difference of values ​​for each ordered pair of months of the first year, replacing the elements in the first year list and deleting the last value of 12th month
    for number in range(len(first_year_monthly_variations) - 1):
        first_year_monthly_variations[number] = abs(first_year_monthly_variations[number] - first_year_monthly_variations[number + 1])
    first_year_monthly_variations = first_year_monthly_variations[0 : - 1]
    # Calculation of the difference of values ​​for each ordered pair of months of the second year, replacing the elements in the second year list and deleting the last value of 12th month
    for number in range(len(second_year_monthly_variations) - 1):
        second_year_monthly_variations[number] = abs(second_year_monthly_variations[number] - second_year_monthly_variations[number + 1])
    second_year_monthly_variations = second_year_monthly_variations[0 : - 1]
    # Creation of a list
    similar_monthly_variations = []
    # Loop for each value in the first year list
    for value in range(len(first_year_monthly_variations)):
        # If the difference of the differences of the values for each ordered pair of months of the two respective years is ±2, add true to the list
        if abs(first_year_monthly_variations[value] - second_year_monthly_variations[value]) <= 2:
            similar_monthly_variations.append(True)
        # If the difference of the differences of the values for each ordered pair of months of the two respective years is not ±2, add false to the list
        else:
            similar_monthly_variations.append(False)
    return similar_monthly_variations

# ==============================
#            PROGRAM
# ==============================
#          Main Program
# ==============================
time_series_file = CSVTimeSeriesFile(name = 'dta.csv')

time_series = time_series_file.get_data()

print('Dati contenuti nel file: "{}"'.format(time_series))

result = detect_similar_monthly_variations(time_series, [1949, 1950])

print('Dati contenuti nel file: "{}"'.format(result))