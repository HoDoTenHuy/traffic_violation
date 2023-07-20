from os import environ

environ['PORT'] = '3000'
environ['HOST'] = 'localhost'

environ['DB_HOST'] = 'localhost'
environ['DB_USERNAME'] = 'root'
environ['DB_PASSWORD'] = ''
environ['DB_NAME'] = 'notes'
environ['DB_PORT'] = '3306'

environ['DATABASE_URL'] = 'mysql+pymysql://root:@localhost:3306/notes?schema=public'