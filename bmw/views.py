from django.shortcuts import render
from .forms import Length_form, Buildings_form
from .models import BuildingsTKB, BuildingsTU, BuildingsTEM, BuildingsTMO, JelkodVVS, JelkodCCS
from django.contrib.auth.decorators import user_passes_test, login_required

def BMW_group_check(user):
    return user.groups.filter(name='BMW').exists()


@login_required
def home(request):
    return render(request, "bmw/home.html", {})


@login_required
def jelkod(request):
    form = Length_form(request.POST)
    return render(request, "bmw/jelkod.html", {"form": form})


@login_required
def jelkod_ajax(request):
    # ccs and vvs are in request
    if request.GET["ccs"] and request.GET["vvs"]:
        ccs = request.GET["ccs"]
        vvs = request.GET["vvs"]
        #both ccs and vvs are valid
        if JelkodCCS.objects.filter(notation=ccs) and JelkodVVS.objects.filter(notation=vvs):
            ccs_length = JelkodCCS.objects.get(notation=ccs).length
            vvs_length = JelkodVVS.objects.get(notation=vvs).length
            result_str = f"{ccs} - {vvs} = {round(vvs_length-ccs_length, 2)}"
        # ccs and vvs are not valid
        elif not JelkodCCS.objects.filter(notation=ccs) and not JelkodVVS.objects.filter(notation=vvs):
            result_str = "Helytelen CCS és VVS"
        # invalid ccs
        elif not JelkodCCS.objects.filter(notation=ccs):
            result_str = "Helytelen CCS"
        # invalid vvs
        elif not JelkodVVS.objects.filter(notation=vvs):
            result_str = "Helytelen VVS"
        return render(request, "bmw/ajax/jelkod.html",  {"result": result_str})

    # ccs and vvs are not in request
    elif not request.GET["ccs"] and not request.GET["vvs"]:
        result_str = "Hiányzó CCS és VVS"
    # ccs is not in request
    elif not request.GET["ccs"]:
        result_str = "Hiányzó CCS"
    # vvs is not in request
    elif not request.GET["vvs"]:
        result_str = "Hiányzó VVS"
    return render(request, "bmw/ajax/jelkod.html", {"result": result_str})

@login_required
def buildings(request):
    form = Buildings_form()
    return render(request, "bmw/buildings.html", {"form": form})

@login_required
def buildings_ajax(request):
    print(request.GET)
    if request.GET["sorszam"]:
        building = request.GET["building"]
        sorszam = request.GET["sorszam"]
        instance = globals()[f"Buildings{building}"].objects.filter(sorszam=sorszam)
        if instance:
            instance = instance[0]
            szerkezeti_hossz = instance.szerkezeti_hossz
            return_str = f"{sorszam} - {building}: {szerkezeti_hossz}"
        else:
            return_str = "Helytelen sorszám"
    else:
        return_str = "Hiányzó sorszám"
    return render(request, "bmw/ajax/buildings.html", {"result": return_str})
