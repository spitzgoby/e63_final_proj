# CLONE GIT REPOR
echo 'Creating home directory'
git clone https://github.com/spitzgoby/e63_final_proj.git &&
cd ~/e63_final_proj; 

# INSTALL PYTHON DEPENDENCIES AND START SERVICE
echo 'Installing required python modules';
sudo pip install -r requirements.txt &&
python interaction_service/interaction_service.py;

# CONFIGURE ENVIRONMENT FOR SPARK 
