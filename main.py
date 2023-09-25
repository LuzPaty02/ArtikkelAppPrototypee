
import csv
import sqlite3


class Database:
    def __init__(self) -> None:
        self._csv_path: str = "ArtikkelApp/InglesAleman.csv"
        self._db_path: str = "ArtikkelApp/InglesAleman.db"
        self.search_results: dict[str, list[str]] = {
            "EnglishWord": [],
            "GermanWord": []
        }


    def _csv_to_database(self) -> None:
        """
        Convierte un archivo .csv en una base de datos .db con SQLite3.
        """

        # Se crea la conexión y el cursor
        _connection: sqlite3.Connection = sqlite3.connect(self._db_path)
        _cursor: sqlite3.Cursor = _connection.cursor()

        # Se crea una lista temporal para almacenar los datos
        _temp_list: list[tuple[str, str]] = []

        with open(self._csv_path, newline="", encoding="utf-8") as csvfile:
                    _reader = csv.reader(csvfile, delimiter=" ")
                    for row in _reader:
                        # Para casos en los que hay varios espacios en una línea
                        English_multipleWords_word = row[0].split(None, 1)
                        if len(English_multipleWords_word) >= 2:
                            english_words_Col = English_multipleWords_word[0].strip()
                            german_words_Col = English_multipleWords_word[1].strip()
                            
                            _temp_list.append((english_words_Col, german_words_Col))
                        else:
                            english_words_Col = row[0].strip()
                            german_words_Col = row[1].strip()

                            _temp_list.append((english_words_Col, german_words_Col))
        #Funcion si se usa archivo sql en vez de csv y se separa solo por comas 
        """ with open(self._csv_path, newline="", encoding="utf-8") as csvfile:
                _reader = csv.reader(csvfile, delimiter=",")
                for row in _reader:
                    # Ignorar comillas 
                    english_words_Col = row[0].strip().strip('"')
                    german_words_Col = row[1].strip().strip('"')

                    _temp_list.append((english_words_Col, german_words_Col))
            
            return _temp_list """

        # Se crea la tabla y se insertan los datos
        _cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS vocabulary (EnglishWord TEXT, GermanWord TEXT) '''
        )

        _connection.commit()

        # Se elimina la lista temporal para liberar memoria

        # Se insertan los datos en la tabla
        _cursor.executemany(
            ''' INSERT INTO vocabulary VALUES (?, ?) ''', _temp_list
        )

        _connection.commit()

        del _temp_list

        # Prueba de que la base de datos se creó correctamente
        # Por defecto, se comenta para evitar que se imprima en la terminal
        _test_printing = _cursor.execute(
            ''' SELECT * FROM vocabulary '''
         )

        for row in _test_printing:
             print(row)

        _cursor.close()
        _connection.close()


    def search_vocab(self, EnglishWord: str) -> dict[list[str], list[str]]:

        _connection: sqlite3.Connection = sqlite3.connect(self._db_path)
        _cursor: sqlite3.Cursor = _connection.cursor()

        list_search_results: list[tuple[str, str]] = _cursor.execute(
            '''SELECT * FROM vocabulary WHERE EnglishWord LIKE ?''', ('%' + EnglishWord + '%',)
        ).fetchall()

        self.search_results['EnglishWord'].clear()
        self.search_results['GermanWord'].clear()

        for result in list_search_results:
            self.search_results['EnglishWord'].append(result[0])
            self.search_results['GermanWord'].append(result[1])

        _cursor.close()
        _connection.close()

        return self.search_results 