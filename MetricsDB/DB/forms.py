from django import forms
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML


list_criteria_population = [('BA1','BA1'), ('BS1', 'BS1'), ('BS2', 'BS2'), ('PM2','PM2'), ('PS4','PS4')]
list_criteria_comp = [('BP4','BP4'),('BP1','BP1'),('BP7','BP7'),('PP3','PP3'),('PM5','PM5'),('PM4','PM4'),('PS1','PS1'),('PVS1','PVS1')]
list_criteria_func = [('BS3','BS3'),('PP2','PP2'),('PM1','PM1'),('PS3','PS3')]
list_criteria_segregation = [('BS4','BS4'),('PP1','PP1')]
list_cliteria_denovo = [('PM6','PM6'),('PS2','PS2')]
list_criteria_allele = [('BP2','BP2'),('PM3','PM3')]
list_criteria_other = [('BP6','BP6'),('PP5','PP5'),('BP5','BP5'),('PP4','PP4')]

list_all_criteria = list_criteria_population + list_criteria_comp + list_criteria_func + list_criteria_segregation + list_cliteria_denovo + list_criteria_allele + list_criteria_other

class InputForm(forms.Form):

    name = forms.CharField(label='Patient name', max_length=200)
    age = forms.IntegerField(label='Patient age', validators=[MinValueValidator(0),MaxValueValidator(120)])
    proband = forms.BooleanField(required=False, label='Proband status')
    affected_relatives = forms.BooleanField(required=False, label='Affected Relatives?')
    stage = forms.ChoiceField(label='Stage', choices=[("Non cancer", "Non cancer"),("1","1"),("2","2"),("3","3")])
    description = forms.CharField(label='Phenotype information', max_length=500)
    sequencer = forms.ChoiceField(label='Sequencer', choices=[("HiSeq", "HiSeq"), ("MiSeq", "MiSeq"), ("NovaSeq", "NovaSeq"),("Other", "Other")])
    gene = forms.CharField(label='Gene', max_length=10)
    chrm = forms.ChoiceField(label='Chromosome', choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10"),("11","11"),("12","12"),("13","13"),("14","14"),("15","15"),("16","16"),("17","17"),("18","18"),("19","19"),("20","20"),("21","21"),("22","22"),("X","X"),("Y","Y")])
    variant_cdna = forms.CharField(label='Variant cDNA', max_length=200)
    variant_protein = forms.CharField(label='Variant Protein', max_length=200)
    variant_genome = forms.CharField(label='Variant genome coordinate', max_length=200)
    code_pathogenicity = forms.ChoiceField(label="Pathogenicity Code", choices=[("Benign","1 : Benign"),("Likely Benign","2 : Likely Benign"),("VOUS","3 : VOUS"),("Likely Pathogenic","4 : Likely Pathogenic"),("Pathogenic","5 : Pathogenic")])
    codes_evidence = forms.MultipleChoiceField(label="ACMG evidence codes",
                                     widget=forms.CheckboxSelectMultiple, choices=list_all_criteria)

