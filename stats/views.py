from django.shortcuts import render
from django.views.generic import View, DetailView

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


class UserRatedItemsList(DetailView):
    model = Mark
    template_name = 'stats/user_rated_items_list.html'
    context_object_name = 'marks'

    def get(self, request, pk, *args, **kwargs):
        self.pk = pk
        return super().get()

    def get_queryset(self):
        return Mark.objects.filter(
            user__pk=self.pk,
        )
