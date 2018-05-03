class Error:
    def __init__(self, file_name, coordintes, err_code):
        self.file_name = file_name
        self.coordinates = coordintes
        self.err_code = err_code
        self.language = 'english'
        self.languages = ('english')

    def write(self):
        print('On {0} {1}: {2}'.
              format(self.file_name, self.coordinates, self.description()))

    def get_code(self):
        return self.err_code

    def description(self):
        with open('errors/{}.txt'.format(self.language)) as file:
            for line in file:
                if line.find(self.err_code) != -1:
                    dates = line.split('-')
                    return dates[1]

    def change_language(self, language):
        if language in self.languages:
            self.language = language
