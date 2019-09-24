# dat<-data.frame(replicate(20, sample(c("A","B","C","D"), size = 100, replace=TRUE)))

corpus = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/word2vec_input_E.dat"
input_data <- read.csv(file=corpus, check.names=FALSE, strip.white = TRUE, sep=" ",na.strings= c("NA", " ", ""))

Markovmatrix <- function(X, l=1){
   tt <- table(X[, -c((ncol(X)-l+1):ncol(X))] , c(X[,-c(1:l)]))
   tt <- tt / rowSums(tt)
   return(tt)
}