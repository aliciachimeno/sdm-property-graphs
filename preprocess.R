getwd()
setwd("/Users/ali/Downloads/dblp-to-csv-master")

library(skimr)
library(ggplot2)
library(tidyverse)

## authors, papers, conference, editions, volume, journal, 

df_authors<-read.csv("dblp_author.csv",sep=";",row.names =NULL, encoding = "latin1")
df_authors

df_books_header<-read.csv("dblp_book_header.csv",sep=";",row.names =NULL, encoding = "latin1")
header<-names(df_books_header)

df_books<-read.csv("dblp_book.csv",sep=";",row.names =NULL, encoding = "latin1")
df_books
colnames(df_books)<-header
df_books
skim(df_books)
summary(df_books$journal.string)

df_books$journal.string<-as.factor(df_books$journal.string)
names(df_books)
