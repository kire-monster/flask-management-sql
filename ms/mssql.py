import pyodbc
"""
# Versiones soportadas
# {SQL Server} - released with SQL Server 2000
# {SQL Native Client} - released with SQL Server 2005 (also known as version 9.0)
# {SQL Server Native Client 10.0} - released with SQL Server 2008
# {SQL Server Native Client 11.0} - released with SQL Server 2012
# {ODBC Driver 11 for SQL Server} - supports SQL Server 2005 through 2014
# {ODBC Driver 13 for SQL Server} - supports SQL Server 2005 through 2016
# {ODBC Driver 13.1 for SQL Server} - supports SQL Server 2008 through 2016
# {ODBC Driver 17 for SQL Server} - supports SQL Server 2008 through 2019
"""
class SqlConnection:
    
    def __init__(self, drive, ip, usr, pwd, database):
        self.connectionString = 'DRIVER=' + drive + ';SERVER='+ip+';DATABASE='+database+';UID='+usr+';PWD='+ pwd + ";Charset='utf-8'"
        self.timeout = 0
        self.cnx = None
        self.cursor = None
        self.MessageError = ''
        self.StatusError = False
    
    def open(self):
        try:
            if not self.StatusError:
                self.cnx = pyodbc.connect(self.connectionString, timeout=self.timeout)
                #self.cnx.setencoding(encoding='utf-8')
                self.cursor = self.cnx.cursor()
                self.StatusError = False
        except Exception as err:
            self.MessageError = err 
            self.StatusError = True


    def close(self):
        try:
            self.cnx.close()
        except Exception as err:
            self.MessageError = err 
            self.StatusError = True

            
        
    
