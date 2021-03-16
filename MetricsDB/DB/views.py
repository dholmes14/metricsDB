import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from .forms import InputForm
from .models import Patient_data, Variant_data, Test_data, Interpretation_data, Nextseq_Metrics, HS_Metrics
from .tables import Nextseq_Metrics_Table
from django.shortcuts import render
from django.views.generic import ListView
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML
from django.contrib.auth.models import User
from tablib import Dataset
from django.http import HttpResponseRedirect
import csv
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2 import RequestConfig
# Create your views here.


def Homepage(request):
    search_term = ''
    DateSearchQuery = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        queryset = Nextseq_Metrics.objects.filter(Project_No__icontains=search_term)
    elif 'date_search' in request.GET:
        DateSearchQuery= request.GET['date_search']
        queryset = Nextseq_Metrics.objects.filter(run_start_date__icontains=DateSearchQuery)
    else:
        queryset = Nextseq_Metrics.objects.all()
    table = Nextseq_Metrics_Table(queryset)
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    RequestConfig(request).configure(table)
    return render(request, 'DB/homepage.html', {'table': table})



def Searchsamplepage(request):
    search_term = ''
    DateSearchQuery = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        HS_Metrics_data = HS_Metrics.objects.filter(Sample__icontains=search_term)
    elif 'date_search' in request.GET:
        DateSearchQuery= request.GET['date_search']
        HS_Metrics_data = HS_Metrics.objects.filter(rundate__icontains=DateSearchQuery)

    else:
        HS_Metrics_data = HS_Metrics.objects.all()

    return render(request, 'DB/searchsamplepage.html', {'HS_Metrics_data' : HS_Metrics_data, 'search_term': search_term, 'DateSearchQuery': DateSearchQuery })

def Variantpage(request, variant_id):

    Variant = get_object_or_404(Variant_data, variant_id=variant_id)

    Interpretations = Interpretation_data.objects.filter(variant_id__exact=variant_id)

    context = {

    'Variant': Variant,
    'Interpretations' : Interpretations,
    }

    return render(request, 'DB/variantpage.html', context)

def Projectpage(request, Project_No):
    Project = get_object_or_404(Nextseq_Metrics, Project_No=Project_No)

    Linked_HS_metrics = HS_Metrics.objects.filter(sequencing_project__exact=Project_No)

    context = {
    'Project': Project,
    'Linked_HS_metrics': Linked_HS_metrics
    }
    return render(request, 'DB/projectpage.html', context)



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

            project, creation = Nextseq_Metrics.objects.get_or_create(
            Project_No = row['Project_No'],
            description= row['description'],
            run_start_date= row['run_start_date'],
            run_ID= row['run_ID'],
            instrument= row['instrument'],
            run_type= row['run_type'],
            flowcell= row['flowcell'],
            mean_cluster_density= row['mean_cluster_density_(k/mm2)'] or '0',
            clusters_PF= row['percentage_clusters_PF'] or '0',
            RT_yield_GB= row['real-time_yield_(Gb)'] or '0',
            indexed_reads= row['indexed_reads_PF_(M)'] or '0',
            demux_yield_GB= row['demux_yield_(Gb)'] or '0',
            bases_Q30= row['percentage_bases_>Q30'] or '0',
            raw_demux_yield_ratio= row['raw:demux_yield_ratio'] or '0',
            Pass_fail= row['Pass/fail'],
            Notes= row['Notes']
    )

    return render(request, 'DB/bulkinputpage.html')

