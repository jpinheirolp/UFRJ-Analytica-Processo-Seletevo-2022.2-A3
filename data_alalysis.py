from operator import index
import pandas as pd
import basedosdados as bd

import numpy as np
import matplotlib.pyplot as plt




df_join = bd.read_sql(
query="SELECT * FROM `basedosdados.br_denatran_frota.municipio_tipo` JOIN `basedosdados.mundo_onu_adh.municipio` ON `basedosdados.br_denatran_frota.municipio_tipo`.`id_municipio` = `basedosdados.mundo_onu_adh.municipio`.`id_municipio` LIMIT 100000",
billing_project_id="587262807117"
)

df_veicles = bd.read_table(dataset_id='br_denatran_frota',
table_id='municipio_tipo',
billing_project_id="587262807117",
limit=10
)

df_social_indicators  = bd.read_table(dataset_id='mundo_onu_adh',
table_id='municipio',
billing_project_id="587262807117",
limit=10
)

df_corr = df_join.corr()

for veicle in df_veicles.columns:
    if not(veicle in df_corr.columns): continue
    for indicator in df_social_indicators.columns:
        if indicator[:3] == 'pop' or indicator[:3] == 'pea' or indicator[:3] == 'pia' : continue
        if not(indicator in df_corr.columns): continue
        corr_value = df_corr.loc[veicle][indicator]
        if abs(corr_value) > 0.3:
            print(veicle, indicator, corr_value)


df_corr.to_csv('correlation.csv')


height = []
bars = []

for veicle in df_veicles.columns:
    if not(veicle in df_corr.columns): continue
    if veicle in ["ano","mes","outros","utilitario"]: continue
    if df_corr.loc[veicle]["prop_ocupados_renda_5_sm"] == np.nan: continue
    height.append(df_corr.loc[veicle]["prop_ocupados_renda_5_sm"] * (-100))
    bars.append(veicle)


y_pos = np.arange(stop=len(bars)*1, step=1)


plt.bar(y_pos, height)


plt.xticks(y_pos, bars, rotation='vertical')


plt.savefig('grafo_barras_coreelacao.png',bbox_inches='tight')

