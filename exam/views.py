from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam, Question, Answer, Result
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import ExamForm
from django.contrib import messages

def user_exams(request, user_id):
    # Filter exams created by the user
    exams = Exam.objects.filter(created_by=user_id)
    return render(request, 'user_exams.html', {'exams': exams})
@login_required
def list_exams(request):
    exams = Exam.objects.all()
    return render(request, 'exam_list.html', {'exams': exams})

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    
    if not exam.can_take_exam(request.user):
        messages.error(request, "You cannot take this exam. Either you've already completed it or it's not published.")
        return redirect('exam:user-exams', user_id=request.user.id)

    
    if request.method == 'POST':
        score = 0
        for question in exam.questions.all():
            selected_answer_id = request.POST.get(str(question.id))
            if selected_answer_id:
                try:
                    selected_answer = Answer.objects.get(pk=selected_answer_id)
                    if selected_answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    pass   
                
                
                
                  

        Result.objects.create(
            exam=exam,
            student=request.user,
            score=score,
            submitted_at=timezone.now()
        )
        return redirect('exam:view_result', exam_id=exam.id)

    return render(request, 'take_exam.html', {'exam': exam})


@login_required
@login_required
def view_result(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    
    # Fetch the student's result for the given exam, if exists
    result = Result.objects.filter(exam=exam, student=request.user).first()  # Use 'first()' to get only one result
    
    if not result:
        # Handle the case where the result doesn't exist
        return render(request, 'no_result.html', {'exam': exam})
    
    return render(request, 'view_result.html', {'exam': exam, 'result': result})




@login_required
def exam_dashboard(request):
    exams = request.user.exams.all()
    return render(request, 'exam_dashboard.html', {'exams': exams})

@login_required
def create_exam(request):
    if request.method == "POST":
        exam_form = ExamForm(request.POST)
        if exam_form.is_valid():
            exam = exam_form.save(commit=False)
            exam.is_published = request.POST.get('is_published', False) == 'on' 
            exam.created_by = request.user
            exam.save()

            # Process questions and answers
            questions_data = {}
            for key, value in request.POST.items():
                if key.startswith('question_'):
                    question_num = key.split('_')[1]
                    if question_num not in questions_data:
                        questions_data[question_num] = {'text': value, 'answers': {}}
                elif key.startswith('answer_'):
                    _, q_num, a_num = key.split('_')
                    if q_num not in questions_data:
                        questions_data[q_num] = {'text': '', 'answers': {}}
                    questions_data[q_num]['answers'][a_num] = {
                        'text': value,
                        'is_correct': f'correct_{q_num}_{a_num}' in request.POST
                    }

            # Save questions and answers
            for q_data in questions_data.values():
                if q_data['text'].strip():
                    question = Question.objects.create(
                        exam=exam,
                        text=q_data['text']
                    )
                    for a_data in q_data['answers'].values():
                        if a_data['text'].strip():
                            Answer.objects.create(
                                question=question,
                                text=a_data['text'],
                                is_correct=a_data['is_correct']
                            )

            return redirect('exam:exam_list')
    else:
        exam_form = ExamForm()

    return render(request, 'create-exam.html', {
        'form': exam_form,
    })
    
@login_required
def exam_list(request):
    created_exams = Exam.objects.filter(created_by=request.user)
    available_exams = Exam.objects.filter(is_published=True).exclude(created_by=request.user)
    
    # Add has_result information to available_exams
    for exam in available_exams:
        exam.has_result = Result.objects.filter(
            exam=exam,
            student=request.user
        ).exists()
    
    context = {
        'created_exams': created_exams,
        'available_exams': available_exams
    }
    return render(request, 'exam_list.html', context)