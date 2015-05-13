# CLONE GIT REPO
# git clone https://github.com/spitzgoby/e63_final_proj.git &&
cd ~/e63_final_proj;
mkdir data;

# add sbt repo to apt-get's database and install
echo "deb http://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list &&
sudo apt-get update;
sudo apt-get install sbt;

# CONFIGURE ENVIRONMENT FOR SPARK 
cd ~;
mkdir spark;
cd spark/;
wget http://mirror.tcpdiag.net/apache/spark/spark-1.2.1/spark-1.2.1.tgz;
gunzip -c spark-1.2.1.tgz | tar -xvf -;
cd spark-1.2.1/;
sudo sbt/sbt assembly;
cd ..;
sudo cp -Rp spark-1.2.1 /usr/local/;
cd /usr/local/;
sudo ln -s spark-1.2.1 spark;


# copy existing interactions and and cities data
cd ~/e63_final_proj;
curl -k https://s3-us-west-1.amazonaws.com/thomasleu.e63final/interactions.csv -o ~/e63_final_proj/data/interactions.csv;
curl -k https://s3-us-west-1.amazonaws.com/thomasleu.e63final/cities.csv -o ~/e63_final_proj/data/cities.csv;


# INSTALL PYTHON DEPENDENCIES AND START SERVICE
sudo pip install -r requirements.txt;
cqlsh -f commands.cql;
python interaction_service/interaction_service.py;
