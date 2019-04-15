from django.http import HttpResponse
from django.shortcuts import render

# poll_list = [
#     {
#         'id': 1,
#         'title': 'การสอนวิชา Web Programming',
#         'questions': [
#             {
#                 'text': 'อาจารย์บัณฑิตสอนน่าเบื่อไหม',
#                 'choices': [
#                     {'text': 'น่าเบื่อมาก', 'value': 1},
#                     {'text': 'ค่อนข้างน่าเบื่อ', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างสนุก', 'value': 4},
#                     {'text': 'สนุกมากๆ', 'value': 5}
#                 ]
#             },
#             {
#                 'text': 'นักศึกษาเรียนรู้เรื่องหรือไม่',
#                 'choices': [
#                     {'text': 'ไม่รู้เรื่องเลย', 'value': 1},
#                     {'text': 'รู้เรื่องนิดหน่อย', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'เรียนรู้เรื่อง', 'value': 4},
#                     {'text': 'เรียนเข้าใจมากๆ', 'value': 5}
#                 ]
#             },
#             {
#                 'text': 'เครื่องคอมพิวเตอร์ใช้งานดีหรือไม่',
#                 'choices': [
#                     {'text': 'เครื่องช้ามาก', 'value': 1},
#                     {'text': 'เครื่องค่อนข้างช้า', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'เครื่องเร็ว', 'value': 4},
#                     {'text': 'เครื่องเร็วมากๆ', 'value': 5}
#                 ]
#             },
#
#         ]
#     },
#     {
#         'id': 2,
#         'title': 'ความยากข้อสอบ mid-term',
#         'questions': [
#             {
#                 'text': 'ข้อ 1',
#                 'choices': [
#                     {'text': 'ง่ายมากๆ', 'value': 1},
#                     {'text': 'ค่อนข้างง่าย', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างยาก', 'value': 4},
#                     {'text': 'ยากมากๆ', 'value': 5}
#                 ]
#             },
#             {
#                 'text': 'ข้อ 2',
#                 'choices': [
#                     {'text': 'ง่ายมากๆ', 'value': 1},
#                     {'text': 'ค่อนข้างง่าย', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างยาก', 'value': 4},
#                     {'text': 'ยากมากๆ', 'value': 5}
#                 ]
#             },
#             {
#                 'text': 'ข้อ 3',
#                 'choices': [
#                     {'text': 'ง่ายมากๆ', 'value': 1},
#                     {'text': 'ค่อนข้างง่าย', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างยาก', 'value': 4},
#                     {'text': 'ยากมากๆ', 'value': 5}
#                 ]
#             },
#             {
#                 'text': 'ข้อ 4',
#                 'choices': [
#                     {'text': 'ง่ายมากๆ', 'value': 1},
#                     {'text': 'ค่อนข้างง่าย', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างยาก', 'value': 4},
#                     {'text': 'ยากมากๆ', 'value': 5}
#                 ]
#             },
#             {
#                 'text': 'ข้อ 5',
#                 'choices': [
#                     {'text': 'ง่ายมากๆ', 'value': 1},
#                     {'text': 'ค่อนข้างง่าย', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างยาก', 'value': 4},
#                     {'text': 'ยากมากๆ', 'value': 5}
#                 ]
#             },
#             {
#                 'text': 'ข้อ 6',
#                 'choices': [
#                     {'text': 'ง่ายมากๆ', 'value': 1},
#                     {'text': 'ค่อนข้างง่าย', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างยาก', 'value': 4},
#                     {'text': 'ยากมากๆ', 'value': 5}
#                 ]
#             },
#
#         ]
#     },
#
#     {
#         'id': 3,
#         'title': 'อาหารที่ชอบ',
#         'questions': [
#             {
#                 'text': 'พิซซ่า',
#                 'choices': [
#                     {'text': 'ไม่ชอบเลย', 'value': 1},
#                     {'text': 'ค่อนข้างไม่ชอบ', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างชอบ', 'value': 4},
#                     {'text': 'ชอบมากๆ', 'value': 5}
#                 ]
#             },
#             {
#                 'text': 'ไก่ทอด',
#                 'choices': [
#                     {'text': 'ไม่ชอบเลย', 'value': 1},
#                     {'text': 'ค่อนข้างไม่ชอบ', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างชอบ', 'value': 4},
#                     {'text': 'ชอบมากๆ', 'value': 5}
#                 ]
#             },
#             {
#                 'text': 'แฮมเบอร์เกอร์',
#                 'choices': [
#                     {'text': 'ไม่ชอบเลย', 'value': 1},
#                     {'text': 'ค่อนข้างไม่ชอบ', 'value': 2},
#                     {'text': 'เฉยๆ', 'value': 3},
#                     {'text': 'ค่อนข้างชอบ', 'value': 4},
#                     {'text': 'ชอบมากๆ', 'value': 5}
#                 ]
#             },
#
#         ]
#     },
# ]


# Create your views here.
from .forms import PollForm
from .models import Poll, Question, Answer


def index(req):
    poll_list = Poll.objects.all()
    for poll in poll_list:
        ques_count = Question.objects.filter(poll_id=poll.id).count()
        poll.question_len = ques_count


    print(poll_list)
    context = {
        "page_title": "My Polls",
        "poll_list": poll_list,
    }
    return render(req, "polls/index.html", context=context)


def details(req, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    ques_count = Question.objects.filter(poll_id=poll.id).count()
    poll.question_len = ques_count

    print(poll)



    for question in poll.question_set.all():
        print(question)
        name = 'choice'+str(question.id)
        choice_id = req.POST.get(name)
        if choice_id:
            try:
                ans = Answer.objects.get(question_id=question.id)
                ans.choice_id = choice_id
                ans.save()
            except Answer.DoesNotExist:
                Answer.objects.create(
                    choice_id=choice_id,
                    question_id=question.id
                )
    return render(req, 'polls/detail.html', context={'poll':poll})


def create(req):
    if(req.method == 'POST'):
        form = PollForm(req.POST)

        if form.is_valid():
            poll = Poll.objects.create(
                title=form.cleaned_data.get('title'),
                start_date=form.cleaned_data.get('start_date'),
                end_date=form.cleaned_data.get('end_date'),

            )
        for i in range(1, form.cleaned_data.get('no_question')+1):
            Question.objects.create(
                text='Q'+str(i),
                type='01',
                poll=poll

            )
    else:
        form = PollForm()
    context = {
        'form' : form
    }

    return render(req, 'polls/create.html' ,context=context)