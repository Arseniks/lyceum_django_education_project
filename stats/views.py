from django.db.models import Avg
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import View

from catalog.models import Item
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


class ItemStats(DetailView):
    template_name = 'stats/item_stat.html'
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemStats, self).get_context_data(**kwargs)
        item = context.get('item')
        item_marks = Mark.objects.filter(item=item)

        if item_marks.exists():
            stat_info = item_marks.aggregate(
                Min(Mark.mark.field.name),
                Max(Mark.mark.field.name),
                Avg(Mark.mark.field.name),
                Count(Mark.mark.field.name),
            )
            avg_rating = stat_info[f'{Mark.mark.field.name}__avg']
            mark_count = stat_info[f'{Mark.mark.field.name}__count']

            max_mark = stat_info[f'{Mark.mark.field.name}__max']
            min_mark = stat_info[f'{Mark.mark.field.name}__min']

            max_user = item_marks.select_related(
                f'{Mark.user.field.name}'
            ).get(mark=max_mark)

            min_user = item_marks.select_related(
                f'{Mark.user.field.name}'
            ).get(mark=min_mark)

            context.update(
                {
                    'avg_rating': avg_rating,
                    'mark_count': mark_count,
                    'max_user': max_user,
                    'min_user': min_user,
                }
            )

        return context
