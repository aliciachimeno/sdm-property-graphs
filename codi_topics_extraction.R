install.packages("remotes")
remotes::install_github("news-r/textblob")

# replace with path of your choice
my_env <- "./env"

# run this (works on unix)
args <- paste("-m venv", my_env) 
system2("python3", args) # create environment
reticulate::use_virtualenv(my_env) # force reticulate to use env
# install textblob in environment
textblob::install_textblob(my_env)

# download corpora
textblob::download_corpora() 

library(textblob)

string <- paste(
  "Seven Steps to Rendezvous with the Casual User"
)

wiki <- text_blob(string) 

wiki$sentiment # get sentiment
#> Sentiment(polarity=0.4, subjectivity=0.8)

wiki$correct() # correct programmming langage
#> R is a programming language and free software environment for statistical computing and graphics supported by the R Foundation for Statistical Computing.

wiki$np_extractor$extract(string)

topics <- c("Data Management", "Indexing", "Data Modeling", "Big Data", "Data Processing", "Data Storage", "Data querying")
