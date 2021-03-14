from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Nextseq_Metrics(models.Model):
    nextseq_project_id=models.AutoField(primary_key=True, null=False)
    Project_No= models.CharField(max_length=200)
    description= models.CharField(max_length=200)
    run_start_date= models.CharField(max_length=200)
    run_ID= models.CharField(max_length=200)
    instrument= models.CharField(max_length=200)
    run_type= models.CharField(max_length=200)
    flowcell= models.CharField(max_length=200)
    mean_cluster_density= models.FloatField(db_column='mean_cluster_density_(k/mm2)', blank=True)
    clusters_PF= models.FloatField(db_column='percentage_clusters_PF', blank=True)
    RT_yield_GB= models.FloatField(db_column='real-time_yield_(Gb)', blank=True)
    indexed_reads= models.FloatField(db_column='indexed_reads_PF_(M)', blank=True, null=True)
    demux_yield_GB= models.FloatField(db_column='yield_(Gb)', blank=True)
    bases_Q30= models.FloatField(db_column='percentage_bases_>Q30', blank=True)
    raw_demux_yield_ratio= models.FloatField(db_column='raw:demux_yield_ratio', blank=True)
    Pass_fail= models.CharField(max_length=200, blank=True)
    Notes= models.CharField(max_length=300, blank=True)

class HS_Metrics(models.Model):
    HS_Metrics_id=models.AutoField(primary_key=True, null=False)
    Sample = models.CharField(max_length=200, db_column='SAMPLE')
    sample_type=models.CharField(max_length=200, db_column='sample type', blank=True)
    QN_ratio=models.CharField(max_length=200, db_column='Q:N ratio', blank=True)
    sequencing_project=models.CharField(max_length=200, db_column='SEQUENCING PROJECT(S) - orange shading = merged data')
    platform=models.CharField(max_length=200, db_column='Platform')
    rundate=models.CharField(max_length=200, db_column='DATE')
    RAW_NEXTSEQ_READS=models.CharField(max_length=200, db_column='RAW_NEXTSEQ_READS (M)')
    BAIT_SET=models.CharField(max_length=200, db_column='BAIT_SET')
    GENOME_SIZE=models.CharField(max_length=200, db_column='GENOME_SIZE')
    BAIT_TERRITORY=models.CharField(max_length=200, db_column='BAIT_TERRITORY')
    TARGET_TERRITORY=models.CharField(max_length=200, db_column='TARGET_TERRITORY')
    BAIT_DESIGN_EFFICIENCY=models.CharField(max_length=200, db_column='BAIT_DESIGN_EFFICIENCY')
    TOTAL_READS=models.CharField(max_length=200, db_column='TOTAL_READS')
    PF_READS=models.CharField(max_length=200, db_column='PF_READS')
    PF_UNIQUE_READS=models.CharField(max_length=200, db_column='PF_UNIQUE_READS')
    PCT_PF_READS=models.FloatField(db_column='PCT_PF_READS')
    PCT_PF_UQ_READS=models.FloatField(db_column='PCT_PF_UQ_READS')
    PF_UQ_READS_ALIGNED=models.FloatField(db_column='PF_UQ_READS_ALIGNED')
    PCT_PF_UQ_READS_ALIGNED=models.FloatField(db_column='PCT_PF_UQ_READS_ALIGNED')
    PF_BASES_ALIGNED=models.FloatField(db_column='PF_BASES_ALIGNED')
    PF_UQ_BASES_ALIGNED=models.FloatField(db_column='PF_UQ_BASES_ALIGNED')
    ON_BAIT_BASES=models.FloatField(db_column='ON_BAIT_BASES')
    NEAR_BAIT_BASES=models.FloatField(db_column='NEAR_BAIT_BASES')
    OFF_BAIT_BASES=models.FloatField(db_column='OFF_BAIT_BASES')
    ON_TARGET_BASES=models.FloatField(db_column='ON_TARGET_BASES')
    PCT_SELECTED_BASES=models.FloatField(db_column='PCT_SELECTED_BASES (flagged @ <0.6)')
    PCT_OFF_BAIT=models.FloatField(db_column='PCT_OFF_BAIT')
    ON_BAIT_VS_SELECTED=models.FloatField(db_column='ON_BAIT_VS_SELECTED')
    MEAN_BAIT_COVERAGE=models.FloatField(db_column='MEAN_BAIT_COVERAGE (flagged @ <75)')
    MEAN_TARGET_COVERAGE=models.FloatField(db_column='MEAN_TARGET_COVERAGE')
    MEDIAN_TARGET_COVERAGE=models.FloatField(db_column='MEDIAN_TARGET_COVERAGE')
    MAX_TARGET_COVERAGE=models.FloatField(db_column='MAX_TARGET_COVERAGE')
    PCT_USABLE_BASES_ON_BAIT=models.FloatField(db_column='PCT_USABLE_BASES_ON_BAIT')
    PCT_USABLE_BASES_ON_TARGET=models.FloatField(db_column='PCT_USABLE_BASES_ON_TARGET')
    FOLD_ENRICHMENT=models.FloatField(db_column='FOLD_ENRICHMENT')
    ZERO_CVG_TARGETS_PCT=models.FloatField(db_column='ZERO_CVG_TARGETS_PCT')
    PCT_EXC_DUPE=models.FloatField(db_column='PCT_EXC_DUPE')
    PCT_EXC_MAPQ=models.FloatField(db_column='PCT_EXC_MAPQ')
    PCT_EXC_BASEQ=models.FloatField(db_column='PCT_EXC_BASEQ')
    PCT_EXC_OVERLAP=models.FloatField(db_column='PCT_EXC_OVERLAP')
    PCT_EXC_OFF_TARGET=models.FloatField(db_column='PCT_EXC_OFF_TARGET')
    FOLD_80_BASE_PENALTY=models.FloatField(db_column='FOLD_80_BASE_PENALTY (flagged @ >2)')
    PCT_TARGET_BASES_1X=models.FloatField(db_column='PCT_TARGET_BASES_1X')
    PCT_TARGET_BASES_2X=models.FloatField(db_column='PCT_TARGET_BASES_2X')
    PCT_TARGET_BASES_10X=models.FloatField(db_column='PCT_TARGET_BASES_10X')
    PCT_TARGET_BASES_20X=models.FloatField(db_column='PCT_TARGET_BASES_20X (flagged @ <0.98)')
    PCT_TARGET_BASES_30X=models.FloatField(db_column='PCT_TARGET_BASES_30X')
    PCT_TARGET_BASES_40X=models.FloatField(db_column='PCT_TARGET_BASES_40X')
    PCT_TARGET_BASES_50X=models.FloatField(db_column='PCT_TARGET_BASES_50X')
    PCT_TARGET_BASES_100X=models.FloatField(db_column='PCT_TARGET_BASES_100X')
    AT_DROPOUT=models.FloatField(db_column='AT_DROPOUT')
    GC_DROPOUT=models.FloatField(db_column='GC_DROPOUT')
    HET_SNP_SENSITIVITY=models.FloatField(db_column='HET_SNP_SENSITIVITY')
    HET_SNP_Q=models.FloatField(db_column='HET_SNP_Q')




