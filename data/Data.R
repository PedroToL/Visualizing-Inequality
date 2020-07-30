library(tidyverse)

# bases
df = read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/CONCURSO VISUALIZACION DESIGUALDAD.csv", 
              col_types = cols(anio_c = col_integer(), 
                               sexo_ci = col_factor(levels = c("Hombre", 
                                                               "Mujer"))), 
              trim_ws = FALSE)

ARG_ <- read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/bases/ARG .csv",
                 col_types = cols(anio_c = col_integer(), 
                                  sexo_ci = col_factor(levels = c("Hombre", 
                                                                  "Mujer"))),
                 trim_ws = FALSE)

BOL_ <- read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/bases/BOL .csv", 
                 col_types = cols(anio_c = col_integer(), 
                                  sexo_ci = col_factor(levels = c("Hombre", 
                                                                  "Mujer"))),
                 trim_ws = FALSE)

BRA_ <- read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/BRA .csv",
                 col_types = cols(anio_c = col_integer(), 
                                  sexo_ci = col_factor(levels = c("Hombre", 
                                                                  "Mujer"))),
                 trim_ws = FALSE)

CHL_ <- read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/CHL .csv",
                 col_types = cols(anio_c = col_integer(), 
                                  sexo_ci = col_factor(levels = c("Hombre", 
                                                                  "Mujer"))),
                 trim_ws = FALSE)

PER_ <- read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/PER .csv",
                 col_types = cols(anio_c = col_integer(), 
                                  sexo_ci = col_factor(levels = c("Hombre", 
                                                                  "Mujer"))),
                 trim_ws = FALSE)

PRY_ <- read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/PRY .csv",
                 col_types = cols(anio_c = col_integer(), 
                                  sexo_ci = col_factor(levels = c("Hombre", 
                                                                  "Mujer"))),
                 trim_ws = FALSE)



#2018
'2018' = df %>% filter(anio_c == 2018)
Chile = CHL_ %>% filter(anio_c == 2017)
`2018` = rbind(`2018`, Chile[-1])

#2010
'2010' = df %>% filter(anio_c == 2010)
Brasil =  BRA_ %>% filter(anio_c == 2009)
Bolivia = BOL_ %>% filter(anio_c == 2009)
Chile = CHL_ %>% filter(anio_c == 2009)
`2010` = rbind(`2010`, Brasil[-1], Chile[-1], Bolivia[-1])

#2000
'2000' = df %>% filter(anio_c == 2000)
Brasil =  BRA_ %>% filter(anio_c == 2001)
Bolivia = BOL_ %>% filter(anio_c == 2000)
Paraguay = PRY_ %>% filter(anio_c == 2001)
`2000` = rbind(`2000`, Brasil[-1], Paraguay[-1], Bolivia[-1])

pag3 = rbind(`2000`, `2010`, `2018`)
pag3$anio_c = replace(pag3$anio_c, pag3$anio_c == 2001, 2000L)
pag3$anio_c = replace(pag3$anio_c, pag3$anio_c == 2009, 2010L)
pag3$anio_c = replace(pag3$anio_c, pag3$anio_c == 2017, 2018L)


pag3 = as.data.frame(pag3)
page3 = transmute(pag3,
                  country = factor(pais_c),
                  factor = factor_ch,
                  year = as.integer(anio_c),
                  area = factor(zona_c),
                  income = ylm_ci,
                  educ = aedu_ci,
                  sex = factor(sexo_ci))

page3 = page3 %>%
  filter(income > 100L & income <= 274088736L & !is.na(income)) %>%
  filter(educ >= 
           0L & educ <= 26L & !is.na(educ))

write.csv(page3, 'pag3.csv')

#####

anios = cbind(pais_c = NULL, anio_c = NULL, sexo_ci = NULL, ylm_ci = NULL)

for (anio in unique(df$anio_c)) {
  dfi = df %>% 
    filter(anio_c == anio)
  
  H = dfi %>% filter(sexo_ci == 'Hombre') %>%
    group_by(pais_c) %>% 
    summarise(
      year = anio,
      sexo = 'Hombre',
      ingreso = mean(ylm_ci, na.rm = T)
    )
  
  M = dfi %>% filter(sexo_ci == 'Mujer') %>%
    group_by(pais_c) %>% 
    summarise(
      year = anio,
      sexo = 'Mujer',
      ingreso = mean(ylm_ci, na.rm = T)
    )
  
  dfi = rbind(H, M)
  anios = rbind(anios, dfi)
  
}

