# cghtxt2vcf
## Export aCGH txt and convert

```
python main.py --txt data/kg_cgh_pksl.txt > data/kg_cgh_pksl.vcf
grep \# data/kg_cgh_pksl.vcf > data/kg_cgh_pksl.sorted.vcf
grep -v \# data/kg_cgh_pksl.vcf|sort -k1,1 -V -k2,2n -s >> data/kg_cgh_pksl.sorted.vcf
```
