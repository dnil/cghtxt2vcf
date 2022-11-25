import click
import logging

LOG = logging.getLogger(__name__)

VCF_HEADER="""##fileformat=VCFv4.1
##source=KGaCGHexport
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=DUP,Description="Duplication">
##ALT=<ID=CNV,Description="Copy Number Variation">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=END,Number=1,Type=String,Description="End of an intra-chromosomal variant">
##INFO=<ID=CLASS,Number=1,Type=String,Description="The classification(usually severity) of the variant">
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Difference in length between REF and ALT alleles">
##FILTER=<ID=PASS,Description="All filters passed">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE"""

@click.command()
@click.option("--txt", help="CGH txt.")
def parse(txt):
    """Parse cgh txt into vcf"""
    txt_file=open(txt)

    click.echo(VCF_HEADER)

    header=next(txt_file)
    fields=header.strip().split('\t')


    for line in txt_file:
        info=dict(zip(fields,line.strip().split('\t')))

        chr = info["Chromosome"]
        start = info["Start"]
        end = info["Stop"]
        if info["Gain/Loss"] == "Gain":
            type = "DUP"
        elif info["Gain/Loss"] == "Loss":
            type = "DEL"
        else:
            type = "CNV"

        if not chr or chr == "?" or not (start or end) or (start == "?" or end == "?"):
            continue

        infotags = f"END={end};SVTYPE={type};SVLEN={int(end)-int(start)+1};CLASS={info['Classification (Initial)']};"
        infotags += ";".join(["=".join( [field.replace(" ", "_").replace("#", "N").replace("(","").replace(")",""), info[field].replace(";", ",")]) for field in fields])

        click.echo("\t".join([chr, start, ".", "N", "<"+type+">", ".", "PASS", infotags, "GT", "./1"]))


if __name__ == '__main__':
    parse()
