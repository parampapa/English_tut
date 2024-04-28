from flask import render_template

from app import app


@app.errorhandler(404)
def error404(error):
    """
       Обработчик для ошибки 404 Not Found.
       Активируется, когда запрошенная страница не найдена.

       :param error: Объект ошибки, содержащий информацию об ошибке.

       :return render_template: Отрисовывает шаблон HTML для ошибки 404.
       - 404: статус код ответа HTTP, указывающий на ошибку Not Found.
       """
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def error404(error):
    """
    Обработчик для ошибки 500 Internal Server Error.
    Активируется, когда на сервере происходит внутренняя ошибка.

    :param error: Объект ошибки, содержащий информацию об ошибке.

    :return render_template: Отрисовывает шаблон HTML для ошибки 500.
    - 500: статус код ответа HTTP, указывающий на внутреннюю ошибку сервера.
    """
    return render_template('errors/500.html'), 500
