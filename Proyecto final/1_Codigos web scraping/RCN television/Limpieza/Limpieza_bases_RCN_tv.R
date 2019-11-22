# install.packages("readxl")
# install.packages("tidyverse")
# install.packages("writexl")
library("readxl")
library('tidyverse')
library(writexl)


path = "C:/Users/juan.salgado/Dropbox/Web scraping/RCN television"
rcn_tv_raw <- read_excel(paste(path,'/RCN_tv_articulos_consolidado.xlsx', sep = ""))
rcn_tv_raw <- subset(rcn_tv_raw, select = -1)

# Keep only values in date != 0

rcn_tv_raw <- subset(rcn_tv_raw, 
                            subset = rcn_tv_raw$Fecha != '**Especial**')

# Modificar fecha

  # Funcion que extrae el anio
year_extr <- function(y){
  year <- substr(y, nchar(y) - 3, nchar(y))
  return(year)
}

  # Funcion que extrae el mes
mes_extr <- function(m){
  mes <- sub(".* (.+) .*", "\\1", m)
  return(mes)
}

# Generar columna de mes y de anio
rcn_tv_uniq <- rcn_tv_raw %>%
  mutate(Mes = mes_extr(Fecha)) %>%
  mutate(Anio = year_extr(Fecha))

# Generar columna de nombre del medio
rcn_tv_uniq <- rcn_tv_uniq %>%
  mutate(Medio = "RCN television")

# Drop and order columns for panel
rcn_tv_panel <- subset(rcn_tv_uniq, select = c(-2, -6))
rcn_tv_panel <- rcn_tv_panel %>%
  select(c(Medio, Anio, Mes), everything())

# Change month names

rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Dic"] <- 12
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Nov"] <- 11
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Oct"] <- 10
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Sep"] <- 9
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Ago"] <- 8
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Jul"] <- 7
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Jun"] <- 6
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "May"] <- 5
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Abr"] <- 4
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Mar"] <- 3
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Feb"] <- 2
rcn_tv_panel$Mes[rcn_tv_panel$Mes == "Ene"] <- 1

# Save database

path2 <- paste(path,'/limpieza/base_limpia', sep = "")
dir.create(path2)
write_xlsx(rcn_tv_panel,paste0(path2,"/rcn_tv_panel.xlsx"))
