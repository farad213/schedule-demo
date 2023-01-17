from django.shortcuts import render
from .forms import Length_form, Buildings_form, QuickReportForm
from .models import JelkodVVS, JelkodCCS, Technician, Customer, BuildingsTU, BuildingsTMO, BuildingsTEM, BuildingsTKB
from django.contrib.auth.decorators import user_passes_test, login_required
import datetime, shutil, os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from django.http import FileResponse
from concurrent.futures import ThreadPoolExecutor, wait


def BMW_group_check(user):
    return user.groups.filter(name='BMW').exists()


@login_required
def home(request):
    return render(request, "bmw/home.html", {})


@login_required
@user_passes_test(BMW_group_check)
def jelkod(request):
    form = Length_form(request.POST)
    return render(request, "bmw/jelkod.html", {"form": form})


@login_required
def jelkod_ajax(request):
    # ccs and vvs are in request
    if request.GET["ccs"] and request.GET["vvs"]:
        ccs = request.GET["ccs"]
        vvs = request.GET["vvs"]
        # both ccs and vvs are valid
        if JelkodCCS.objects.filter(notation=ccs) and JelkodVVS.objects.filter(notation=vvs):
            ccs_length = JelkodCCS.objects.get(notation=ccs).length
            vvs_length = JelkodVVS.objects.get(notation=vvs).length
            result_str = f"{ccs} - {vvs} = {round(vvs_length - ccs_length, 2)}"
        # ccs and vvs are not valid
        elif not JelkodCCS.objects.filter(notation=ccs) and not JelkodVVS.objects.filter(notation=vvs):
            result_str = "Helytelen CCS és VVS"
        # invalid ccs
        elif not JelkodCCS.objects.filter(notation=ccs):
            result_str = "Helytelen CCS"
        # invalid vvs
        elif not JelkodVVS.objects.filter(notation=vvs):
            result_str = "Helytelen VVS"
        return render(request, "bmw/ajax/jelkod.html", {"result": result_str})

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
@user_passes_test(BMW_group_check)
def buildings(request):
    form = Buildings_form()
    return render(request, "bmw/buildings.html", {"form": form})


@login_required()
def buildings_ajax(request):
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

@login_required
@user_passes_test(BMW_group_check)
def quickreport(request):

    form = QuickReportForm()
    context = {"form": form}
    if request.method == "GET":
        if "quickreport" in request.GET:

            directory = 'bmw/download'
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

            print(request.GET)
            language = request.GET["language"]
            customer = request.GET["customer"]
            technician = request.GET["technician"]
            technician_obj = Technician.objects.get(pk=technician)
            customer_obj = Customer.objects.get(pk=customer)
            profile_from = request.GET.getlist("profile_from")
            profile_to = request.GET.getlist("profile_to")
            profile_pairs = list(zip(profile_from, profile_to))
            profiles_sorted = []
            for profile_pair in profile_pairs:
                if profile_pair[0].isnumeric() and profile_pair[1].isnumeric():
                    profile_pair = tuple(int(profile) for profile in profile_pair)
                    profile_pair = [min(profile_pair), max(profile_pair)]
                else:
                    profile_pair = list(reversed([min(profile_pair), max(profile_pair)]))
                profiles_sorted.append(profile_pair)

            if request.GET["building"] == "Other":
                building = request.GET["custom_building"]
            else:
                building = request.GET["building"]

            context = {"company": customer_obj.company,
                       "customer": customer_obj.name,
                       "address_street": customer_obj.address_1,
                       "address_town": customer_obj.address_2,
                       "measurement_date": request.GET["date_of_measurement"].replace("-", "."),
                       "building": building,
                       "technician": technician_obj.name,
                       "technician_tel": technician_obj.phone_no,
                       "technician_email": technician_obj.email,
                       "date": datetime.date.today().strftime("%Y.%m.%d"),
                       "comment": request.GET["comment"]}

            if language == "HU":
                template = DocxTemplate("bmw/quickreport/HU_template.docx")
                technician_signature = InlineImage(template, technician_obj.signature, width=Mm(30))
                profiles_text = []
                profiles_counter = 0
                for profiles in profiles_sorted:
                    if profiles[0] == "" and profiles[1] == "":
                        continue
                    elif profiles[1] == "":
                        profiles_text.append(f"P{profiles[0]} számú cölöp")
                        profiles_counter += 1
                    else:
                        profiles_text.append(f"P{profiles[0]} - P{profiles[1]} számú cölöpök")
                        profiles_counter += int(profiles[1]) - int(profiles[0]) + 1

                context.update({"technician_signature": technician_signature,
                                "title": customer_obj.position_HU,
                                "profiles": profiles_text,
                                "no_of_profiles": profiles_counter,
                                "technician_title": technician_obj.position_HU})
                template.render(context)
                file_name = f"FCH-20091_SIT_Debrecen_BMW - {context['building']}_{context['measurement_date'].replace('.', '')}_HBM_quickreport_{language}.docx"
                path = f"bmw/download/{file_name}"
                executor = ThreadPoolExecutor()
                save_future = executor.submit(template.save, path)
                wait([save_future])
                file = open(path, "rb")
                response = FileResponse(file)
                response['Content-Disposition'] = f'attachment; filename="{file_name}.docx"'
                return response


            elif language == "EN":
                template = DocxTemplate("bmw/quickreport/EN_template.docx")
                technician_signature = InlineImage(template, technician_obj.signature, width=Mm(30))
                profiles_text = []
                profiles_counter = 0
                for profiles in profiles_sorted:
                    if profiles[0] == "" and profiles[1] == "":
                        continue
                    elif profiles[1] == "":
                        profiles_text.append(f"Pile No. P{profiles[0]}")
                        profiles_counter += 1
                    else:
                        profiles_text.append(f"Pile No. P{profiles[0]} - P{profiles[1]}")
                        profiles_counter += int(profiles[1]) - int(profiles[0]) + 1

                context.update({"technician_signature": technician_signature,
                                "title": customer_obj.position_EN,
                                "profiles": profiles_text,
                                "no_of_profiles": profiles_counter,
                                "technician_title": technician_obj.position_EN})
                template.render(context)
                file_name = f"FCH-20091_SIT_Debrecen_BMW - {context['building']}_{context['measurement_date'].replace('.', '')}_HBM_quickreport_{language}.docx"
                path = f"bmw/download/{file_name}"
                executor = ThreadPoolExecutor()
                save_future = executor.submit(template.save, path)
                wait([save_future])
                file = open(path, "rb")
                response = FileResponse(file)
                response['Content-Disposition'] = f'attachment; filename="{file_name}.docx"'
                return response



    return render(request, "bmw/quickreport.html", context)
