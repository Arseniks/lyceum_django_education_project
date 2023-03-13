from django.conf import settings
from django.http import FileResponse


def download_image(request, file_name):
    print(file_name)
    file_name = str(settings.BASE_DIR) + file_name
    print(file_name)
    return FileResponse(open(file_name, mode='rb'), as_attachment=True)
