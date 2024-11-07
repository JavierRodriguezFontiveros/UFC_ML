#--------------------------------------------Bibliotecas------------------------------------------#

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



#----------------------------------------------------------FUNCION--------------------------------------------------------------#

def analizar_correlaciones(df, target, threshold_target=0.7, threshold_predictors=0.7, plot_heatmap=False):
   
    df_numeric = df.select_dtypes(include=[np.number])

    corr_matrix = df_numeric.corr()
    
    # Identificar correlaciones con la variable objetivo
    target_corr_vars = corr_matrix[target].abs()
    target_corr_vars = target_corr_vars[target_corr_vars > threshold_target].index.tolist()
    target_corr_vars.remove(target)
    
    # Identificar pares de variables predictoras con alta correlación
    corr_matrix = corr_matrix.drop(target, axis=0).drop(target, axis=1)
    upper_triangle = np.triu(corr_matrix.abs(), k=1)  # np.triu coge la mitad superior de la matriz para evitar duplicados

    high_corr_pairs = []
    indices = np.where(upper_triangle > threshold_predictors)

    for i, j in zip(*indices):
        high_corr_pairs.append((upper_triangle.index[i], upper_triangle.columns[j]))
    
    print("Con la variable a predecir:", target_corr_vars)
    print("Entre variables predictoras", high_corr_pairs)
    
    if plot_heatmap:
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1);
    
    return target_corr_vars, high_corr_pairs



#---------------------------------------------------------------USO----------------------------------------------------#

target_corr_vars, high_corr_pairs = analizar_correlaciones(df, target='nombre_de_la_variable_objetivo', 
                                                           threshold_target=0.8, 
                                                           threshold_predictors=0.75, 
                                                           plot_heatmap=True)



