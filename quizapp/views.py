from django.db.models import Max
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User

from .models import Question, Answer


# Create your views here.


class QuestionView(APIView):

    def post(self, request):
        req_data = request.data
        try:
            user = request.user
            if user.is_admin:
                get_user = User.objects.get(username=user)
                q_no = Question.objects.filter(created_by=get_user).all().aggregate(Max('q_no'))[
                    'q_no__max']
                qno_next = q_no + 1 if q_no else 1
                question = req_data['question']
                opt1 = req_data['opt1']
                opt2 = req_data['opt2']
                opt3 = req_data['opt3']
                opt4 = req_data['opt4']
                ans = req_data['ans']
                create_question = Question.objects.create(q_no=qno_next, question=question, opt1=opt1, opt2=opt2,
                                                          opt3=opt3, opt4=opt4, ans=ans, created_by=get_user)
                return Response({'success': 'Question created successfully'})

            else:
                return Response({'error': 'Your are not allowed to do this action'})

        except:
            return Response({'error': 'Authorization Required'})


class AnswerView(APIView):

    def post(self, request):
        req_data = request.data
        try:
            user = request.user
            if user.is_user:
                get_user = User.objects.get(username=user)
                q_no = req_data['q_no']
                get_question = Question.objects.get(q_no=q_no)
                ans = req_data['ans']
                create_ans = Answer.objects.create(user=get_user, q_no=get_question, ans=ans)
                return Response({'success': 'your answer is successfully submitted'})

            else:
                return Response({'error': 'Your are not allowed to do this action'})

        except:
            return Response({'error': 'Authorization Required'})


class AnswerSummaryView(APIView):

    def post(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({'error': 'Authorization Required'})
        correct = 0
        wrong = 0
        try:
            user = request.user
            if user.is_user:
                get_user_answers = Answer.objects.filter(user=user)
                for answer in get_user_answers:
                    question = answer.q_no
                    if question.ans == answer.ans:
                        correct += 1
                    else:
                        wrong += 1
                total_questions = Question.objects.all().count()
                return Response({'user': user.username, 'total_questions': total_questions,
                                 'correct_answers': correct, 'wrong_answers': wrong})

            elif user.is_admin:
                req_user = request.data.get('user')
                if req_user:
                    get_user = User.objects.get(username=req_user)
                    user_answers = Answer.objects.filter(user=get_user)
                    print(user_answers)
                    for answer in user_answers:
                        question = answer.q_no
                        if question.ans == answer.ans:
                            correct += 1
                        else:
                            wrong += 1
                    total_questions = Question.objects.all().count()
                    return Response({'user': req_user, 'total_questions': total_questions,
                                     'correct_answers': correct, 'wrong_answers': wrong})
                else:
                    return Response({'error': 'Provide a user to view answer summary'})

                # return Response({'error': 'Admin user does not have any answers'})

        except Answer.DoesNotExist:
            return Response({'error': 'No answers submitted for this user'})



