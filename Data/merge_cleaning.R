library(haven)
library(tidyverse)

merged <- read_dta("Merged.dta") %>%
  select(!ends_with("_norm")) %>%
  filter(! country %in% c("Belize", "Guatemala", "Honduras", "El Salvador", "Nicaragua", "Costa Rica", "Panama"))

expgpp <- read_dta("LAC - Merged (with CA).dta") %>%
  select(!ends_with("_norm"))

data   <- merged %>% 
  bind_rows(expgpp)

cnames <- names(data)

results <- map_dfr(cnames[7:length(cnames)], function(targetCol){
  
  subset <- data %>%
    select(country, year, all_of(targetCol)) %>%
    rename(target = 3) %>%
    group_by(country, year) %>%
    summarise(n = sum(!is.na(target))) %>%
    filter(n > 0) %>%
    mutate(country_year = paste(country, year, sep = "-"),
           variable     = targetCol) %>%
    group_by(variable) %>%
    summarise(availability = toString(country_year))
  
  return(subset)
  
})

write_csv(results, "/Users/carlostorunopaniagua/Documents/GitHub/WJP-datamap-app/Data/merged_availability.csv")