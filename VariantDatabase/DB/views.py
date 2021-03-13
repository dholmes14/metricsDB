import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from .forms import InputForm
from .models import Patient_data, Variant_data, Test_data, Interpretation_data
from django.shortcuts import render
from django.views.generic import ListView
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML
from django.contrib.auth.models import User
from tablib import Dataset
from django.http import HttpResponseRedirect
import csv
# Create your views here.

def Homepage(request):
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        Variants = Variant_data.objects.filter(gene__icontains=search_term)
    else:
        Variants = Variant_data.objects.all()

    return render(request, 'DB/homepage.html', {'Variants' : Variants, 'search_term': search_term })

def Variantpage(request, variant_id):

    Variant = get_object_or_404(Variant_data, variant_id=variant_id)

    Interpretations = Interpretation_data.objects.filter(variant_id__exact=variant_id)

    context = {

    'Variant': Variant,
    'Interpretations' : Interpretations,
    }

    return render(request, 'DB/variantpage.html', context)


def Datainputpage(request):


    if request.method == 'POST':

        form = InputForm(request.POST)

        if form.is_valid():

            patient, creation = Patient_data.objects.get_or_create(
                name = form.cleaned_data['name'],
                age = form.cleaned_data['age'],
                proband = form.cleaned_data['proband'],
                stage = form.cleaned_data['stage'],
                description = form.cleaned_data['description']
            )

            variant, creation = Variant_data.objects.get_or_create(
                gene = form.cleaned_data['gene'],
                chrm = form.cleaned_data['chrm'],
                variant_cdna = form.cleaned_data['variant_cdna'],
                variant_protein = form.cleaned_data['variant_protein'],
                variant_genome = form.cleaned_data['variant_genome']
            )

            test, creation = Test_data.objects.get_or_create(
                patient_id = patient,
                sequencer = form.cleaned_data['sequencer'],
                variant_id = variant,
                uploaded_time = datetime.datetime.now()
            )

            interpretation, creation = Interpretation_data.objects.get_or_create(
                variant_id = variant,
                patient_id = patient,
                code_pathogenicity = form.cleaned_data['code_pathogenicity'],
                codes_evidence = str(form.cleaned_data['codes_evidence']).replace("'",""),
                uploaded_time = datetime.datetime.now()
            )

            return redirect('Variantpage', variant_id=variant.variant_id)
    else:
       form = InputForm()

    return render(request, 'DB/datainputpage.html', {'form' : form})

def Bulkinputpage(request):
    if request.method == 'POST':
        file = request.FILES['myfile']
        uploaded_file = request.POST.get('file')
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            print(row)

            patient, creation = Patient_data.objects.get_or_create(
            name = row['Name'],
            age = row['Age'],
            proband = str(row['Proband']).replace("Y","True").replace("N", "False"),
            affected_relatives = str(row['Affected Relatives']).replace("Y","True").replace("N", "False"),
            stage = row['Stage'],
            description = row['Description']
            )

            variant, creation = Variant_data.objects.get_or_create(
            variant_cdna = row['Variant cDNA'],
            variant_protein = row['Variant Protein'],
            variant_genome = row['Variant Genome']
            )

            test, creation = Test_data.objects.get_or_create(
            patient_id = patient,
            sequencer = row['Sequencer'],
            variant_id = variant,
            uploaded_time = datetime.datetime.now()
            )

            interpretation, creation = Interpretation_data.objects.get_or_create(
                variant_id = variant,
                patient_id = patient,
                code_pathogenicity = row['Pathogenicity Code'].replace("1","Benign").replace("2","Likely Benign").replace("3","VOUS").replace("4","Likely Pathogenic").replace("5","Pathogenic"),
                codes_evidence = str(row['Evidence Codes']).replace("'",""),
                uploaded_time = datetime.datetime.now()
            )

    return render(request, 'DB/bulkinputpage.html')



class SearchView(ListView):
    model = Variant_data
    template_name = 'homepage.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('search')
       if query:
          postresult = Variant_data.objects.filter(title__contains=query)
          result = postresult
       else:
           result = None
       return result
