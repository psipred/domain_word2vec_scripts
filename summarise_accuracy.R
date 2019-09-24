pathroot<-"/home"
if (R.version$os=="darwin13.4.0")     pathroot="/Users"
nn1_accuracy_data <- read.csv(file=paste(pathroot,"/dbuchan/Code/domain_word2vec/nn1_accuracy_with_recall.csv", sep=""), check.names=FALSE, strip.white = TRUE, sep=",",na.strings= c("NA", " ", ""))
nn3_accuracy_data <- read.csv(file=paste(pathroot,"/dbuchan/Code/domain_word2vec/nn3_accuracy_with_recall.csv", sep=""), check.names=FALSE, strip.white = TRUE, sep=",",na.strings= c("NA", " ", ""))
nn5_accuracy_data <- read.csv(file=paste(pathroot,"/dbuchan/Code/domain_word2vec/nn5_accuracy_with_recall.csv", sep=""), check.names=FALSE, strip.white = TRUE, sep=",",na.strings= c("NA", " ", ""))
nn10_accuracy_data <- read.csv(file=paste(pathroot,"/dbuchan/Code/domain_word2vec/nn10_accuracy_with_recall.csv", sep=""), check.names=FALSE, strip.white = TRUE, sep=",",na.strings= c("NA", " ", ""))
nn1_subset <- nn1_accuracy_data[nn1_accuracy_data$`No. True` != 0, ]
nn3_subset <- nn3_accuracy_data[nn1_accuracy_data$`No. True` != 0, ]
nn5_subset <- nn5_accuracy_data[nn1_accuracy_data$`No. True` != 0, ]
nn10_subset <- nn10_accuracy_data[nn1_accuracy_data$`No. True` != 0, ]

results_table_with_recall <- data.frame("K" = c(1,3,5,10),
                            "Mean Precision" = c(mean(nn1_subset$Precision), mean(nn3_subset$Precision), mean(nn5_subset$Precision), mean(nn10_subset$Precision)),
                            "Mean Accuracy" = c(mean(nn1_subset$Accuracy), mean(nn3_subset$Accuracy), mean(nn5_subset$Accuracy), mean(nn10_subset$Accuracy)),
                            "Mean Recall" = c(mean(nn1_subset$Recall), mean(nn3_subset$Recall), mean(nn5_subset$Recall), mean(nn10_subset$Recall)),
                            "Mean MCC" = c(mean(nn1_subset$MCC), mean(nn3_subset$MCC), mean(nn5_subset$MCC), mean(nn10_subset$MCC)),
                            "Mean Hit Rate" = c(mean(nn1_subset$`Hit Rate`), mean(nn3_subset$`Hit Rate`), mean(nn5_subset$`Hit Rate`), mean(nn10_subset$`Hit Rate`)),
                            "Mean Consensus Precision" = c(mean(nn1_subset$`Consensus Precision`), mean(nn3_subset$`Consensus Precision`), mean(nn5_subset$`Consensus Precision`), mean(nn10_subset$`Consensus Precision`)),
                            "Mean Consensus Accuracy" = c(mean(nn1_subset$`Consensus Accuracy`), mean(nn3_subset$`Consensus Accuracy`), mean(nn5_subset$`Consensus Accuracy`), mean(nn10_subset$`Consensus Accuracy`)),
                            "Mean Consensus Recall" = c(mean(nn1_subset$`Consensus Recall`), mean(nn3_subset$`Consensus Recall`), mean(nn5_subset$`Consensus Recall`), mean(nn10_subset$`Consensus Recall`)),
                            "Mean Consensus MCC" = c(mean(nn1_subset$`Consensus MCC`), mean(nn3_subset$`Consensus MCC`), mean(nn5_subset$`Consensus MCC`), mean(nn10_subset$`Consensus MCC`)),
                            "Mean Consensus Hit Rate" = c(mean(nn1_subset$`Consensus Hit Rate`), mean(nn3_subset$`Consensus Hit Rate`), mean(nn5_subset$`Consensus Hit Rate`), mean(nn10_subset$`Consensus Hit Rate`))
                            )
