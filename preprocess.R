getwd()
setwd("/Users/ali/Downloads/dblp-to-csv-master")

library(skimr)
library(ggplot2)
library(tidyverse)
library(dplyr)


### graphs modeling 

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

# dades dels papers
dblp_inproceedings<-read.csv("dblp_inproceedings.csv",sep=";",row.names =NULL, encoding = "latin1",nrows=100000)
dblp_inproceedings_header<-read.csv("dblp_inproceedings_header.csv",sep=";",row.names =NULL, encoding = "latin1")
header_3<-names(dblp_inproceedings_header)
colnames(dblp_inproceedings)<-header_3

names(dblp_inproceedings)
dblp_inproceedings$title.string # titul dels papers
dblp_inproceedings$crossref.string..
dblp_inproceedings_db<-dblp_inproceedings[,c(9,25)]

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
inner_join_df <- inner_join(dblp_proceedings_db, dblp_inproceedings_db, by = c("key.string" = "crossref.string.."))
inner_join_df
