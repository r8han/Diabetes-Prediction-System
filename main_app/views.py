from django.shortcuts import render, redirect
from django.utils import timezone
from .models import HistoryModel
import joblib


def home(request):
    user = request.user
    if request.user.is_authenticated:
        return render(request, 'main_app/home.html')
    return redirect("login")


def predict(request):
    user = request.user
    if request.user.is_authenticated:
        if request.method == 'POST':
            data_list = []
            data_list.append(int(request.POST.get('pregancies')))
            data_list.append(int(request.POST.get('glucose')))
            data_list.append(int(request.POST.get('bp')))
            data_list.append(int(request.POST.get('skin')))
            data_list.append(int(request.POST.get('insulin')))
            data_list.append(float(request.POST.get('bmi')))
            data_list.append(float(request.POST.get('dpf')))
            data_list.append(int(request.POST.get('age')))

            model = joblib.load('static/model/rfc_model.sav')
            result = model.predict([data_list])
            print(result)
            if result == 1:
                resulttext = "Positive"
            else:
                resulttext = "Negative"

            HistoryModel.objects.create(user=user, pregancies=data_list[0], glucose=data_list[1], bp=data_list[2], skin=data_list[3],
                                        insulin=data_list[4], bmi=data_list[5], dpf=data_list[6], age=data_list[7], result=resulttext, datetime=timezone.now())
            context = {
                'result': result,
            }
            return render(request, 'main_app/result.html', context)
        return render(request, 'main_app/predict.html')
    return redirect("login")


def history(request):
    user = request.user
    if user.is_authenticated:
        empty = False
        history = HistoryModel.objects.filter(
            user=user).order_by('-datetime')[:7]
        if not history.exists():
            empty = True
        context = {
            'history': history,
            'empty': empty,
        }
        return render(request, 'main_app/history.html', context)
    return redirect("login")


def about(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'main_app/about.html')
    return redirect("login")
