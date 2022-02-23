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
        # Checking the type of data name
        if type(name) != str:
            raise ExamException('Invalid type for name, only string supported. Got "{}".'.format(type(name)))

    def get_data(self):
        # Creation of a list of list to save data values
        listoflist = []
        # Creation of a date list and two variables, which will be used later to check the recurrence of dates in data file
        date_list = []
        previous_year = 0
        previous_month = 1
        # File opening ('Existance', 'Reading' and 'Emptiness' cases)
        try:
            file = open(self.name, 'r')
        except:
            raise ExamException('The file does not exist!')
        myfile = open(self.name, 'r')
        try:
            content = myfile.read()  
        except:
            raise ExamException('The file cannot be read!')
        if content == '':
            raise ExamException('Empty file!')
        # File reading, line by line
        for line in file:
            # Creation of a list for each line of data file
            list = []
            # Testing the line ('Empty line' case)
            if line == '\n':
                pass
            else:
                # Testing the line ('Cannot distinguish date from passengers' case)
                if ',' not in line:
                    pass
                else:
                    # Creation of elements with line splitted on ","
                    elements = line.split(',')
                    # Testing the line ('Cannot distinguish month from year' case)
                    if '-' not in elements[0]:
                        pass
                    else:
                        # Testing the recurrence of dates in data file by using the previous date list
                        if elements[0] in date_list:
                            raise ExamException('Got a duplicate timestamp for "{}".'.format(elements[0]))
                        # Creation of a list with date line splitted on "-"
                        date = elements[0].split('-')
                        # Creation of a variable, which tracks the date conversion error: it is 0 when there is no error, 1 when there is error
                        date_conversion_error = 0
                        # Testing the convertibility of the date ('Cannot convert the date into a numeric date' case)
                        try:
                            year = int(date[0])
                            month = int(date[1])
                        except:
                            date_conversion_error = 1
                        if date_conversion_error == 1:
                            pass
                        else:
                            # Testing the month and the year ('Validity' and 'Order' cases) by using the previous variables
                            if month not in range(1, 13):
                                pass
                            else:
                                if previous_year > year:
                                    raise ExamException('Years are not in ascending order.')
                                elif previous_year == year:
                                    if previous_month > month:
                                        raise ExamException('Months are not in ascending order.')
                                    previous_month = month
                                else:
                                    previous_month = month
                                previous_year = year
                                # Creation of a variable, which tracks the number of passengers conversion error: it is 0 when there is no error, 1 when there is error
                                number_of_passengers_conversion_error = 0
                                # Testing the convertibility of the number of passengers ('Cannot convert the number of passengers into a numeric value' case)
                                try:
                                    passengers = int(elements[1])
                                except:
                                    number_of_passengers_conversion_error = 1
                                if number_of_passengers_conversion_error == 1:
                                    pass
                                else:
                                    # Testing the passengers ('Validity' case)
                                    if passengers <= 0:
                                        pass
                                    else:
                                        # Creation of definitive variables to save the date and the number of passengers
                                        valid_date = elements[0]
                                        valid_passengers = passengers
                                        # Adding date to the date list, in order to repeat the check for the next date
                                        date_list.append(valid_date)
                                        # Adding values to the previous list
                                        list.append(valid_date)
                                        list.append(valid_passengers)
                                        # Adding values of the list to the list of list
                                        listoflist.append(list)
        # File closing
        file.close()
        return listoflist

# ==============================
#            METHODS
# ==============================
#          DSMV method
# ==============================
def detect_similar_monthly_variations(data, years):
    # Testing the input years
    if type(years) != list:
        raise ExamException('Invalid type for years, only list supported. Got "{}"'.format(type(years)))
    if len(years) != 2:
        raise ExamException('Got less or more than two years, only two years supported.')
    if not isinstance(years[0], int):
        raise ExamException('Invalid type for the first year, only integer accepted. Got "{}"'.format(type(years[0])))
    if not isinstance(years[1], int):
        raise ExamException('Invalid type for the second year, only integer accepted. Got "{}"'.format(type(years[1])))
    if years[0] <= 0:
        raise ExamException('Invalid year. Got "{}"'.format(years[0]))
    if years[1] <= 0:
        raise ExamException('Invalid year. Got "{}"'.format(years[1]))
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
    # Creation of two variables, which will be used later to order data by months
    first_year_previous_month_couple = 0
    second_year_previous_month_couple = 0
    # Loop for each year
    for i, year in enumerate(years):
        # Loop for each couple in data
        for couple in data:
            # If that year is in the couple, add element to the years list
            if str(year) == couple[0][0 : 4]:
                # If it is processing the first year, add element to the first year list
                if i == 0:
                    # If two months are not consecutives, add 'False' to the first year list
                    if abs(first_year_previous_month_couple - int(couple[0][5 : 7])) != 1:
                        for g in range(abs(first_year_previous_month_couple - int(couple[0][5 : 7]))):
                            first_year_monthly_variations.append(False)
                    # If two months are consecutives, add element to the first year list
                    else:
                        first_year_monthly_variations.append(couple[1])
                    # Since the first year was found, the boolean variable is true
                    first_year_in_data = True
                    # Update the previous month value
                    first_year_previous_month_couple = int(couple[0][5 : 7])
                # If it is processing the second year, add element to the second year list
                else:
                    # If two months are not consecutives, add 'False' to the second year list
                    if abs(second_year_previous_month_couple - int(couple[0][5 : 7])) != 1:
                        for g in range(abs(second_year_previous_month_couple - int(couple[0][5 : 7]))):
                            second_year_monthly_variations.append(False)
                    # If two months are consecutives, add element to the second year list
                    else:
                        second_year_monthly_variations.append(couple[1])
                    # Since the second year was found, the boolean variable is true
                    second_year_in_data = True
                    # Update the previous month value
                    second_year_previous_month_couple = int(couple[0][5 : 7])
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
    # Calculation of the difference of values for each ordered pair of months of the first year, replacing the elements in the first year list and deleting the last value of 12th month (if the value is 'False', mantain that value)
    for value in range(len(first_year_monthly_variations) - 1):
        if value == False:
            first_year_monthly_variations[value] = False
        else:
            first_year_monthly_variations[value] = abs(first_year_monthly_variations[value] - first_year_monthly_variations[value + 1])
    first_year_monthly_variations = first_year_monthly_variations[0 : - 1]
    # Calculation of the difference of values for each ordered pair of months of the second year, replacing the elements in the second year list and deleting the last value of 12th month (if the value is 'False', mantain that value)
    for value in range(len(second_year_monthly_variations) - 1):
        if value == False:
            second_year_monthly_variations[value] = False
        else:
            second_year_monthly_variations[value] = abs(second_year_monthly_variations[value] - second_year_monthly_variations[value + 1])
    second_year_monthly_variations = second_year_monthly_variations[0 : - 1]
    # Creation of a list
    similar_monthly_variations = []
    # Loop for each value in the first year list
    for value in range(len(first_year_monthly_variations)):
        # If the value is 'False', add 'False' to the list
        if first_year_monthly_variations[value] == False:
            similar_monthly_variations.append(False)
        # If the difference of the differences of the values for each ordered pair of months of the two respective years is ±2, add 'True' to the list
        elif abs(first_year_monthly_variations[value] - second_year_monthly_variations[value]) <= 2:
            similar_monthly_variations.append(True)
        # If the difference of the differences of the values for each ordered pair of months of the two respective years is not ±2, add 'False' to the list
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