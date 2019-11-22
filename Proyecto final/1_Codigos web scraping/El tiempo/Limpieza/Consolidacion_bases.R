# install.packages("readxl")
# install.packages("tidyverse")
# install.packages("viridis")
# install.packages("ggsci")
library("ggsci")
library("viridis")
library("readxl")
library('tidyverse')

path = "C:/Users/juan.salgado/Desktop/Proyecto CCB/GIT_Cerac/Web scraping/El tiempo"
el_tiempo_raw <- read_excel(paste(path,'/eltiempo_consolidado.xlsx', sep = ""))
el_tiempo_raw <- subset(el_tiempo_raw, select = -1)

# Seleccionar valores unicos segun el link
el_tiempo_uniq <- el_tiempo_raw %>% distinct(Link, .keep_all = TRUE)
  # Modificar palabra buscada
el_tiempo_uniq$`Palabra buscada`[el_tiempo_uniq$`Palabra buscada` == 'Seguridad'] <-
                      'Seguridad bogotá'
el_tiempo_uniq$`Palabra buscada`[el_tiempo_uniq$`Palabra buscada` == 'Homicidio'] <-
                      'Homicidio bogotá'

# Modificar fecha

  # Funcion que extrae el anio
year_extr <- function(y){
  year <- sub(".* de .* ", "", y)
  return(year)
}
  # Funcion que extrae el mes
mes_extr <- function(m){
  mes <- sub(".*de (.+) .*", "\\1",m)
  return(mes)
}

# Generar columna de mes y de anio
el_tiempo_uniq <- el_tiempo_uniq %>%
  mutate(mes = mes_extr(Fecha)) %>%
  mutate(anio = year_extr(Fecha))

# Collapse by year & palabra_buscada

  # Por Anio
year_count <- data.frame(table(el_tiempo_uniq$anio))
colnames(year_count) <- c('Anio', 'Cantidad de articulos')
tot_art <- sum(year_count$`Cantidad de articulos`)
year_count <- year_count %>%
              mutate(`Proporcion de articulos total (%)` = 
                       round((`Cantidad de articulos` / tot_art)*100, 2))

  # Por palabra buscada
pal_year_count <- count(el_tiempo_uniq, `Palabra buscada`, anio)
colnames(pal_year_count) <- c('Palabra buscada', 'Anio', 'Cantidad de articulos')
  
    # Total palabras por articulo
tot_art_pal <- sum(year_count$`Cantidad de articulos`)

pal_year_count <- pal_year_count %>%
  
    # Generar total articulos por palabra
  group_by(`Palabra buscada`) %>%
  mutate(`Articulos por palabra` = 
           sum(`Cantidad de articulos`)) %>% ungroup() %>%
  
    # Proporcion de articulos sobre el total de articulos por palabra
  mutate(`Proporcion de articulos palabra (%)` = 
           round((`Cantidad de articulos` / `Articulos por palabra`)*100, 2)) %>%
  
    # Proporcion de articulos sobre el total de articulos
  mutate(`Proporcion de articulos total (%)` = 
           round((`Cantidad de articulos` / tot_art)*100, 2))

  # Asignando id para cada palabra
pal_year_count$id <- pal_year_count %>% 
  group_indices(`Palabra buscada`)

  # Dividir pal_year_coun en 3 grupos (para graficar)
grupos = max(pal_year_count$id)
div <- 3
incremento <- round(grupos/div)
inic <- 0
fin <- incremento

  # Sacar los que tienen pocos articulos por palabra
pal_year_count_reduc <- pal_year_count %>%
      filter(`Articulos por palabra` < 4)

pal_year_count_mas_4 <- pal_year_count %>%
  filter(`Articulos por palabra` >= 4)


for (val in 1:div){
  assign(paste0('pal_year_count_', val, sep = ''), pal_year_count_mas_4 %>%
          filter(id <= fin & id > inic))
  inic <- fin
  fin <- 2*fin
}

data_list <- list(pal_year_count_1, pal_year_count_2, pal_year_count_3)

# Grafico num articulos por anio
graph_art_anio <- ggplot(year_count, aes(x = Anio, 
                                         y = `Cantidad de articulos`)) + 
  geom_col() + 
  labs(title = 'Articulos recopilados para El Tiempo', 
       x = 'Año', y = 'Cantidad de articulos') #+ scale_fill_material("lime")

