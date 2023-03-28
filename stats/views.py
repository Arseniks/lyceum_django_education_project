from django.shortcuts import render
from django.views.generic import View

from rating.models import Mark


class ShortUser(View):
    template_name = 'stats/short_user_stat.html'

    def get(self, request):
        marks = [
            (i.mark, i.date_created, i.get_mark_display(), i.item)
            for i in Mark.objects.filter(user=request.user)
        ]
        context = {
            'best_mark': max(marks, key=lambda el: (el[0], el[1])),
            'worst_mark': max(marks, key=lambda el: (-el[0], el[1])),
            'count': len(marks),
            'middle_value': sum([i[0] for i in marks]) / len(marks),
        }
        return render(request, self.template_name, context)
