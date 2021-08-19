#from an environment variable
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'es*y86f+-t@%27n&4$6#p)t%jaeqxxom_g%dpa5=)an3%emtlf'
JWT_SECRET_KEY = 'adf2fa0b-5243-483a-b062-67f51609db60'


#SECRET_KEY = os.environ.get('SECRET_KEY')

#from an file
#with open('/etc/secret_key.txt') as f:
 #   SECRET_KEY = f.read().strip() """