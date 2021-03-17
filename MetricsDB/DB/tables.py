import django_tables2 as tables

from .models import Nextseq_Metrics

class Nextseq_Metrics_Table(tables.Table):
    #selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    Pass_fail = tables.Column()
    #Project_No = tables.Column()
    nextseq_project_id = tables.Column()
    Project_No = tables.TemplateColumn('<a href="/projects/{{record.Project_No}}">{{record.Project_No}}</a>')
    class Meta:
        model = Nextseq_Metrics
        row_attrs = { "style": lambda record: "background-color: lightcoral;" if record.Pass_fail =='Fail' else "background-color: white;" }
        template_name="django_tables2/bootstrap-responsive.html"
        sequence = ("Project_No", "description", "instrument", "run_start_date", "run_ID", "instrument", "run_type", "flowcell", "mean_cluster_density", "clusters_PF", "indexed_reads",
        "RT_yield_GB", "demux_yield_GB", "bases_Q30", "raw_demux_yield_ratio", "Pass_fail", "Notes" )
        exclude = ("nextseq_project_id" , )
