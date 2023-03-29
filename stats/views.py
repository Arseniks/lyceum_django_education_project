from django.db.models import Avg
from django.db.models import Max
from django.db.models import Min
from django.shortcuts import render
from django.views.generic import DetailView

from rating.models import Mark


class ShortUserStatsView(DetailView):
    template_name = 'stats/short_user_stat.html'

    def get(self, request, pk):
        query = Mark.objects.filter(user=pk)
        if query:
            best_mark = query.aggregate(Max(Mark.mark.field.name))['mark__max']
            best_mark_date = query.filter(mark=best_mark).aggregate(
                Max(Mark.date_created.field.name)
            )['date_created__max']
            worst_mark = query.aggregate(Min(Mark.mark.field.name))[
                'mark__min'
            ]
            worst_mark_date = query.filter(mark=worst_mark).aggregate(
                Max(Mark.date_created.field.name)
            )['date_created__max']
            context = {
                'best_mark': query.get(
                    mark=best_mark, date_created=best_mark_date
                ),
                'worst_mark': query.get(
                    mark=worst_mark, date_created=worst_mark_date
                ),
                'count': query.count(),
                'middle_value': round(
                    query.aggregate(Avg(Mark.mark.field.name))['mark__avg'], 3
                ),
            }
        else:
            context = {'message': 'Вы пока не поставили ни одной оценки'}
        return render(request, self.template_name, context)
