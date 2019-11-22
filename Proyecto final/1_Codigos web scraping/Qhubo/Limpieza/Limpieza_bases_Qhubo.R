# install.packages("readxl")
# install.packages("tidyverse")
# install.packages("writexl")
library("readxl")
library('tidyverse')
library(writexl)

path = "C:/Users/juan.salgado/Dropbox/Web scraping/Qhubo"
qhubo_raw <- read_excel(paste(path,'/Qhubo_total.xlsx', sep = ""))
qhubo_raw <- subset(qhubo_raw, select = -1)

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
qhubo_uniq <- qhubo_raw %>%
  mutate(Mes = mes_extr(Fecha)) %>%
  mutate(Anio = year_extr(Fecha))

# Generar columna de nombre del medio
qhubo_uniq <- qhubo_uniq %>%
  mutate(Medio = "Qhubo")

# Drop and order columns for panel
qhubo_panel <- subset(qhubo_uniq, select = c(-2, -6))
qhubo_panel <- qhubo_panel %>%
  select(c(Medio, Anio, Mes), everything())

# Change month names

qhubo_panel$Mes[qhubo_panel$Mes == "diciembre"] <- 12
qhubo_panel$Mes[qhubo_panel$Mes == "noviembre"] <- 11
qhubo_panel$Mes[qhubo_panel$Mes == "octubre"] <- 10
qhubo_panel$Mes[qhubo_panel$Mes == "septiembre"] <- 9
qhubo_panel$Mes[qhubo_panel$Mes == "agosto"] <- 8
qhubo_panel$Mes[qhubo_panel$Mes == "julio"] <- 7
qhubo_panel$Mes[qhubo_panel$Mes == "junio"] <- 6
qhubo_panel$Mes[qhubo_panel$Mes == "mayo"] <- 5
qhubo_panel$Mes[qhubo_panel$Mes == "abril"] <- 4
qhubo_panel$Mes[qhubo_panel$Mes == "marzo"] <- 3
qhubo_panel$Mes[qhubo_panel$Mes == "febrero"] <- 2
qhubo_panel$Mes[qhubo_panel$Mes == "enero"] <- 1

# Save database

path2 <- paste(path,'/limpieza/base_limpia', sep = "")
dir.create(path2)
write_xlsx(qhubo_panel,paste0(path2,"/qhubo_panel.xlsx"))
