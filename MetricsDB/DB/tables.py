import django_tables2 as tables

from .models import Nextseq_Metrics

class Nextseq_Metrics_Table(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    Project_No = tables.Column(attrs={"tf": {"bgcolor": "red"}})
    class Meta:
        model = Nextseq_Metrics
        
        template_name="django_tables2/bootstrap-responsive.html"
        sequence = ("selection", "Project_No", "instrument", "run_start_date", "run_ID", "instrument", "run_type", "flowcell", "mean_cluster_density", "clusters_PF", "indexed_reads",
        "RT_yield_GB", "demux_yield_GB", "bases_Q30", "raw_demux_yield_ratio", "Pass_fail", "Notes" )
