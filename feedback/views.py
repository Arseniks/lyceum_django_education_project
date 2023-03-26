from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View

from feedback import models
from feedback.forms import FeedbackFilesForm
from feedback.forms import FeedbackForm
from feedback.forms import FeedbackTextForm


class FeedbackView(View):
    template_name = 'feedback/feedback.html'

    def get(self, request):
        feedback_form = FeedbackForm()
        feedback_text_form = FeedbackTextForm()
        feedback_file_form = FeedbackFilesForm()
        context = {
            'feedback_form': feedback_form,
            'feedback_text_form': feedback_text_form,
            'feedback_file_form': feedback_file_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        feedback_form = FeedbackForm(request.POST)
        feedback_text_form = FeedbackTextForm(request.POST)
        feedback_file_form = FeedbackFilesForm(request.POST, request.FILES)

        if (
            feedback_form.is_valid()
            and feedback_text_form.is_valid()
            and feedback_file_form.is_valid()
        ):
            text = feedback_text_form.cleaned_data['text']
            mail = feedback_form.cleaned_data['mail']
            message = (
                'Благодарим за Ваши замечания и предложения!\nВы отправили '
                'отзыв о работе сайта KittyShop.\nВаш отзыв непременно '
                'передадут в службу клиентской поддержки для '
                'улучшения работы нашего сервиса.\n'
                f'Ваш отзыв:\n{text}\n\n'
                'Надеемся у вас будет положительный '
                'опыт использования сайта KittyShop\n'
                '---\n'
                'Интернет-магазин KittyShop'
            )
            send_mail(
                'KittyShop',
                message,
                settings.FEEDBACK_MAIL,
                [mail],
                fail_silently=False,
            )

            feedback_user = models.Feedback.objects.create(
                mail=mail,
            )
            models.FeedbackText.objects.create(
                feedback=feedback_user,
                text=text,
            )
            for user_file in request.FILES.getlist('files'):
                models.FeedbackFiles.objects.create(
                    feedback=feedback_user,
                    files=user_file,
                )

            messages.add_message(
                request, messages.INFO, 'Ваш отзыв был успешно отправлен!'
            )
            return redirect('feedback:feedback')
        context = {
            'feedback_form': feedback_form,
            'feedback_text_form': feedback_text_form,
            'feedback_file_form': feedback_file_form,
        }

        return render(request, self.template_name, context)
