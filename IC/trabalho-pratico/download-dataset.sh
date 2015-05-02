#!/bin/bash
mkdir dataset -p
cd dataset
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00210/donation.zip
unzip donation.zip
rm donation.zip
unzip block_10.zip
unzip block_1.zip
unzip block_2.zip
unzip block_3.zip
unzip block_4.zip
unzip block_5.zip
unzip block_6.zip
unzip block_7.zip
unzip block_8.zip
unzip block_9.zip
rm *.zip
find . -name "*.csv" | xargs sed -i s/\?/-1/
