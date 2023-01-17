from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Date, Project, DateBoundWithProject, Subproject, Artifact, Profile
from .forms import DateBoundWithProjectForm
import datetime
from django.utils import timezone


def Monitoring_group_check(user):
    return user.groups.filter(name='Schedule - Monitoring').exists() or user.is_superuser


@user_passes_test(Monitoring_group_check)
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
    last_month = datetime.date(year=year, month=month, day=15) - datetime.timedelta(30)
    next_month = datetime.date(year=year, month=month, day=15) + datetime.timedelta(30)
    dates_in_database = Date.objects.filter(date__range=(last_month, next_month))

    # appending Date model object to list
    for week in cal:
        for day in week:
            if Date.objects.filter(date=day[8]):
                date = Date.objects.get(date=day[8])
                day.append(date)


    # updating project status
    for date in dates_in_database:
        if DateBoundWithProject.objects.filter(date=date):
            if date.state == "untouched":
                date.state = "done"
                date.save()
        else:
            date.state = "untouched"
            date.save()

        # if Date has DateBoundWithProject, updating Date with DateBoundWithProject's info
        if DateBoundWithProject.objects.filter(date=date):
            for project in DateBoundWithProject.objects.filter(date=date):
                for week in cal:
                    for day in week:
                        if day[8] == date.date:
                            if len(day) < 11:
                                day.append({})

                            if project.project.hasSubproject():
                                if project.project.project in day[10].keys():
                                    day[10][project.project.project].append(f"{project.subproject.name} - {len(project.profile.all())} cső")
                                else:
                                    day[10].update({project.project.project: [f"{project.subproject.name} - {len(project.profile.all())} cső"]})

                            else:
                                if project.project.project in day[10].keys():
                                    day[10][project.project.project].append(project.comment)
                                else:
                                    day[10].update({project.project.project: [project.comment]})

                            break
                        continue
                    continue


    dates_in_database = [date.__str__() for date in dates_in_database]
    month_str = str(month)
    context = {"cal": cal, "dates_in_database": dates_in_database, "year": year, "month_str": month_str}
    return render(request=request, template_name="schedule/admin.html", context=context)
    # return render(request=request, template_name="schedule/admin.html", context={"cal": cal})


@user_passes_test(Monitoring_group_check)
@login_required
def date(request, year, month, day):
    date = Date.objects.get(date=datetime.date(year, month, day))
    projects = list(Project.objects.all())
    saved_projects_for_the_day = DateBoundWithProject.objects.filter(date=date)
    saved_projects = [saved_project for saved_project in saved_projects_for_the_day]
    untouched_projects = [project for project in projects]

    date_bound_project_form = DateBoundWithProjectForm(date=datetime.date(year, month, day))

    saved_project_forms = [DateBoundWithProjectForm(instance=project, date=datetime.date(year, month, day)) for project
                           in saved_projects_for_the_day]

    saved_projects_and_forms = zip(saved_projects, saved_project_forms)

    if request.method == "POST":

        if "delete" in request.POST:
            # delete a project on that day
            project = Project.objects.filter(project=request.POST.get("delete")).get()
            project_to_delete = DateBoundWithProject.objects.filter(pk=int(request.POST.get("project_id")))
            project_to_delete.delete()
            return redirect("date", year, month, day)

        else:
            project = Project.objects.filter(project=request.POST.get("project_name")).get()
            filled_form = DateBoundWithProjectForm(data=request.POST, date=datetime.date(year, month, day))

            # create a project for that day
            if "untouched" in request.POST:
                # create a project for that day
                filled_model = filled_form.save(commit=False)
                filled_model.date = date
                filled_model.project = project
                filled_model.save()
                filled_form.save_m2m()
            # update a project for that day
            elif "saved" in request.POST:
                for saved_project in saved_projects_for_the_day:
                    if saved_project.id == int(request.POST.get("project_id")):
                        saved_project.employee.set(request.POST.getlist("employee"))
                        saved_project.vehicle.set(request.POST.getlist("vehicle"))
                        saved_project.comment = request.POST["comment"]
                        if "subproject" in request.POST or "artifact" in request.POST or "profile" in request.POST:
                            saved_project.subproject_id = request.POST["subproject"]
                            saved_project.artifact_id = request.POST["artifact"]
                            saved_project.profile.set(request.POST.getlist("profile"))
                        saved_project.save()

            return redirect("date", year, month, day)


    else:
        # changing dates within date.html being handled through GET requests
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


