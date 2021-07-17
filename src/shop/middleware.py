from django.http import HttpResponse, HttpResponse
import re

RE_EMPTY_STRING = r'\n\s*?\n'
RE_STRING_SPACE_PREFIX = r'\n\s+'


def html_optimize(get_response):
    """
    Оптимизирует html код, генерируемый автоматически
    """

    def middleware(request):
        response: HttpResponse = get_response(request)

        new_content = re.sub(RE_EMPTY_STRING, lambda *_: '\n', response.content.decode())
        new_content = re.sub(RE_STRING_SPACE_PREFIX, lambda *_: '\n', new_content)

        response.content = new_content.encode()
        response['Content-Length'] = len(response.content)
        return response

    return middleware


def add_banner(get_response):
    """
        Добавляет рекламный баннер на все страницы сайта
    """

    def middleware(request):
        response: HttpResponse = get_response(request)

        response.content += '<div class="banners">' \
                                '<div class="banner">Объявление</div>' \
                                '<div class="banner">Объявление</div>' \
                                '<div class="banner">Реклама</div>' \
                            '</div>'.encode()
        response['Content-Length'] = len(response.content)
        return response

    return middleware