graph_art_anio <- graph_art_anio + theme(
  plot.title = element_text(size=15),
  axis.title.x = element_text(size=12),
  axis.title.y = element_text(size=12)
)

# Grafico num articulos por anio y palabra

  ## Grupo 1
graph_art_anio_pal_1 <- 
         ggplot(pal_year_count_1, aes(x = Anio, 
                                      y = `Cantidad de articulos`)) + 
           geom_col() + 
           labs(title = 'Articulos recopilados para El Tiempo', 
                x = 'Año', y = '')  + 
           facet_wrap(~`Palabra buscada`, scales = "free_x")+ coord_flip()
  
graph_art_anio_pal_1 <-
  graph_art_anio_pal_1 + theme(
           plot.title = element_text(size=15),
           axis.title.x = element_text(size=12),
           axis.title.y = element_text(size=12))

  ## Grupo 2
graph_art_anio_pal_2 <- 
  ggplot(pal_year_count_2, aes(x = Anio, 
                               y = `Cantidad de articulos`)) + 
  geom_col() + 
  labs(title = 'Articulos recopilados para El Tiempo', 
       x = 'Año', y = '')  + 
  facet_wrap(~`Palabra buscada`, scales = "free_x")+ coord_flip()

graph_art_anio_pal_2 <-
  graph_art_anio_pal_2 + theme(
    plot.title = element_text(size=15),
    axis.title.x = element_text(size=12),
    axis.title.y = element_text(size=12))

  ## Grupo 3
graph_art_anio_pal_3 <- 
  ggplot(pal_year_count_3, aes(x = Anio, 
                               y = `Cantidad de articulos`)) + 
  geom_col() + 
  labs(title = 'Articulos recopilados para El Tiempo', 
       x = 'Año', y = '')  + 
  facet_wrap(~`Palabra buscada`, scales = "free_x")+ coord_flip()

graph_art_anio_pal_3 <-
  graph_art_anio_pal_3 + theme(
    plot.title = element_text(size=15),
    axis.title.x = element_text(size=12),
    axis.title.y = element_text(size=12))


graph_art_anio_pal_reduc <- 
  ggplot(pal_year_count_reduc, aes(x = Anio, 
                                   y = `Cantidad de articulos`)) + 
  geom_col() + 
  labs(title = 'Articulos recopilados para El Tiempo', 
       x = 'Año', y = '')  + 
  facet_wrap(~`Palabra buscada`)  + coord_flip()

graph_art_anio_pal_reduc <- graph_art_anio_pal_reduc + theme(
  plot.title = element_text(size=15),
  axis.title.x = element_text(size=12),
  axis.title.y = element_text(size=12)
)

# Grafico num articulos por palabra
art_pal <- cbind('Palabra buscada' = pal_year_count$`Palabra buscada`, 
        'Articulos por palabra' = pal_year_count$`Articulos por palabra`)
art_pal <- as.data.frame(unique(art_pal))
art_pal$`Articulos por palabra` <- 
  as.numeric(as.character(art_pal$`Articulos por palabra`))


graph_art_pal <- ggplot(art_pal, aes(x = reorder(`Palabra buscada`, -`Articulos por palabra`) , 
                            y = `Articulos por palabra`)) + 
  geom_col() + 
  labs(title = 'Articulos recopilados para El Tiempo', 
       x = '', y = '') + coord_flip()

graph_art_pal <- graph_art_pal + theme(
  plot.title = element_text(size=15),
  axis.title.x = element_text(size=12),
  axis.title.y = element_text(size=12)
)

path = "C:/Users/juan.salgado/Desktop/Proyecto CCB/GIT_Cerac/Web scraping/El tiempo/Limpieza/outputs/"
setwd(path)

pdf(paste(path, 'graphs_el_tiempo.pdf', sep = ''))
print(graph_art_anio)
print(graph_art_pal)
print(graph_art_anio_pal_1)
print(graph_art_anio_pal_2)
print(graph_art_anio_pal_3)
print(graph_art_anio_pal_reduc)
dev.off()
  