class Patient_data(models.Model):
    patient_id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=200, name='name')
    age = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(120)], name='age')
    proband = models.BooleanField(choices=((True,"Y"),(False,"N")), null=True, name='proband', blank=True)
    affected_relatives = models.BooleanField(choices=((True,"Y"),(False,"N")), null=True, name='affected_relatives', blank=True)
    stage = models.CharField(choices=(("Not cancer", "Not cancer"),("1","1"),("2","2"),("3","3")), name='stage', max_length=20, null=True)
    description = models.CharField(max_length=500, null=True, name='description')


class Variant_data(models.Model):
    variant_id = models.AutoField(primary_key=True, null=False)
    gene = models.CharField(max_length=10, null=True, name='gene', default='BRCA1')
    chrm = models.CharField(null=True, choices=(("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10"),("11","11"),("12","12"),("13","13"),("14","14"),("15","15"),("16","16"),("17","17"),("18","18"),("19","19"),("20","20"),("21","21"),("22","22"),("X","X"),("Y","Y")), max_length=2, name='chrm', default="17")
    variant_cdna = models.CharField(max_length=200, null=True, name='variant_cdna')
    variant_protein = models.CharField(max_length=200, null=True, name='variant_protein')
    variant_genome = models.CharField(blank=False, max_length=200, null=True, name='variant_genome')
    # todo: either one of cDNA and genome coordinate is required input rather than both?


class Test_data(models.Model):
    test_id = models.AutoField(primary_key=True, null=False)
    patient_id = models.ForeignKey(Patient_data, on_delete=models.CASCADE, null=True)
    sequencer = models.CharField(choices=(("HiSeq", "HiSeq"), ("MiSeq", "MiSeq"), ("NovaSeq", "NovaSeq"),("Other", "Other")), max_length=20, null=True, name='sequencer')
    variant_id = models.ForeignKey(Variant_data, on_delete=models.CASCADE, null=True)
    uploaded_time = models.DateTimeField(blank=True, null=True, name="uploaded_time")

class Interpretation_data(models.Model):
    Interpretation_id = models.AutoField(primary_key=True, null=False)
    variant_id = models.ForeignKey(Variant_data, on_delete=models.CASCADE, null=True)
    patient_id = models.ForeignKey(Patient_data, on_delete=models.CASCADE, null=True)
    code_pathogenicity = models.CharField(blank=True, choices=(("1","1"),("2","2"),("3","3"),("4","4"),("5","5")), max_length=1, name="code_pathogenicity")
    codes_evidence = models.CharField(max_length=200, blank=True, name="codes_evidence")
    uploaded_time = models.DateTimeField(blank=True, null=True, name="uploaded_time")
    # todo: reviewed interpretation to be added
