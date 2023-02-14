import os
import string

from dotenv import load_dotenv


class ReverseEachTenWordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.counter = 0

        load_dotenv()
        self.activate_middleware = (
            os.environ.get('ACTIVATE_REVERSE_MIDDLEWARE', 'False') == 'True'
        )

    @staticmethod
    def reverse_russian_words(text):
        result_content = ''
        russian_word = ''
        punctuation = set(string.punctuation)

        for i in text:
            if i in punctuation or i == ' ':
                result_content += russian_word[-1::-1]
                russian_word = ''
                result_content += i
                continue
            if ord('а') <= ord(i) <= ord('я') or ord('А') <= ord(i) <= ord(
                'Я'
            ):
                russian_word += i
            else:
                result_content += russian_word
                result_content += i
                russian_word = ''
        result_content += russian_word[-1::-1]

        return result_content

    def __call__(self, request):
        response = self.get_response(request)

        if self.activate_middleware is True:
            if self.counter == 10:
                content = response.content.decode()[6:-7]

                response.content = self.reverse_russian_words(content).encode()

                self.counter = 0

            self.counter += 1

        return response
