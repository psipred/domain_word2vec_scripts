library(ggplot2)

pathroot<-"/home"
if (R.version$os=="darwin13.4.0")     pathroot="/Users"

angles_data <-  read.csv(file=paste(pathroot,"/dbuchan/Code/domain_word2vec/transform_angles.csv", sep=""), check.names=FALSE, strip.white = TRUE, sep=",",na.strings= c("NA", " ", ""))

nuclear_slice <- angles_data[angles_data$group == "nuclear",]
intracellular_slice <- angles_data[angles_data$group == "intracellular",]
transmembrane_slice <- angles_data[angles_data$group == "transmembrane",]

ggplot(nuclear_slice, aes(x=radians)) + geom_histogram()
mean(nuclear_slice$radians)

ggplot(intracellular_slice, aes(x=radians)) + geom_histogram()+ xlab('Radians') + ylab("Count")+theme(text = element_text(size=20))
ggsave("/scratch0/NOT_BACKED_UP/dbuchan/projects/interpro_word2vec/Fig7_intra-extra_radian_histogram.eps", width=10, height=7, dpi=300)
mean(intracellular_slice$radians)

ggplot(transmembrane_slice, aes(x=radians)) + geom_histogram()
mean(transmembrane_slice$radians)

duf_count_data <-  read.csv(file=paste(pathroot,"/dbuchan/Code/domain_word2vec/duf_counts.csv", sep=""), check.names=FALSE, strip.white = TRUE, sep=",",na.strings= c("NA", " ", ""))
ggplot(duf_count_data, aes(x=Count)) + geom_histogram() + xlab('Number of GO terms assigned') + ylab("Frequency")+theme(text = element_text(size=20))
ggsave("/scratch0/NOT_BACKED_UP/dbuchan/projects/interpro_word2vec/Fig9_duf_assignment_frequencies.eps", width=10, height=7, dpi=300)