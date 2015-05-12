function usage
{
  echo "Usage: ./install.sh [-k keyfile] [-d aws ip/host]"
}

while [ "$1" != "" ]; do
    case $1 in
        -k | --key )            shift
                                KEY=$1
                                ;;
        -d | --dns )            shift
                                HOST=$1 
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

if [ "$KEY" != "" ]; then
  if [ "$HOST" != "" ]; then
    ssh -t -i $KEY ubuntu@$HOST bash -c "'
      # CLONE GIT REPO
      echo 'Creating home directory'
      git clone https://github.com/spitzgoby/e63_final_proj.git &&
      cd ~/e63_final_proj; 

      # INSTALL PYTHON DEPENDENCIES AND START SERVICE
      echo 'Installing required python modules';
      sudo pip install -r requirements.txt &&
      echo 'Starting interaction REST service';
      python interaction_service/interaction_service.py;

      # CONFIGURE ENVIRONMENT FOR SPARK 
    '"
  else
    usage
    exit 1
  fi
else
  usage
  exit 1
fi

exit