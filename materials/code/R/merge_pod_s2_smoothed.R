library(lubridate)

## GEE script... https://code.earthengine.google.com/06ad5adca90af9c8afc294f9b765a2e4

pod_data <- read.csv("./materials/data/pod_s2_merge/pod_data_downloaded.csv")
pod_data$date <- as_date(pod_data$time)

s2_smoothed_ndvi <- read.csv("./materials/data/pod_s2_merge/S2_data_downloaded.csv",
                             stringsAsFactors = FALSE)
colnames(s2_smoothed_ndvi) <- c("S2_time", "S2_ndvi_original", "S2_ndvi_smoothed")
s2_smoothed_ndvi$date = as_date(s2_smoothed_ndvi$S2_time, format = "%b %d, %Y")



s2_smoothed_ndvi_filt <- s2_smoothed_ndvi %>% filter(!is.na(S2_ndvi_smoothed))

pod_data_joined <- merge(pod_data, s2_smoothed_ndvi_filt, by = 'date', all.x = TRUE)

