from django.shortcuts import render
from .forms import Length_form, Buildings_form
from .models import BuildingsTKB, BuildingsTU, BuildingsTEM, BuildingsTMO
import pandas as pd



def home(request):
    return render(request, "bmw/home.html", {})


def jelkod(request):

    form = Length_form(request.POST)
    if "ccs" in request.GET and "vvs" in request.GET:
        result = get_result(ccs=request.GET["ccs"], vvs=request.GET["vvs"])
        return render(request, "bmw/jelkod.html", {"form": form, "result": result})

    return render(request, "bmw/jelkod.html", {"form": form})


def buildings(request):

    form = Buildings_form()
    if "sorszam" in request.GET:
        building = request.GET["building"]
        sorszam = request.GET["sorszam"]
        if sorszam:
            form = Buildings_form(initial={"building": building})
            instance = globals()[f"Buildings{building}"].objects.filter(sorszam=sorszam)
            if instance:
                instance = instance[0]
                szerkezeti_hossz = instance.szerkezeti_hossz
                return_str= f"{sorszam} - {building}: {szerkezeti_hossz}"
                return render(request, "bmw/buildings.html", {"form": form, "result": return_str})

    return render(request, "bmw/buildings.html", {"form": form})



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

