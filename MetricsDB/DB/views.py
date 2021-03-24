import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from .models import Nextseq_Metrics, HS_Metrics
from .tables import Nextseq_Metrics_Table, HS_Metrics_Table
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
from plotly.offline import plot
from plotly.graph_objs import Scatter
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Sum
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
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    return render(request, 'DB/homepage.html', {'table': table})



def Searchsamplepage(request):
    search_term = ''
    DateSearchQuery = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        queryset = HS_Metrics.objects.filter(Sample__icontains=search_term)
    elif 'date_search' in request.GET:
        DateSearchQuery= request.GET['date_search']
        queryset = HS_Metrics.objects.filter(rundate__icontains=DateSearchQuery)

    else:
        queryset = HS_Metrics.objects.all()

    table = HS_Metrics_Table(queryset)
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    return render(request, 'DB/searchsamplepage.html', {'table': table})
    #return render(request, 'DB/searchsamplepage.html', {'HS_Metrics_data' : HS_Metrics_data, 'search_term': search_term, 'DateSearchQuery': DateSearchQuery })


def Projectpage(request, Project_No):
    Project = get_object_or_404(Nextseq_Metrics, Project_No=Project_No)
    Linked_HS_metrics = HS_Metrics.objects.filter(sequencing_project__exact=Project_No)
    table = HS_Metrics_Table(Linked_HS_metrics)
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1))


    Sample = []
    Percentage_20X_coverage = []
    Fold_80_Base_penalty = []
    mean_bait_coverage = []

    Linked_sample = HS_Metrics.objects.filter(sequencing_project__exact=Project_No)
    for sample in Linked_sample:
        Sample.append(sample.Sample)
        Percentage_20X_coverage.append(sample.PCT_TARGET_BASES_20X)
        Fold_80_Base_penalty.append(sample.FOLD_80_BASE_PENALTY)
        mean_bait_coverage.append(sample.MEAN_BAIT_COVERAGE)



    return render(request, 'DB/projectpage.html', {'table': table, 'Project': Project, 'Sample': Sample, 'Percentage_20X_coverage': Percentage_20X_coverage,
                                                    'Fold_80_Base_penalty': Fold_80_Base_penalty, 'mean_bait_coverage': mean_bait_coverage })


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
