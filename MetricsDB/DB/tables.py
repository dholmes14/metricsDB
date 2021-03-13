import django_tables2 as tables

class VariantTable(tables.Table):
    class Meta:
        model = Variant_data
        sequence = (variant_cdna, variant_protein, variant_genome)
