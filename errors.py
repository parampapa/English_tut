"""
Модуль проекта для обработки ошибок 404 и 500.
"""

from flask import render_template

from app import app


@app.errorhandler(404)
def error404(error):
    """
       Обработчик для ошибки 404 Not Found.
       Активируется, когда запрошенная страница не найдена.

    Args:
        error: Exception, Объект ошибки, содержащий информацию об ошибке.

    Returns:
        tuple: Кортеж, содержащий объект ответа (отрисованный HTML-шаблон для
        ошибки 404) и числовой статус код ответа HTTP (404).
    """
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def error500(error):
    """
    Обработчик для ошибки 500 Internal Server Error.
    Активируется, когда на сервере происходит внутренняя ошибка.

    Args:
        error: Exception, Объект ошибки, содержащий информацию об ошибке.

    Returns:
        tuple: Кортеж, содержащий объект ответа (отрисованный HTML-шаблон для
        ошибки 500) и числовой статус код ответа HTTP (500).
    """
    return render_template('errors/500.html'), 500
