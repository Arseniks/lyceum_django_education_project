from django.conf import settings
from django.http import FileResponse
from django.views.generic import View


class DownloadImageView(View):
    def get(self, request, file_name):
        file_name = str(settings.BASE_DIR) + file_name
        return FileResponse(open(file_name, mode='rb'), as_attachment=True)
