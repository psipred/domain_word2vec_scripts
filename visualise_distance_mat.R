library(rgl)

pfam_distances <- read.csv(file="/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/word2vec_E.similarity", row.names=1, header=TRUE, check.names=FALSE, strip.white = TRUE, sep=",",na.strings= c("NA", " ", ""))

dmat <- as.matrix(pfam_distances)
res <- cmdscale(dmat, k=3, eig=TRUE)

clade_labels <- read.csv(file="/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/Pfam2clade.csv", row.names=1, header=FALSE, check.names=FALSE, strip.white = TRUE, sep=",",na.strings= c("NA", " ", ""))
colnames(clade_labels) <- c("clade")
clade_labels$clade <- gsub("U", '', clade_labels$clade)
clade_labels$clade <- gsub("O", '', clade_labels$clade)
clade_labels$clade <- gsub("V", '', clade_labels$clade)
clade_labels[clade_labels == ""] <- NA
clade_labels$clade <- as.factor(clade_labels$clade)

mpoints <- merge(res$points, clade_labels, by=0, all=TRUE)
mpoints <- na.omit(mpoints)

col_set <- c('red', 'white', 'white', 'white' ,'green', 'white', 'blue')

plot3d(mpoints$V1, mpoints$V2, mpoints$V3, col=col_set)
legend3d("topright", pch=15,legend=levels(mpoints$clade), col=col_set, cex=1, inset=c(0.02))

col_set <- c('black', 'white', 'white', 'white' ,'black', 'white', 'black')

plot3d(mpoints$V1, mpoints$V2, mpoints$V3, col=col_set)
legend3d("topright", pch=15,legend=levels(mpoints$clade), col=col_set, cex=1, inset=c(0.02))

sample_set <- sample.int(11206, 1000)
sampled_distances <- pfam_distances[sample_set, sample_set]
sampled_dmat <- as.matrix(sampled_distances)
sampled_res <- cmdscale(sampled_dmat, k=3, eig=TRUE)
merges_s_res <- merge(sampled_res$points, clade_labels, by=0, all=TRUE)
merges_s_res <- na.omit(merges_s_res)

plot3d(merges_s_res$V1, merges_s_res$V2, merges_s_res$V3, col=col_set)
legend3d("topright", pch=15,legend=levels(merges_s_res$clade), col=col_set, cex=1, inset=c(0.02))