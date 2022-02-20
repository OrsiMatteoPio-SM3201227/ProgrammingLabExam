# ==============================
#           CLASSI
# ==============================
#    Classe per ExamException
# ==============================
class ExamException(Exception):
    pass

# ==============================
#       Classe per Diff
# ==============================
class Diff():
    
    def __init__(self, ratio = 1):
        # Test per ratio
        if not isinstance(ratio, (int, float)):
            raise ExamException('Invalid type for ratio, only int supported. Got "{}"'. format(type(ratio)))

        if ratio < 1:
            raise ExamException('Negative or zero ratio value provided')

        # Istanziamento dell'attributo opzionale "ratio"
        self.ratio = ratio
    
    def compute(self, data):
        # Test per data e i suoi elementi
        if not isinstance(data, list):
            raise ExamException('Invalid type for data, only list supported. Got "{}"'.format(type(data)))
        
        if len(data) < 2:
            raise ExamException('Not enough data to compute a difference')
        
        for item in data:
            if not isinstance(item, (int, float)):
                raise ExamException('Got non-numeric item in the list data: "{}"'.format(item))
        
        # Istanziamento di una lista
        differences = []

        # Ciclo per ogni elemento di data
        for item in range(len(data) - 1):
            # Calcolo della differenza e compilazione della lista
            differences.append(abs(data[item] - data[item + 1]) / self.ratio)

        # Ritorno della lista
        return differences

# ==============================
#           PROGRAMMA
# ==============================
#       Corpo del programma
# ==============================
diff = Diff()

result = diff.compute([2, 4, 8, 16])

print(result)