def artifacts(request):
    subproject_id = request.GET.get("subproject")
    artifacts = Artifact.objects.filter(subproject_id=subproject_id)
    context = {"artifacts": artifacts}
    return render(request, "schedule/ajax/artifacts.html", context)


def profiles(request):
    artifact_id = request.GET.get('artifact')
    profiles = Profile.objects.filter(artifact_id=artifact_id)
    context = {'profiles': profiles}
    return render(request, 'schedule/ajax/profiles.html', context)


def partial_save(request):
    project_id = int(request.GET.get("project_id"))
    project = DateBoundWithProject.objects.get(pk=project_id)

    # click on update button(can save profiles, employees, vehicles, comments)
    if not request.GET.get("r_type"):
        print(request.GET)
        project.profile.add(*request.GET.getlist("profile[]"))
        if request.GET.get("employee[]"):
            project.employee.set(request.GET.getlist("employee[]"))
            project.save()
        if request.GET.get("vehicle[]"):
            project.vehicle.set(request.GET.getlist("vehicle[]"))
            project.save()
        if request.GET.get("comment"):
            project.comment = request.GET.get("comment")
            project.save()

    # clicks on add/remove icons
    elif request.GET.get("r_type") == "add or remove":
        id = request.GET.get("id")
        id_list = id.split("_")
        if id_list[0] == "add":
            project.profile.add(id_list[-1])
        elif id_list[0] == "remove":
            project.profile.remove(id_list[-1])

    # building context dict
    artifacts = set()
    subprojects = set()
    for profile in project.profile.all():
        artifacts.add(profile.artifact)
        subprojects.add(profile.artifact.subproject)
    context = {}
    for subproject in subprojects:
        context[subproject] = {}
    for artifact in artifacts:
        context[artifact.subproject].update({artifact: {}})
    for profile in project.profile.all():
        context[profile.artifact.subproject][profile.artifact].update({profile: "active"})
    for artifact in artifacts:
        for profile in artifact.profile_set.all():
            if profile not in context[artifact.subproject][artifact]:
                context[artifact.subproject][artifact].update({profile: "inactive"})
    return render(request, 'schedule/ajax/partial_save.html', context={"context": context})


@user_passes_test(Monitoring_group_check)
@login_required()
def user_calendar(request, year=datetime.date.year, month=datetime.date.month):
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

    user = request.user
    active_days = []
    for week in cal:
        for day in week:
            if Date.objects.filter(date=day[8]):
                date = Date.objects.get(date=day[8])
                projects_for_specific_day = DateBoundWithProject.objects.filter(date=date)
                for project in projects_for_specific_day:
                    if user in project.employee.all():
                        active_days.append(day[3])

    month_str = str(month)
    context = {"cal": cal, "year": year, "month_str": month_str, "active_days": active_days}
    return render(request=request, template_name="schedule/user_calendar.html", context=context)