paises = data.frame(cbind(pais_c = unique(anios$pais_c), c_name = c('Argentina', 'Bolivia', 'Brazil', 
                                                                    'Colombia', 'Costa Rica', 'Peru',
                                                                    'Paraguay', 'El Salvador', 'Uruguay',
                                                                    'Chile', 'Dominican Republic', 'Ecuador',
                                                                    'Guatemala', 'Mexico')))



df2 = right_join(anios, paises, "pais_c")

df2 = df2 %>% filter(anio_c != 2015)

pag3_ = transmute(df2,
                  year = as.integer(year),
                  country = pais_c,
                  c_name = c_name, 
                  sex = sexo,
                  income = ingreso)


write.csv(pag3_, 'page3_.csv')

#### 

anios = cbind(pais_c = NULL, anio_c = NULL, area = NULL, ylm_ci = NULL)

for (anio in unique(df$anio_c)) {
  dfi = df %>% 
    filter(anio_c == anio)
  
  U = dfi %>% filter(zona_c == 'urbana') %>%
    group_by(pais_c) %>% 
    summarise(
      year = anio,
      area = 'Urban',
      ingreso = weighted.mean(ylm_ci, na.rm = T)
    )
  
  R = dfi %>% filter(zona_c == 'rural') %>%
    group_by(pais_c) %>% 
    summarise(
      year = anio,
      area = 'Rural',
      ingreso = mean(ylm_ci, na.rm = T)
    )
  
  dfi = rbind(U, R)
  anios = rbind(anios, dfi)
  
}

paises = data.frame(cbind(pais_c = unique(anios$pais_c), c_name = c('Argentina', 'Bolivia', 'Brazil', 
                                                                    'Colombia', 'Costa Rica', 'Peru',
                                                                    'Paraguay', 'El Salvador', 'Uruguay',
                                                                    'Chile', 'Dominican Republic', 'Ecuador',
                                                                    'Guatemala', 'Mexico')))






df3 = full_join(anios, paises, "pais_c")

df3 = df3 %>% filter(anio_c != 2015)


pag4_ = transmute(df3,
                  year = as.integer(year),
                  country = pais_c,
                  c_name = c_name, 
                  area = area,
                  income = ingreso)

write.csv(pag4_, 'page4_.csv')


#####

Rural_Urbano_y_sexo <- read_csv("D:/Descargas/Rural, Urbano y sexo.csv", 
                                col_types = cols(Time = col_integer()))

df4 = transmute(Rural_Urbano_y_sexo,
               year = Time,
               country_n = `Country Name`,
               country_c = `Country Code`,
               female = `Population, female (% of total population) [SP.POP.TOTL.FE.ZS]`,
               male = `Population, male (% of total population) [SP.POP.TOTL.MA.ZS]`,
               rural = `Rural population (% of total population) [SP.RUR.TOTL.ZS]`,
               urban = `Urban population (% of total population) [SP.URB.TOTL.IN.ZS]`
)
df4 = df4 %>%
  filter(!(country_n %in% c("Honduras", "Haiti", "Nicaragua", "Panama", "Venezuela, RB")) 
         | is.na(country_n))
df4 = df4 %>% filter(year == 2000 | year == 2005 | year == 2010 | year == 2015 | year == 2018)

write.csv(df4, 'Rural-Urbano-Sex.csv')

####


df5 = read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/Indicadores por Región.csv", 
              col_types = cols(Time = col_integer()))
GDP_PC <- read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/GDP PC.csv",
                   col_types = cols(Time = col_integer()))
df5 = full_join(df5, GDP_PC)

df5 = transmute(df5, 
               year = Time,
               c_name = `Country Name`,
               c_code = `Country Code`,
               `GDP_2010` = df$`GDP (constant 2010 US$) [NY.GDP.MKTP.KD]`,
               density = df$`Population density (people per sq. km of land area) [EN.POP.DNST]`,
               ratio = `Urban population (% of total population) [SP.URB.TOTL.IN.ZS]`/`Rural population (% of total population) [SP.RUR.TOTL.ZS]`,
               ch_out = df$`Children out of school (% of primary school age) [SE.PRM.UNER.ZS]`,
               region = Region,
               `GDP_PC_2010` = df$`GDP per capita (constant 2010 US$) [NY.GDP.PCAP.KD]`
)

write.csv(df5, 'page1.csv')

### 

#df6 = read_csv("C:/Users/pedro/OneDrive/Desktop/Santiago/app/bases/PIB-GINI.csv", 
                           #col_types = cols(year = col_integer()))

#df6_1 = df6 %>% group_by(year) %>%
  #summarise(
   # country_c = 'BID',
    #country_n = 'BID',
    #GINI = mean(GINI),
    #GDPpc = mean(GDPpc))


#df6 = rbind(df6[, -1], df6_1)

#write.csv(df6, 'PIB-GINI.csv')
