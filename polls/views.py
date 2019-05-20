import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .forms import PollForm, CommentForm, ChangePasswordForm, RegisterForm, PollModelForm, QuestionForm, ChoiceModelForm
from .models import Poll, Question, Answer, Comment, Profile, Choice


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


@login_required
@permission_required('users.change_barbershop')

def details(req, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    ques_count = Question.objects.filter(poll_id=poll.id).count()
    poll.question_len = ques_count

    for question in poll.question_set.all():
        name = 'choice' + str(question.id)
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
    return render(req, 'polls/detail.html', context={'poll': poll})


@login_required
@permission_required('polls.add_poll')
def create(req):
    QuestionFormSet = formset_factory(QuestionForm, extra=2)
    context = {}
    if (req.method == 'POST'):
        form = PollModelForm(req.POST)
        formset = QuestionFormSet(req.POST)
        if form.is_valid():
            poll = form.save()
            if formset.is_valid():
                for question_form in formset:
                    Question.objects.create(
                        text=question_form.cleaned_data.get('text'),
                        type=question_form.cleaned_data.get('type'),
                        poll=poll
                    )
                    context['success'] = "Poll %s created successfully" % (poll.title)
            # poll = Poll.objects.create(
            #     title=form.cleaned_data.get('title'),
            #     start_date=form.cleaned_data.get('start_date'),
            #     end_date=form.cleaned_data.get('end_date'),
            #
            # )
            # for i in range(1, form.cleaned_data.get('no_question') + 1):
            #     Question.objects.create(
            #         text='Q' + str(i),
            #         type='01',
            #         poll=poll
            #
            #     )
    else:
        form = PollModelForm()
        formset = QuestionFormSet()
    context['form'] = form
    context['formset'] = formset

    return render(req, 'polls/create.html', context=context)

@login_required
@permission_required('polls.change_poll')
def update(req, poll_id):
    poll = Poll.objects.get(id=poll_id)
    QuestionFormSet = formset_factory(QuestionForm, extra=2, max_num=10)
    if (req.method == 'POST'):
        form = PollModelForm(req.POST, instance=poll)
        formset = QuestionFormSet(req.POST)
        if form.is_valid():
            form.save()
            if formset.is_valid():
                for question_form in formset:
                    if question_form.cleaned_data.get('question_id'):
                        question = Question.objects.get(id=question_form.cleaned_data.get('question_id'))
                        if question:
                            question.text = question_form.cleaned_data.get('text')
                            question.type = question_form.cleaned_data.get('type')
                            question.save()
                        else:
                            if question_form.cleaned_data.get('text'):
                                Question.objects.create(
                                    text=question_form.cleaned_data.get('text'),
                                    type=question_form.cleaned_data.get('type'),
                                    poll=poll
                                )
            # poll = Poll.objects.create(
            #     title=form.cleaned_data.get('title'),
            #     start_date=form.cleaned_data.get('start_date'),
            #     end_date=form.cleaned_data.get('end_date'),
            #
            # )
            # for i in range(1, form.cleaned_data.get('no_question') + 1):
            #     Question.objects.create(
            #         text='Q' + str(i),
            #         type='01',
            #         poll=poll
            #
            #     )
    else:
        form = PollModelForm(instance=poll)
        data = []
        for question in poll.question_set.all():
            data.append(
                {
                    'text':question.text,
                    'type':question.type,
                    'question_id':question.id
                }
            )
        formset = QuestionFormSet(initial=data)
    context = {
        'form': form,
        'poll' : poll,
        'formset' :formset
    }

    return render(req, 'polls/update.html', context=context)
@login_required()
@permission_required('polls.change_poll')
def delete_question(req, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect('update', poll_id=question.poll_id)
@login_required()
@permission_required('polls.change_poll')
def add_choice(req, question_id):
    question = Question.objects.get(id=question_id)
    choices = []
    for q in question.choice_set.all():
        data = {
            'text' : q.text,
            'value' : q.value
        }
        choices.append(data)
    print(choices)
    context = {'question':question, 'choices':choices}
    return render(req, 'choices/add.html', context)


# @login_required()
# @permission_required('polls.change_poll')
@csrf_exempt
def add_choice_api(req, question_id):
    if req.method == "POST":
        choice_list = json.loads(req.body)
        print(choice_list)
        error_list = []
        for choice in choice_list:
            data = {
                'text':choice['text'],
                'value':choice['value'],
                'question':question_id
            }
            form = ChoiceModelForm(data)
            print(form.is_valid())
            if form.is_valid():
                print("success")
                form.save()
            else:
                error_list.append(form.errors.as_text())

        if len(error_list) == 0:
            return JsonResponse({'messages' : 'success'}, status=200)
        else:
            return JsonResponse({'message':error_list}, status=400)
    elif(req.method == "DELETE"):
        choice_list = json.load(req.body)
        print(choice_list)
    return JsonResponse({'message':'this API does not accept GET request'}, status=405)

def my_login(req):
    context = {}
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user:
            login(req, user)
            next_url = req.POST.get('next_url')  # hidden field input name
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            error = 'Wrong username or password'
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password'

    next_url = req.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(req, 'polls/login.html', context=context)


@login_required
def my_logout(req):
    logout(req)
    return redirect('login')


def comment(req):
    if (req.method == "POST"):
        form = CommentForm(req.POST)
        if form.is_valid():
            Comment.objects.create(
                title=form.cleaned_data.get('title'),
                body=form.cleaned_data.get('body'),
                email=form.cleaned_data.get('email'),
                tel=form.cleaned_data.get('tel'),
            )
    else:
        form = CommentForm()
    context = {
        'form': form
    }
    return render(req, "polls/comment.html", context)


@login_required()
def changepass(req):
    if (req.method == "POST"):
        form = ChangePasswordForm(req.POST)
        if form.is_valid():
            user = req.user
            u = authenticate(req, username=user.username, password=form.cleaned_data.get('old_password'))

            if(u):
                u.set_password(form.cleaned_data.get('new_password1'))
                u.save()
                return redirect('login')
            else:
                form.add_error('old_password', "รหัสผ่านผิด")

    else:
        form = ChangePasswordForm()
    context = {
        'form': form
    }
    return render(req, 'polls/change_password.html', context)


def register(req):
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            if(not User.objects.filter(username=form.cleaned_data.get('username')).exists()):
                u = User.objects.create_user(username=form.cleaned_data.get('username'), email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
                Profile.objects.create(
                    user=u,
                    line_id=form.cleaned_data.get('line_id'),
                    facebook=form.cleaned_data.get('facebook'),
                    gender=form.cleaned_data.get('gender'),
                    birthday=form.cleaned_data.get('birthday')
                )
                return redirect('login')
            else:
                form.add_error('username', "Username นี้มีในระบบแล้ว")
    else:
        form = RegisterForm()
    context = {
        'form' : form
    }
    return render(req, 'polls/register.html', context)
