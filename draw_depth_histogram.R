line <- readChar("/home/dbuchan/Code/domain_word2vec/duf_annotation_depths_list.csv", file.info("/home/dbuchan/Code/domain_word2vec/duf_annotation_depths_list.csv")$size-1)
number_list <- unlist(strsplit(line, split=","))
number_list <- number_list [! number_list %in% '-']
number_list <- as.integer(number_list)
mean(number_list)
hist(number_list)