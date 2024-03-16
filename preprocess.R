getwd()
setwd("/Users/ali/Downloads/dblp-to-csv-master")

library(skimr)
library(ggplot2)
library(tidyverse)
library(dplyr)

# paper -> journal

# load
dblp_article<-read.csv("dblp_article.csv",sep=";",row.names =NULL, encoding = "latin1",nrows=100000)
# load header
dblp_article_header<-read.csv("dblp_article_header.csv",sep=";",row.names =NULL, encoding = "latin1")
header<-names(dblp_article_header)
colnames(dblp_article)<-header
#preprocess
dblp_article <- na_if(dblp_article, "")
skim(dblp_article)
missing_prop <- colMeans(is.na(dblp_article))
threshold <- 0.8  
columns_to_remove <- names(dblp_article)[missing_prop > threshold]
dblp_article <- dblp_article[, !names(dblp_article) %in% columns_to_remove]
colnames(dblp_article)


## DATA EXPLORATION
## only want to keep: paper, authors, title, journal, volume, year, doi,
names(dblp_article)
dblp_article$article.ID # id
dblp_article$author.string.. # string de autors
dblp_article$ee.string.. # doi number
dblp_article$pages.string # !!abanico de pages, no num of pages
dblp_article$volume.string
dblp_article[,c(1,2,4,5,9,10,12,13)]

# paper -> conference 
#inproceedings: dades dels papers
dblp_inproceedings<-read.csv("dblp_inproceedings.csv",sep=";",row.names =NULL, encoding = "latin1",nrows=100000)
dblp_inproceedings_header<-read.csv("dblp_inproceedings_header.csv",sep=";",row.names =NULL, encoding = "latin1")
header_3<-names(dblp_inproceedings_header)
colnames(dblp_inproceedings)<-header_3

names(dblp_inproceedings)
dblp_inproceedings$author.string.. #author
dblp_inproceedings$title.string # titul dels papers
dblp_inproceedings$crossref.string.. # key pel join
dblp_inproceedings_db<-dblp_inproceedings[,c(2,9,25)]

# dades de les conferences: 
# preprocess
dblp_proceedings<-read.csv("dblp_proceedings.csv",sep=";",row.names =NULL, encoding = "latin1",nrows=100000)
dblp_proceedings_header<-read.csv("dblp_proceedings_header.csv",sep=";",row.names =NULL, encoding = "latin1")
header_4<-names(dblp_proceedings_header)
colnames(dblp_proceedings)<-header_4

#explore
colnames(dblp_proceedings)
dblp_proceedings$title.string # conference / workshop name 
dblp_proceedings$key.string
dblp_proceedings_db<-dblp_proceedings[,c(15,29,32)]


# join
names(dblp_proceedings_db)
left_join_df <- left_join(dblp_inproceedings_db, dblp_proceedings_db, by = c("crossref.string.."="key.string"))
left_join_df$title.string.y

#################################################

conference_split <- strsplit(left_join_df$title.string.y, ", ")
conference_split[[2]] # exaple of entry
conference_name <- sapply(conference_split, function(x) paste(x[1], collapse = ", "))
detect_location <- function(entry) {
  location <- entry[nchar(entry) < 20 & !grepl("\\d", entry)] # Select entries shorter than 20 characters and without any number
  location <- paste(location, collapse = ", ") # Combine into a single string
  return(location)
}
locations <- sapply(conference_split, detect_location)
conference_year <- as.numeric(sub(".*\\b(\\d{4})\\b.*", "\\1", left_join_df$title.string.y))


conference_title <- sub(".*?((?:Conference|Workshop).*?$)", "\\1", conference_df$conference_name)
conference_edition <- extract_ordinals(conference_name)


extract_ordinals <- function(names_list) {
  # Regular expression pattern to match ordinal numbers up to "30th"
  ordinal_pattern <- "\\b(?:1st|2nd|3rd|(?:[4-9]|1[0-9]|2[0-9]|30)th|First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth)\\b"
  
  # Extract ordinal numbers from each entry
  extracted_ordinals <- regmatches(names_list, gregexpr(ordinal_pattern, names_list))
  
  # Create a vector to store the results
  result <- character(length(names_list))
  
  # Loop through each entry to assign ordinal numbers or NA
  for (i in seq_along(names_list)) {
    if (length(extracted_ordinals[[i]]) > 0) {
      result[i] <- extracted_ordinals[[i]]
    } else {
      result[i] <- NA
    }
  }
  
  return(result)
}


conference_title <- sub(".*?((?:Conference|Workshop).*?$)", "\\1", conference_df$conference_name)
conference_edition <- extract_ordinals(conference_name)


  
conference_df <- data.frame(
  conference_complete=left_join_df$title.string.y,
  ref=left_join_df$crossref.string..,
  title=left_join_df$title.string.x,
  conference_name=conference_name,
  conference_title = conference_title,
  conference_edition=conference_edition,
  location = locations,
  year=conference_year
)

## com no necessitem totes les dades, només una part -> borrem les entrades que tenen algun camp buit
conference_df_complete <- na.omit(conference_df)


