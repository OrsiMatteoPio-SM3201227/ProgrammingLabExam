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
                list.append(elements)
        # File closing
        file.close()
        # Adding elements of the list to the list of list
        listoflist.extend(list)

        # Creation of a list, which will have a string column and a numerical column from the previous list of list
        definitive_listoflist = []
        # List of list reading, line by line
        for string_row in listoflist:
            # Creaton of a list for each line of the previous list of list
            definitive_row = []
            # Line reading, element by element and using an index
            for i, element in enumerate(string_row):
                # Adding the first element in string type to the list
                if i == 0:
                    definitive_row.append(element)
                # Conversion of the second column from string type to numerical type
                else:
                    try:
                        definitive_row.append(float(element))
                    except ExamException as e:
                        print('Conversion error of the value "{}" to numerical type: "{}"'.format(element, e))
                        break
                # If lengths are equal, add elements of the list to the list of list
                if len(definitive_row) == len(string_row):
                    definitive_listoflist.extend(definitive_row)
        return definitive_listoflist
# ==============================
#            METHODS
# ==============================
#          DSMV method
# ==============================
# def detect_similar_monthly_variations():


# ==============================
#            PROGRAM
# ==============================
#          Main Program
# ==============================
time_series_file = CSVTimeSeriesFile(name = 'data.csv')

time_series = time_series_file.get_data()

print('Dati contenuti nel file: "{}"'.format(time_series))

# detect_similar_monthly_variations(time_series, years)