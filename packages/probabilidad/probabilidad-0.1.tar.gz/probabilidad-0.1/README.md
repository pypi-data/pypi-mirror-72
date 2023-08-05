## calculo de probabilidad con distribucion binomial y distribucion de Gauss

para usarlo basta con importar 
```python
from probabilidad import Gaussian, Bionomial
```

luego crear las respectivas varibles haciendo herencia de las classes importandas sea el caso

```python
from probabilidad import Gaussian, Bionomial

#el primer argumento es la media y el segundo es la desviacion estandar
gaussian_primera = Gaussian(20,5)
#metodos
gaussian_primera.calculate_mean() #media
gaussian_primera.calculate_stdev() #estandar desviacion
gaussian_primera.plot_histogram #generar graficos
gaussian_primera.pdf #probabilidad de desidad 
gaussian_primera.plot_histogram_pdf #generar graficos con probabilidad de densidad

gaussian_primera + gaussian_sengunda #suma de desviaciones



#el primer valor representa la probabilidad y el segundo n
bionomial_primero = Bionomial(.24, 28)

bionomial_primero.calculate_mean() # calcula la media
bionomial_primero.calculate_stdev() #calcula la desviacion
bionomial_primero.replace_stats_with_data() #remplace con datos de un fichero txt
bionomial_primero.pdf() #calcula la probabilidad de densidad
bionomial_primero.plot_bar_pdf #hace el grafico
````

pronto se agregaran mas probabilidades..