def HS_metrics_inputpage(request):
    if request.method == 'POST':
        file = request.FILES['HS_metrics_file']
        uploaded_file = request.POST.get('file')
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            print(row)


            project, creation = HS_Metrics.objects.get_or_create(
            Sample = row['SAMPLE'],
            sample_type=row['sample type'],
            QN_ratio=row['Q:N ratio'],
            sequencing_project=row['SEQUENCING PROJECT(S) - orange shading = merged data'],
            platform=row['Platform'],
            rundate=row['DATE'],
            RAW_NEXTSEQ_READS=row['RAW_NEXTSEQ_READS (M)'],
            BAIT_SET=row['BAIT_SET'],
            GENOME_SIZE=row['GENOME_SIZE'],
            BAIT_TERRITORY=row['BAIT_TERRITORY'],
            TARGET_TERRITORY=row['TARGET_TERRITORY'],
            BAIT_DESIGN_EFFICIENCY=row['BAIT_DESIGN_EFFICIENCY'],
            TOTAL_READS=row['TOTAL_READS'],
            PF_READS=row['PF_READS'],
            PF_UNIQUE_READS=row['PF_UNIQUE_READS'],
            PCT_PF_READS=row['PCT_PF_READS'],
            PCT_PF_UQ_READS=row['PCT_PF_UQ_READS'],
            PF_UQ_READS_ALIGNED=row['PF_UQ_READS_ALIGNED'],
            PCT_PF_UQ_READS_ALIGNED=row['PCT_PF_UQ_READS_ALIGNED'],
            PF_BASES_ALIGNED=row['PF_BASES_ALIGNED'],
            PF_UQ_BASES_ALIGNED=row['PF_UQ_BASES_ALIGNED'],
            ON_BAIT_BASES=row['ON_BAIT_BASES'],
            NEAR_BAIT_BASES=row['NEAR_BAIT_BASES'],
            OFF_BAIT_BASES=row['OFF_BAIT_BASES'],
            ON_TARGET_BASES=row['ON_TARGET_BASES'],
            PCT_SELECTED_BASES=row['PCT_SELECTED_BASES (flagged @ <0.6)'],
            PCT_OFF_BAIT=row['PCT_OFF_BAIT'],
            ON_BAIT_VS_SELECTED=row['ON_BAIT_VS_SELECTED'],
            MEAN_BAIT_COVERAGE=row['MEAN_BAIT_COVERAGE (flagged @ <75)'],
            MEAN_TARGET_COVERAGE=row['MEAN_TARGET_COVERAGE'],
            MEDIAN_TARGET_COVERAGE=row['MEDIAN_TARGET_COVERAGE'],
            MAX_TARGET_COVERAGE=row['MAX_TARGET_COVERAGE'],
            PCT_USABLE_BASES_ON_BAIT=row['PCT_USABLE_BASES_ON_BAIT'],
            PCT_USABLE_BASES_ON_TARGET=row['PCT_USABLE_BASES_ON_TARGET'],
            FOLD_ENRICHMENT=row['FOLD_ENRICHMENT'],
            ZERO_CVG_TARGETS_PCT=row['ZERO_CVG_TARGETS_PCT'],
            PCT_EXC_DUPE=row['PCT_EXC_DUPE'],
            PCT_EXC_MAPQ=row['PCT_EXC_MAPQ'],
            PCT_EXC_BASEQ=row['PCT_EXC_BASEQ'],
            PCT_EXC_OVERLAP=row['PCT_EXC_OVERLAP'],
            PCT_EXC_OFF_TARGET=row['PCT_EXC_OFF_TARGET'],
            FOLD_80_BASE_PENALTY=row['FOLD_80_BASE_PENALTY (flagged @ >2)'],
            PCT_TARGET_BASES_1X=row['PCT_TARGET_BASES_1X'],
            PCT_TARGET_BASES_2X=row['PCT_TARGET_BASES_2X'],
            PCT_TARGET_BASES_10X=row['PCT_TARGET_BASES_10X'],
            PCT_TARGET_BASES_20X=row['PCT_TARGET_BASES_20X (flagged @ <0.98)'],
            PCT_TARGET_BASES_30X=row['PCT_TARGET_BASES_30X'],
            PCT_TARGET_BASES_40X=row['PCT_TARGET_BASES_40X'],
            PCT_TARGET_BASES_50X=row['PCT_TARGET_BASES_50X'],
            PCT_TARGET_BASES_100X=row['PCT_TARGET_BASES_100X'],
            AT_DROPOUT=row['AT_DROPOUT'],
            GC_DROPOUT=row['GC_DROPOUT'],
            HET_SNP_SENSITIVITY=row['HET_SNP_SENSITIVITY'],
            HET_SNP_Q=row['HET_SNP_Q']
    )

    return render(request, 'DB/HS_metrics_inputpage.html')
