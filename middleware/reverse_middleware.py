import string

from django.conf import settings


class ReverseEachTenWordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.counter = 0
        self.activate_middleware = settings.ACTIVATE_REVERSE_MIDDLEWARE

    @staticmethod
    def is_russian_letter(letter):
        if ord('а') <= ord(letter) <= ord('я'):
            return True
        if ord('А') <= ord(letter) <= ord('Я'):
            return True
        return False

    def reverse_russian_words(self, text):
        result_content = ''
        russian_word = ''
        punctuation = set(string.punctuation)

        for i in text:
            if i in punctuation or i == ' ':
                result_content += russian_word[::-1]
                russian_word = ''
                result_content += i
                continue
            if self.is_russian_letter(i):
                russian_word += i
            else:
                result_content += russian_word
                result_content += i
                russian_word = ''
        result_content += russian_word[::-1]

        return result_content

    def __call__(self, request):
        response = self.get_response(request)

        if self.activate_middleware is True:
            if self.counter == 10:
                content = response.content.decode()
                response.content = self.reverse_russian_words(content).encode()
                self.counter = 0
            self.counter += 1

        return response
