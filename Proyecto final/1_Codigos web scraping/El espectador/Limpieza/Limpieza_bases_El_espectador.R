# install.packages("readxl")
# install.packages("tidyverse")
# install.packages("writexl")
library("readxl")
library('tidyverse')
library(writexl)


path = "C:/Users/juan.salgado/Dropbox/Web scraping/El espectador"
el_espectador_raw <- read_excel(paste(path,'/el_espectador_articulos_consolidado.xlsx', sep = ""))
el_espectador_raw <- subset(el_espectador_raw, select = -1)

# Keep only values in date != 0

el_espectador_raw <- subset(el_espectador_raw, 
                            subset = nchar(el_espectador_raw$Fecha) > 2)

# Modificar fecha

  # Funcion que extrae el anio
year_extr <- function(y){
  year <- sub(".* .* (.+)", "\\1", y)
  return(year)
}

  # Funcion que extrae el mes
mes_extr <- function(m){
  mes <- sub(".* (.+) .*", "\\1", m)
  return(mes)
}

# Generar columna de mes y de anio
el_espectador_uniq <- el_espectador_raw %>%
  mutate(Mes = mes_extr(Fecha)) %>%
  mutate(Anio = year_extr(Fecha))

# Generar columna de nombre del medio
el_espectador_uniq <- el_espectador_uniq %>%
  mutate(Medio = "El espectador")

# Drop and order columns for panel
el_espectador_panel <- subset(el_espectador_uniq, select = c(-2, -6))
el_espectador_panel <- el_espectador_panel %>%
  select(c(Medio, Anio, Mes), everything())

# Change month names

el_espectador_panel$Mes[el_espectador_panel$Mes == "Dic"] <- 12
el_espectador_panel$Mes[el_espectador_panel$Mes == "Nov"] <- 11
el_espectador_panel$Mes[el_espectador_panel$Mes == "Oct"] <- 10
el_espectador_panel$Mes[el_espectador_panel$Mes == "Sep"] <- 9
el_espectador_panel$Mes[el_espectador_panel$Mes == "Ago"] <- 8
el_espectador_panel$Mes[el_espectador_panel$Mes == "Jul"] <- 7
el_espectador_panel$Mes[el_espectador_panel$Mes == "Jun"] <- 6
el_espectador_panel$Mes[el_espectador_panel$Mes == "May"] <- 5
el_espectador_panel$Mes[el_espectador_panel$Mes == "Abr"] <- 4
el_espectador_panel$Mes[el_espectador_panel$Mes == "Mar"] <- 3
el_espectador_panel$Mes[el_espectador_panel$Mes == "Feb"] <- 2
el_espectador_panel$Mes[el_espectador_panel$Mes == "Ene"] <- 1

# Save database

path2 <- paste(path,'/limpieza/base_limpia', sep = "")
dir.create(path2)
write_xlsx(el_espectador_panel,paste0(path2,"/el_espectador_panel.xlsx"))
