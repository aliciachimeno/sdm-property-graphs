getwd()
setwd("/Users/ali/Downloads/dblp-to-csv-master")

library(skimr)
library(ggplot2)
library(tidyverse)
library(dplyr)

## authors, papers, conference, editions, volume, journal, 

dblp_article<-read.csv("dblp_article.csv",sep=";",row.names =NULL, encoding = "latin1",nrows=100000)
dblp_article
dblp_article_header<-read.csv("dblp_article_header.csv",sep=";",row.names =NULL, encoding = "latin1")
header<-names(dblp_article_header)
colnames(dblp_article)<-header
colnames(dblp_article)


# Assuming df is your dataframe
dblp_article <- na_if(dblp_article, "")
skim(dblp_article)

#summary(df_books$journal.string)
#df_books$journal.string<-as.factor(df_books$journal.string)


missing_prop <- colMeans(is.na(dblp_article))
threshold <- 0.8  # Adjust as needed
columns_to_remove <- names(dblp_article)[missing_prop > threshold]
dblp_article <- dblp_article[, !names(dblp_article) %in% columns_to_remove]
colnames(dblp_article)
dblp_article[,1:2]



