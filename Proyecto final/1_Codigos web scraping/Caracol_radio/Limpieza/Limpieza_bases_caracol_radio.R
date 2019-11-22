# install.packages("readxl")
# install.packages("tidyverse")
# install.packages("writexl")
library("readxl")
library('tidyverse')
library(writexl)


path = "C:/Users/juan.salgado/Dropbox/Web scraping/Caracol_radio"
caracol_radio_raw <- read_excel(paste(path,'/Caracol_radio_articulos_consolidado.xlsx', sep = ""))
caracol_radio_raw <- subset(caracol_radio_raw, select = -1)

# Keep only values in date != 0

caracol_radio_raw <- subset(caracol_radio_raw, 
                         subset = caracol_radio_raw$Fecha != '**Especial**')

# Modificar fecha

  # Funcion que extrae el anio
year_extr <- function(y){
  year <- substr(y, 1, 4)
  return(year)
}

  # Funcion que extrae el mes
mes_extr <- function(m){
  mes <- substr(m, 6, 7)
  return(mes)
}

# Generar columna de mes y de anio
caracol_radio_uniq <- caracol_radio_raw %>%
  mutate(Mes = mes_extr(Fecha)) %>%
  mutate(Anio = year_extr(Fecha))

  # Changing special dates

caracol_radio_uniq$Mes[caracol_radio_uniq$Fecha == "28/02/2011"] <- "02"
caracol_radio_uniq$Mes[caracol_radio_uniq$Fecha == "25/02/2015"] <- "02"

caracol_radio_uniq$Anio[caracol_radio_uniq$Fecha == "28/02/2011"] <- "2011"
caracol_radio_uniq$Anio[caracol_radio_uniq$Fecha == "25/02/2015"] <- "2015"

caracol_radio_uniq$Mes[caracol_radio_uniq$Fecha == "2009/10/29"] <- "09"
caracol_radio_uniq$Mes[caracol_radio_uniq$Fecha == "2009/11/19"] <- "09"

caracol_radio_uniq$Anio[caracol_radio_uniq$Fecha == "2009/10/29"] <- "2015"
caracol_radio_uniq$Anio[caracol_radio_uniq$Fecha == "2009/11/19"] <- "2015"

# Generar columna de nombre del medio
caracol_radio_uniq <- caracol_radio_uniq %>%
  mutate(Medio = "Caracol radio")

# Drop and order columns for panel
caracol_radio_panel <- subset(caracol_radio_uniq, select = c(-2, -6))
caracol_radio_panel <- caracol_radio_panel %>%
  select(c(Medio, Anio, Mes), everything())

# Save database

path2 <- paste(path,'/limpieza/base_limpia', sep = "")
dir.create(path2)
write_xlsx(caracol_radio_panel,paste0(path2,"/caracol_radio_panel.xlsx"))
