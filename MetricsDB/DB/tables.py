import django_tables2 as tables

from .models import Nextseq_Metrics
from .models import HS_Metrics

class NumberColumn(tables.Column):
    def render(self, value):
        return '{:0.4f}'.format(value)


class Nextseq_Metrics_Table(tables.Table):
    #selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
#    Pass_fail = tables.Column()
    Project_No = tables.TemplateColumn('<a href="/projects/{{record.Project_No}}">{{record.Project_No}}</a>')
    class Meta:
        model = Nextseq_Metrics
        row_attrs = { "style": lambda record: "background-color: lightcoral;" if record.Pass_fail =='Fail' else "background-color: white;" }
        template_name="django_tables2/bootstrap-responsive.html"
        sequence = ("Project_No", "description", "instrument", "run_start_date", "run_ID", "instrument", "run_type", "flowcell", "mean_cluster_density", "clusters_PF", "indexed_reads",
        "RT_yield_GB", "demux_yield_GB", "bases_Q30", "raw_demux_yield_ratio", "Pass_fail", "Notes" )
        exclude = ("nextseq_project_id" , )

class HS_Metrics_Table(tables.Table):
    PCT_TARGET_BASES_20X = NumberColumn()
    sequencing_project = tables.TemplateColumn('<a href="/projects/{{record.sequencing_project}}">{{record.sequencing_project}}</a>')
    class Meta:
        model=HS_Metrics
        row_attrs = { "style": lambda record: "background-color: lightcoral;" if record.PCT_TARGET_BASES_20X =='98' else "background-color: white;" }
        template_name="django_tables2/bootstrap-responsive.html"
        sequence = ("HS_Metrics_id", "Sample", 	"sample_type", 	"QN_ratio", 	"sequencing_project", 	"platform", 	"rundate", 	"RAW_NEXTSEQ_READS", 	"BAIT_SET", 	"GENOME_SIZE", 	"BAIT_TERRITORY", 	"TARGET_TERRITORY", 	"BAIT_DESIGN_EFFICIENCY", 	"TOTAL_READS", 	"PF_READS", 	"PF_UNIQUE_READS", 	"PCT_PF_READS", 	"PCT_PF_UQ_READS", 	"PF_UQ_READS_ALIGNED", 	"PCT_PF_UQ_READS_ALIGNED", 	"PF_BASES_ALIGNED", 	"PF_UQ_BASES_ALIGNED", 	"ON_BAIT_BASES", 	"NEAR_BAIT_BASES", 	"OFF_BAIT_BASES", 	"ON_TARGET_BASES", 	"PCT_SELECTED_BASES", 	"PCT_OFF_BAIT", 	"ON_BAIT_VS_SELECTED", 	"MEAN_BAIT_COVERAGE", 	"MEAN_TARGET_COVERAGE", 	"MEDIAN_TARGET_COVERAGE", 	"MAX_TARGET_COVERAGE", 	"PCT_USABLE_BASES_ON_BAIT", 	"PCT_USABLE_BASES_ON_TARGET", 	"FOLD_ENRICHMENT", 	"ZERO_CVG_TARGETS_PCT", 	"PCT_EXC_DUPE", 	"PCT_EXC_MAPQ", 	"PCT_EXC_BASEQ", 	"PCT_EXC_OVERLAP", 	"PCT_EXC_OFF_TARGET", 	"FOLD_80_BASE_PENALTY", 	"PCT_TARGET_BASES_1X", 	"PCT_TARGET_BASES_2X", 	"PCT_TARGET_BASES_10X", 	"PCT_TARGET_BASES_20X", 	"PCT_TARGET_BASES_30X", 	"PCT_TARGET_BASES_40X", 	"PCT_TARGET_BASES_50X", 	"PCT_TARGET_BASES_100X", 	"AT_DROPOUT", 	"GC_DROPOUT", 	"HET_SNP_SENSITIVITY", 	"HET_SNP_Q"
        )
        exclude = ("HS_Metrics_id" , )
