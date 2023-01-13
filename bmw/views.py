from django.shortcuts import render
from .forms import Length_form, Buildings_form
from .models import BuildingsTKB, BuildingsTU, BuildingsTEM, BuildingsTMO, JelkodVVS, JelkodCCS
import pandas as pd
from django.contrib.auth.decorators import user_passes_test, login_required
import os

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

#NOT VIEWS

def get_length(to_check, type=None):
    df = load_file()
    assert type in ["ccs", "vvs"]
    assert isinstance(to_check, str)

    index = df[f"{type} notation"][df[f"{type} notation"] == to_check].index
    result = df[f"{type} length"][index].values
    if list(result):
        return result[0]
    return f"Notation not found in {type} column"


def get_result(ccs, vvs):
    error_msg = ""
    ccs.strip()
    ccs_length = get_length(ccs, type="ccs")
    if isinstance(ccs_length, str):
        error_msg += "Invalid CCS "

    vvs.strip()
    vvs_length = get_length(vvs, type="vvs")
    if isinstance(vvs_length, str):
        error_msg += "Invalid VVS"

    if error_msg:
        return error_msg
    result = round(vvs_length - ccs_length, 2)
    return f"{ccs} - {vvs} = {result}"


def load_file():
    """Excel file has to be named 'BMW.xlsx'
    if there is a new sheet, make sure to update 'sheet_name' in code (line 6)"""

    file_dir = os.path.join(os.path.dirname(__file__), "BMW.xlsx")
    df = pd.read_excel(file_dir, sheet_name="2022.07.29.", header=1, usecols=[4, 5, 7, 8],
                       names=["ccs notation", "ccs length", "vvs notation", "vvs length"])
    return df