@user_passes_test(Monitoring_group_check)
@login_required
def user_date(request, year, month, day):
    context_list = []
    user = request.user
    date = Date.objects.get(date=datetime.date(year, month, day))
    projects_for_that_day = DateBoundWithProject.objects.filter(date=date)
    for project in projects_for_that_day:
        if user in project.employee.all():
            project_name = project.project
            vehicles = project.vehicle.all()
            employees = project.employee.all()
            comment = project.comment
            if project.project.hasSubproject():
                # subproject = project.subproject
                # artifact = project.artifact
                # profiles = project.profile.all()
                artifacts = set()
                subprojects = set()
                for profile in project.profile.all():
                    artifacts.add(profile.artifact)
                    subprojects.add(profile.artifact.subproject)
                context = {}
                for subproject in subprojects:
                    context[subproject] = {}
                for artifact in artifacts:
                    context[artifact.subproject].update({artifact: {}})
                for profile in project.profile.all():
                    context[profile.artifact.subproject][profile.artifact].update({profile: "active"})
                for artifact in artifacts:
                    for profile in artifact.profile_set.all():
                        if profile not in context[artifact.subproject][artifact]:
                            context[artifact.subproject][artifact].update({profile: "inactive"})
                mini_context = {"project_name": project_name, "vehicles": vehicles, "employees": employees,
                                "comment": comment, "hasSubproject": context}
            else:
                mini_context = {"project_name": project_name, "vehicles": vehicles, "employees": employees,
                                "comment": comment}
            context_list.append(mini_context)
    context = {"context": context_list, "date": date}
    print(context)

    return render(request=request, template_name="schedule/calendar_date.html", context=context)


@login_required()
def vacation(request):
    dates_when_user_is_on_leave = Date.objects.filter(employees_on_leave=request.user)
    dates_when_user_is_on_leave = [date.date.strftime("%Y-%m-%d") for date in dates_when_user_is_on_leave]
    context = {"dates_when_user_is_on_leave": dates_when_user_is_on_leave}
    return render(request=request, template_name="schedule/vacation.html", context=context)


def vacation_set_ajax(request):
    dates = request.GET.getlist('dates[]')
    dates_when_user_is_on_leave = Date.objects.filter(employees_on_leave=request.user)
    date_objs_when_user_is_on_leave = [date.date for date in dates_when_user_is_on_leave]
    dates_from_calendar = []
    bad_dates_already_working = []
    for date in dates:
        date = date.split("-")
        date_obj = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        if Date.objects.filter(date=date_obj):
            date_db = Date.objects.get(date=date_obj)
            if DateBoundWithProject.objects.filter(date=date_db, employee=request.user):
                bad_dates_already_working.append(date_obj)
                continue

        dates_from_calendar.append(date_obj)
        if date_obj in date_objs_when_user_is_on_leave:
            pass
        else:
            if Date.objects.filter(date=date_obj):
                date_db = Date.objects.get(date=date_obj)
                date_db.employees_on_leave.add(request.user)
    dates_to_delete = [date for date in date_objs_when_user_is_on_leave if date not in dates_from_calendar]
    for date in dates_to_delete:
        Date.objects.get(date=date).employees_on_leave.remove(request.user)

    dates_when_user_is_on_leave = Date.objects.filter(employees_on_leave=request.user)
    dates_when_user_is_on_leave = [date.date.strftime("%Y-%m-%d") for date in dates_when_user_is_on_leave]
    print(bad_dates_already_working, "bad")
    print(dates_when_user_is_on_leave, "good")
    context = {"dates_when_user_is_on_leave": dates_when_user_is_on_leave,
               "bad_dates_already_working": bad_dates_already_working}
    return render(request=request, template_name="schedule/ajax/vacation_ajax.html", context=context)


def get_calendar(year, month):
    assert isinstance(year, int)
    assert isinstance(month, int)

    import calendar

    day_dict = {0: "Hétfő", 1: "Kedd", 2: "Szerda", 3: "Csütörtök", 4: "Péntek", 5: "Szombat", 6: "Vasárnap"}

    c = calendar.Calendar()
    dates = c.monthdatescalendar(year, month)

    for j, week in enumerate(dates):
        for i, date in enumerate(week):
            full_date_str = date.strftime("%Y.%m.%d")
            date_str = date.strftime("%m/%d")
            day_int = date.day
            day = day_dict[i]
            month_str = date.strftime("%m")
            month_int = date.month
            year_int = date.year
            month_str_from_int = str(date.month)
            week[i] = [date_str, day, month_str, full_date_str, day_int, month_int, year_int, month_str_from_int, date]
    return dates
