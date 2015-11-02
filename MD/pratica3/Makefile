download_datasets:
	rm *.data -rf
	wget http://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data
	wget http://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data
	wget http://archive.ics.uci.edu/ml/machine-learning-databases/00267/data_banknote_authentication.txt -O banknote.data
setup:
	sudo apt-get install python-numpy python-scipy -y
	sudo pip install sklearn --upgrade
run:
	make setup
	make download_datasets
	python main.py
itstop:
	kill -9 $(ps aux | grep "[p]ython main.py" | awk '{print $2}')
