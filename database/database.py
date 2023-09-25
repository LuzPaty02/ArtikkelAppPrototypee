
import csv
import sqlite3

class Database:

    def __init__(self) -> None:
        self._csv_path: str = "database/definite_german_articles.csv"
        self._db_path: str = "database/definite_german_articles.db"
        self.search_results: dict[str, list[str]] = {
            "english_word": [],
            "german_word": [],
            "image_path" : []
        }


    def _csv_to_database(self) -> None:
        """
        Convierte un archivo .csv en una base de datos .db con SQLite3.
        """

        # Se crea la conexión y el cursor
        _connection: sqlite3.Connection = sqlite3.connect(self._db_path)
        _cursor: sqlite3.Cursor = _connection.cursor()

        # Se crea una lista temporal para almacenar los datos
        _temp_list: list[tuple[str, str, str]] = []

        with open(self._csv_path, newline="", encoding="utf-8") as csvfile:
                    _reader = csv.reader(csvfile, delimiter=",")
                    for row in _reader:
                        english_word: str = row[0]
                        german_word_to_clean: str = row[1]

                        # Se separan las direcciones de las imagenes en el csv
                        key_idx: int = german_word_to_clean.find('<img src="')
                        german_word: str = german_word_to_clean[0:key_idx]
                        img_path: str = f"{german_word}.jpg".replace(" ", "")

                        _temp_list.append((english_word, german_word, img_path))

        # Se crea la tabla y se insertan los datos
        _cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS vocabulary (EnglishWord TEXT, GermanWord TEXT, ImagePath TEXT) '''
        )

        _connection.commit()


        # Se insertan los datos en la tabla
        _cursor.executemany(
            ''' INSERT INTO vocabulary VALUES (?, ?, ?) ''', _temp_list
        )

        _connection.commit()

        # Se elimina la lista temporal para liberar memoria
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
        """
        <<< Obsoleto >>>

        Esta función se encarga de buscar una palabra en la base de datos y retornar una lista con los resultados.

        Basado en la KanjiApp de iMega34
        Repo: https://github.com/iMega34/KanjiApp
        """

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


if __name__ == "__main__":
    db: Database = Database()
    db._csv_to_database()
