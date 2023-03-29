from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import View

from catalog.models import Item
from rating.models import Mark


class UserRatedItemsList(ListView):
    model = Mark
    template_name = 'stats/user_rated_items_list.html'
    context_object_name = 'marks'

    def get_queryset(self, **kwargs):
        return (
            super(UserRatedItemsList, self)
            .get_queryset()
            .filter(
                user__pk=self.kwargs.get('pk'),
            )
            .select_related(Mark.item.field.name)
            .only(
                f'{Mark.mark.field.name}',
                f'{Mark.item.field.name}__{Item.name.field.name}',
            )
            .order_by('-mark')
        )
        
        
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
