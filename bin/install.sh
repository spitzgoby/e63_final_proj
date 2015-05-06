# CLONE GIT REPOR
echo 'Creating home directory'
export E63_HOME='~/e63_final';
mkdir $E63_HOME &&
cd $E63_HOME &&
git clone git@github.com:spitzgoby/e63_final_proj.git &&

# INSTALL PYTHON DEPENDENCIES AND START SERVICE
echo 'Installing required python modules';
sudo pip install -r requirements.txt &&
python interaction_service/interaction_service.py;

# CONFIGURE ENVIRONMENT FOR SPARK 
