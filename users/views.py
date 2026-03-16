from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import StudentProfile
from .forms import StudentProfileForm


@login_required
def student_profile_view(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("student_profile")
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, "users/student_profile.html", {"form": form})