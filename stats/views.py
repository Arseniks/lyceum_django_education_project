from django.shortcuts import render
from django.views.generic import View

from rating.models import Mark


class ShortUser(View):
    template_name = 'stats/short_user_stat.html'

    def get(self, request):
        if request.user.id:
            marks = [
                (i.mark, i.date_created, i.get_mark_display(), i.item)
                for i in Mark.objects.filter(user=request.user)
            ]
            if marks:
                context = {
                    'best_mark': max(marks, key=lambda el: (el[0], el[1])),
                    'worst_mark': max(marks, key=lambda el: (-el[0], el[1])),
                    'count': len(marks),
                    'middle_value': sum([i[0] for i in marks]) / len(marks),
                }
            else:
                context = {'message': 'Вы пока не поставили ни одной оценки'}
        else:
            context = {'message': 'Войдите, чтобы просмотреть статистику'}
        return render(request, self.template_name, context)
