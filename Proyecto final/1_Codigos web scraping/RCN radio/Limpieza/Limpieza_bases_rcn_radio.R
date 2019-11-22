# install.packages("readxl")
# install.packages("tidyverse")
# install.packages("writexl")
library("readxl")
library('tidyverse')
library(writexl)


path = "C:/Users/juan.salgado/Dropbox/Web scraping/RCN radio"
rcn_radio_raw <- read_excel(paste(path,'/RCN_radio_articulos_consolidado.xlsx', sep = ""))
rcn_radio_raw <- subset(rcn_radio_raw, select = -1)

# Keep only values in date != 0

rcn_radio_uniq <- subset(rcn_radio_raw, 
                            subset = rcn_radio_raw$Fecha != '**Especial**')

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
rcn_radio_uniq <- rcn_radio_uniq %>%
  mutate(Mes = mes_extr(Fecha)) %>%
  mutate(Anio = year_extr(Fecha))

# Generar columna de nombre del medio
rcn_radio_uniq <- rcn_radio_uniq %>%
  mutate(Medio = "RCN radio")

# Drop and order columns for panel
rcn_radio_panel <- subset(rcn_radio_uniq, select = c(-2, -6))
rcn_radio_panel <- rcn_radio_panel %>%
  select(c(Medio, Anio, Mes), everything())

# Change month names

rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Dic"] <- 12
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Nov"] <- 11
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Oct"] <- 10
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Sep"] <- 9
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Ago"] <- 8
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Jul"] <- 7
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Jun"] <- 6
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Mayo"] <- 5
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Abr"] <- 4
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Mar"] <- 3
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Feb"] <- 2
rcn_radio_panel$Mes[rcn_radio_panel$Mes == "Ene"] <- 1

# Save database

path2 <- paste(path,'/limpieza/base_limpia', sep = "")
dir.create(path2)
write_xlsx(rcn_radio_panel,paste0(path2,"/rcn_radio_panel.xlsx"))
