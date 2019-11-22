# install.packages("readxl")
# install.packages("tidyverse")
# install.packages("writexl")
library("readxl")
library('tidyverse')
library(writexl)


path = "C:/Users/juan.salgado/Dropbox/Web scraping/Caracol_television"
caracol_tv_raw <- read_excel(paste(path,'/Caracol_tv_articulos_consolidado.xlsx', sep = ""))
caracol_tv_raw <- subset(caracol_tv_raw, select = -1)

# Keep only values in date != 0

caracol_tv_raw <- subset(caracol_tv_raw, 
                            subset = caracol_tv_raw$Fecha != '**Especial**')

# Modificar fecha

  # Funcion que extrae el anio
year_extr <- function(y){
  year <- substr(y, nchar(y) - 3, nchar(y))
  return(year)
}

  # Funcion que extrae el mes
mes_extr <- function(m){
  mes <- sub(".* de (.+) de .*", "\\1", m)
  return(mes)
}

# Generar columna de mes y de anio
caracol_tv_uniq <- caracol_tv_raw %>%
  mutate(Mes = mes_extr(Fecha)) %>%
  mutate(Anio = year_extr(Fecha))

# Generar columna de nombre del medio
caracol_tv_uniq <- caracol_tv_uniq %>%
  mutate(Medio = "Caracol television")

# Drop and order columns for panel
caracol_tv_panel <- subset(caracol_tv_uniq, select = c(-2, -6))
caracol_tv_panel <- caracol_tv_panel %>%
  select(c(Medio, Anio, Mes), everything())

# Change month names

caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Diciembre"] <- 12
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Noviembre"] <- 11
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Octubre"] <- 10
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Septiembre"] <- 9
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Agosto"] <- 8
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Julio"] <- 7
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Junio"] <- 6
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Mayo"] <- 5
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Abril"] <- 4
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Marzo"] <- 3
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Febrero"] <- 2
caracol_tv_panel$Mes[caracol_tv_panel$Mes == "Enero"] <- 1

# Save database

path2 <- paste(path,'/limpieza/base_limpia', sep = "")
dir.create(path2)
write_xlsx(caracol_tv_panel,paste0(path2,"/caracol_tv_panel.xlsx"))
