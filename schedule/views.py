from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Date, Project, DateBoundWithProject
from .forms import DateBoundWithProjectForm
import datetime


@login_required
def admin(request, year=datetime.date.year, month=datetime.date.month):
    if request.method == "GET":
        if "previous_month" in request.GET:
            if month > 1:
                month -= 1
            else:
                month = 12
                year -= 1

            return redirect(admin, year=year, month=month)
        elif "next_month" in request.GET:
            if month < 12:
                month += 1
            else:
                month = 1
                year += 1
            return redirect(admin, year=year, month=month)

    cal = get_calendar(year, month)
    dates_in_database = Date.objects.all()
    dates_in_database = [date.__str__() for date in dates_in_database]
    month_str = str(month)
    context = {"cal": cal, "dates_in_database": dates_in_database, "year": year, "month_str": month_str}
    return render(request=request, template_name="schedule/admin.html", context=context)


@login_required
def date(request, year, month, day):
    date = Date.objects.get(date=datetime.date(year, month, day))
    projects = list(Project.objects.all())
    saved_projects_for_the_day = DateBoundWithProject.objects.filter(date=date)
    saved_projects = [saved_project.project for saved_project in saved_projects_for_the_day]
    untouched_projects = [project for project in projects if project not in saved_projects]

    date_bound_project_form = DateBoundWithProjectForm()
    saved_project_forms = [DateBoundWithProjectForm(instance=project) for project in saved_projects_for_the_day]

    saved_projects_and_forms = zip(saved_projects, saved_project_forms)

    if request.method == "POST":

        if "delete" in request.POST:
            project = Project.objects.filter(project=request.POST.get("delete")).get()
            project_to_delete = DateBoundWithProject.objects.filter(date=date, project=project)
            project_to_delete.delete()
            return redirect("date", year, month, day)

        else:
            filled_form = DateBoundWithProjectForm(request.POST)
            if filled_form.is_valid():
                project = Project.objects.filter(project=request.POST.get("project_name")).get()
                if project not in saved_projects:
                    filled_model = filled_form.save(commit=False)
                    filled_model.date = date
                    filled_model.project = project
                    filled_model.save()
                    filled_form.save_m2m()
                else:
                    for saved_project in saved_projects_for_the_day:
                        if saved_project.project == project:
                            saved_project.employee.set(request.POST.getlist("employee"))
                            saved_project.vehicle.set(request.POST.getlist("vehicle"))
                            saved_project.comment = request.POST["comment"]
                            saved_project.save()

                return redirect("date", year, month, day)
            else:
                message = "Invalid form"

    else:
        print(request.GET)
        if "next_day" in request.GET:
            that_day = datetime.date(year, month, day)
            next_day = that_day + datetime.timedelta(1)

            return redirect("date", next_day.year, next_day.month, next_day.day)
        elif "previous_day" in request.GET:
            that_day = datetime.date(year, month, day)
            previous_day = that_day + datetime.timedelta(-1)

            return redirect("date", previous_day.year, previous_day.month, previous_day.day)

    context = {"year_": year, "month_": month, "day_": day, "saved_projects_for_the_day": saved_projects_for_the_day,
               "untouched_projects": untouched_projects, "date_bound_project_form": date_bound_project_form,
                "saved_projects_and_forms": saved_projects_and_forms}
    return render(request=request, template_name="schedule/date.html", context=context)


def get_calendar(year, month):
    assert isinstance(year, int)
    assert isinstance(month, int)

    import calendar

    day_dict = {0: "Hétfő", 1: "Kedd", 2: "Szerda", 3: "Csütörtök", 4: "Péntek", 5: "Szombat", 6: "Vasárnap"}

    c = calendar.Calendar()
    dates = c.monthdatescalendar(year, month)

    for week in dates:
        for i, date in enumerate(week):
            full_date_str = date.strftime("%Y.%m.%d")
            date_str = date.strftime("%m/%d")
            day_int = date.day
            day = day_dict[i]
            month_str = date.strftime("%m")
            month_int = date.month
            year_int = date.year
            month_str_from_int = str(date.month)
            week[i] = [date_str, day, month_str, full_date_str, day_int, month_int, year_int, month_str_from_int]
    return dates
