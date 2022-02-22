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
        except:
            raise ExamException('The file does not exist or cannot be read!')
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
                    elements[1] = int(elements[1])
                except:
                    raise ExamException('Error converting value "{}" to numeric positive integer'.format(elements[1]))
                    pass
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
def detect_similar_monthly_variations(data, years):
    # Testing for input years
    if type(years) != list:
        raise ExamException('Invalid type for years, only list supported. Got "{}""'.format(type(years)))
    if len(years) != 2:
        raise ExamException('Got less or more than two years, only two years supported.')
    if not isinstance(years[0], int):
        raise ExamException('Invalid type for the first year, only integer accepted. Got "{}""'.format(type(years[0])))
    if not isinstance(years[1], int):
        raise ExamException('Invalid type for the second year, only integer accepted. Got "{}""'.format(type(years[1])))
    if years[0] <= 0:
        raise ExamException('Invalid year. Got "{}""'.format(years[0]))
    if years[1] <= 0:
        raise ExamException('Invalid year. Got "{}""'.format(years[1]))
    if (years[1] - years[0]) != 1:
        raise ExamException('Invalid years, only consecutive years accepted. Got "{}" and "{}"'.format(years[0], years[1]))
    if years[0] > years[1]:
        raise ExamException('The first year "{}" is greater than the second year "{}"'.format(years[0], years[1]))

    # Creation of two lists, one per year
    first_year_monthly_variations = []
    second_year_monthly_variations = []
    # Creation of two boolean variables to check the existence of the input years in the data: assuming years are not in the data, then the boolean variables are false
    first_year_in_data = False
    second_year_in_data = False
    # Loop for each year
    for i, year in enumerate(years):
        # Loop for each couple in data
        for couple in data:
            # If that year is in the couple, add element to the years list
            if str(year) == couple[0][0:4]:
                # If it is processing the first year, add element to the first year list
                if i == 0:
                    first_year_monthly_variations.append(couple[1])
                    # Since the first year was found, the boolean variable is true
                    first_year_in_data = True
                # If it is processing the second year, add element to the second year list
                else:
                    second_year_monthly_variations.append(couple[1])
                    # Since the second year was found, the boolean variable is true
                    second_year_in_data = True
        # If it is processing the first year, check the first boolean variable value
        if i == 0:
            # If the first boolean variable is not true, the first year is not in data
            if first_year_in_data != True:
                raise ExamException('The first year value "{}" is not in the list!'.format(year))
        # If it is processing the second year, check the second boolean variable value
        else:
            # If the second boolean variable is not true, the second year is not in data
            if second_year_in_data != True:
                raise ExamException('The second year value "{}" is not in the list!'.format(year))
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
time_series_file = CSVTimeSeriesFile(name = 'data.csv')

time_series = time_series_file.get_data()

print('Dati contenuti nel file: "{}"'.format(time_series))

result = detect_similar_monthly_variations(time_series, [1949, 1950])

print('Dati contenuti nel file: "{}"'.format(result))