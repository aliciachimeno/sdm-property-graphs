getwd()
setwd("/Users/ali/Downloads/dblp-to-csv-master")


library(skimr)
library(ggplot2)
library(tidyverse)
library(dplyr)

#########################################################################################################
# paper -> journal

# loading
dblp_article<-read.csv("dblp_article.csv",sep=";",row.names =NULL, encoding = "latin1",nrows=100000) # load
dblp_article_header<-read.csv("dblp_article_header.csv",sep=";",row.names =NULL, encoding = "latin1") # load header
colnames(dblp_article)<-names(dblp_article_header) # put the header

## data exploration
## only want to keep: paper, authors, title, journal, volume, year, doi,
names(dblp_article)
dblp_article$article.ID # id
dblp_article$author.string.. # string de autors
dblp_article$ee.string.. # doi number
dblp_article$pages.string # !!abanico de pages, no num of pages
dblp_article$volume.string
dblp_article[,c(1,2,13,16,24,30,34,35)]


#########################################################################################################
# paper -> conference 
###################### inproceedings: dades dels PAPERS

dblp_inproceedings<-read.csv("dblp_inproceedings.csv",sep=";",row.names =NULL, encoding = "latin1",nrows=100000)
dblp_inproceedings_header<-read.csv("dblp_inproceedings_header.csv",sep=";",row.names =NULL, encoding = "latin1")
colnames(dblp_inproceedings)<-names(dblp_inproceedings_header)

#explore
names(dblp_inproceedings)
dblp_inproceedings$author.string.. #author
dblp_inproceedings$title.string # titul dels papers
dblp_inproceedings$crossref.string.. # key 

### relation: id_papers with authors
dblp_inproceedings$author.string.. #author
dblp_inproceedings$title.string # titul dels papers
dblp_inproceedings$inproceedings.ID # id dels papers

split_authors <- strsplit(dblp_inproceedings$author.string.., "\\|") # split els authors

authors_papersID <- data.frame(
  id_paper = rep(dblp_inproceedings$inproceedings.ID, sapply(split_authors, length)),
  author = unlist(split_authors)
)

authors_papersID
#write.csv(authors_papersID, "authors_idpapers.csv", row.names = FALSE)


### relation id_paper with paper

idpaper_paper<- data.frame(
  id_paper=dblp_inproceedings$inproceedings.ID,
  paper_title=dblp_inproceedings$title.string
)

## try to join paper and author ->left join
#l_j<-left_join(idpaper_paper,authors_papersID,by=c(c("id_paper"="id_paper"))) # ok works

###################### proceedings: dades de les CONFERENCES: 
# preprocess
dblp_proceedings<-read.csv("dblp_proceedings.csv",sep=";",row.names =NULL, encoding = "latin1",nrows=100000)
dblp_proceedings_header<-read.csv("dblp_proceedings_header.csv",sep=";",row.names =NULL, encoding = "latin1")
colnames(dblp_proceedings)<-names(dblp_proceedings_header)

#explore
colnames(dblp_proceedings)
dblp_proceedings$title.string # conference / workshop complete 
dblp_proceedings$booktitle.string # conference / workshop name 
dblp_proceedings$key.string # key

# ------------------------------------------------------------------------------------------

conference_split <- strsplit(dblp_proceedings$title.string, ", ")
conference_split[[945]] # example of entry
conference_name <- sapply(conference_split, function(x) paste(x[1], collapse = ", "))
detect_location <- function(entry) {
  location <- entry[nchar(entry) < 20 & !grepl("\\d", entry)] # Select entries shorter than 20 characters and without any number
  location <- paste(location, collapse = ", ") # Combine into a single string
  return(location)
}
locations <- sapply(conference_split, detect_location)
conference_year <- as.numeric(sub(".*\\b(\\d{4})\\b.*", "\\1", dblp_proceedings$title.string))


conference_title <- sub(".*?((?:Conference|Workshop).*?$)", "\\1", conference_name)

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
conference_edition <- extract_ordinals(conference_name)

  
conference_df <- data.frame(
  conference_complete=dblp_proceedings$title.string,
  acronym=dblp_proceedings$booktitle.string,
  ref=dblp_proceedings$key.string,
  conference_name=conference_name,
  conference_title = conference_title,
  conference_edition=conference_edition,
  location = locations,
  year=conference_year
)

## com no necessitem totes les dades, només una part -> borrem les entrades que tenen algun camp buit
#conference_df_complete <- na.omit(conference_df)


# join exmple
dblp_inproceedings_db<-dblp_inproceedings[,c(2,9,25)]
names(conference_df)
left_join_df <- left_join(dblp_inproceedings_db, conference_df, by = c("crossref.string.."="ref"))
left_join_df