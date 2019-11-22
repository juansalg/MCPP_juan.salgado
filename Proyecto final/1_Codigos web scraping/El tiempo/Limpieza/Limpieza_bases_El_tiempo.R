# install.packages("readxl")
# install.packages("tidyverse")
# install.packages("writexl")
library("readxl")
library('tidyverse')
library(writexl)

path = "C:/Users/juan.salgado/Dropbox/Web scraping/El tiempo"
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
  mutate(Mes = mes_extr(Fecha)) %>%
  mutate(Anio = year_extr(Fecha))

# Generar columna de nombre del medio
el_tiempo_uniq <- el_tiempo_uniq %>%
  mutate(Medio = "El tiempo")

# Drop and order columns for panel
el_tiempo_panel <- subset(el_tiempo_uniq, select = c(-2, -6))
el_tiempo_panel <- el_tiempo_panel %>%
  select(c(Medio, Anio, Mes), everything())

el_tiempo_panel <- subset(el_tiempo_panel, subset = el_tiempo_panel$Anio != "**Por definir**")

# Change month names

el_tiempo_panel$Mes[el_tiempo_panel$Mes == "diciembre"] <- 12
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "noviembre"] <- 11
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "octubre"] <- 10
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "septiembre"] <- 9
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "agosto"] <- 8
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "julio"] <- 7
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "junio"] <- 6
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "mayo"] <- 5
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "abril"] <- 4
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "marzo"] <- 3
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "febrero"] <- 2
el_tiempo_panel$Mes[el_tiempo_panel$Mes == "enero"] <- 1

# Save database

path2 <- paste(path,'/limpieza/base_limpia', sep = "")
dir.create(path2)
write_xlsx(el_tiempo_panel,paste0(path2,"/el_tiempo_panel.xlsx"))
