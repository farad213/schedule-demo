from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def admin(request, year=datetime.date.year, month=datetime.date.month):
    cal = get_calendar(year, month)
    context = {"cal": cal}
    return render(request=request, template_name="schedule/admin.html", context=context)


def get_calendar(year, month):
    assert isinstance(year, int)
    assert isinstance(month, int)

    import calendar

    day_dict = {0: "Hétfő", 1: "Kedd", 2: "Szerda", 3: "Csütörtök", 4: "Péntek", 5: "Szombat", 6: "Vasárnap"}

    c = calendar.Calendar()
    dates = c.monthdatescalendar(year, month)

    for week in dates:
        for i, date in enumerate(week):
            date_str = date.strftime("%m/%d")
            day = day_dict[i]
            month = date.strftime("%m")
            week[i] = [date_str, day, month]
    return dates
