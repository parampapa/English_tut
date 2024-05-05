"""
       Модуль предназначен для запуска Flask-приложения при выполнении
       файла как основной программы.

       Импортирует объект app из модуля controller и модуль errors для
       регистрации обработчиков ошибок.
"""

if __name__ == '__main__':
    from controller import app
    from errors import app
    app.run()
