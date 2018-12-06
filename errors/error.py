import configparser


__LANGUAGES = ('english', 'russian')


class Error:
    def __init__(self, coordinates, err_code):
        self.settings = configparser.ConfigParser()
        self.settings.read('errors/settings.ini')
        self.coordinates = coordinates
        self.err_code = err_code
        self.language = self.settings['Languages']['Language']

    def write(self):
        print('{0}: {1}'.
              format(self.coordinates, self.description()))

    def get_code(self):
        return self.err_code

    def description(self):
        with open('errors/languages/{}.txt'.format(self.language)) as file:
            for line in file:
                if line.find(self.err_code) != -1:
                    dates = line.split('-')
                    return dates[1].rstrip()

    def err_code(self):
        return self.err_code
