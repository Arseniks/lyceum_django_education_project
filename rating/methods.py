from rating.models import Mark


def add_mark(user_id, item_id, mark):
    cur_mark = Mark.objects.filter(user_id=user_id, item_id=item_id)
    if cur_mark and mark:
        cur_mark.delete()
        add_mark = Mark.objects.create(
            user_id=user_id, item_id=item_id, mark=mark
        )
        add_mark.save()
    elif cur_mark:
        cur_mark.delete()
    elif mark:
        add_mark = Mark.objects.create(
            user_id=user_id, item_id=item_id, mark=mark
        )
        add_mark.save()


def get_initial_form_value(user_id, item_id):
    cur_mark = Mark.objects.filter(user_id=user_id, item_id=item_id)
    if cur_mark:
        return cur_mark[0].mark


def get_marks_statistic(item_id):
    marks = [i.mark for i in Mark.objects.filter(item_id=item_id)]
    if marks:
        return len(marks), round(sum(marks) / len(marks), 3)
    return 0, 'не сформирован'
