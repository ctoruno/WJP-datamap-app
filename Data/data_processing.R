library(haven)
library(readxl)
library(tidyverse)

datamap <- read_excel("Documents/GitHub/WJP-datamap-app/datamap.xlsx")
gpp     <- read_dta("OneDrive - World Justice Project/Data Analytics/Data/GPP/Merged.dta")

var4map <- (datamap$name)[4:395]

available_countries <- lapply(var4map, 
                              function(var){
                                
                                countries <- gpp %>% 
                                  select(country, all_of(var)) %>%
                                  rename(target = 2) %>%
                                  group_by(country) %>% 
                                  summarise(count = sum(!is.na(target))) %>%
                                  filter(count > 0) %>%
                                  pull(country)
                                countries <- paste(countries, collapse = "; ")
                                
                              })

available_years <- lapply(var4map, 
                          function(var){
                            
                            years <- gpp %>% 
                              select(year, all_of(var)) %>%
                              rename(target = 2) %>%
                              group_by(year) %>% 
                              summarise(count = sum(!is.na(target))) %>%
                              filter(count > 0) %>%
                              pull(year)
                            years <- paste(years, collapse = "; ")
                            
                          })


added_data <- as.data.frame(list(
  "name"                = var4map,
  "available_countries" = as.character(available_countries),
  "available_years"     = as.character(available_years)
))

new_data <- left_join(datamap, added_data) %>%
  mutate(available_countries = if_else(is.na(available_countries),
                                       "Always present",
                                       available_countries),
         available_years     = if_else(is.na(available_years),
                                       "Always present",
                                       available_years))

write_csv(new_data, "Documents/GitHub/WJP-datamap-app/Data/datamap.csv")
