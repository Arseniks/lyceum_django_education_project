from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render

from feedback.forms import FeedbackForm


def feedback(request):
    template = 'feedback/feedback.html'
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        text = form.cleaned_data['text']
        mail = form.cleaned_data['mail']
        message = (
            'Благодарим за Ваши замечания и предложения!\nВы отправили отзыв '
            'о работе сайта KittyShop.\nВаш отзыв непременно передадут в службу '
            'клиентской поддержки для улучшения работы нашего сервиса.\n'
            f'Ваш отзыв:\n{text}\n\n'
            'Надеемся у вас будет положительный опыт использования сайта KittyShop\n'
            '---\n'
            'Интеренет-магазин KittyShop'
        )
        send_mail(
            'KittyShop',
            message,
            settings.FEEDBACK_MAIL,
            [mail],
            fail_silently=False,
        )
        return redirect('feedback:successfully_sent')
    context = {'form': form}
    return render(request, template, context)


def successfully_sent(request):
    template = 'feedback/successfully_sent.html'
    return render(request, template)
