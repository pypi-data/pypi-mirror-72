""" This module defines all exergi functions within the AWS.postgreSQL module"""

def config(filePath: str ='/home/ec2-user/SageMaker/.config/database.ini', 
    section: str = 'maximo')-> dict:
    """ The following config() function reads in the database.ini file and 
    returns the connection parameters as a dictionary. This function will be 
    imported in to the main python script. 
    
    This file was adapted from:
    http://www.postgresqltutorial.com/postgresql-python/connect/
    
    Arguments:
        - filePath      - Path to the "database.ini"-file required to initiate
                          connection.
        - section       - Section of "database.ini"-filefile where the 
                          connection-parameters are stored.
    Returns:
        - db_cred  - All connection parameters in the specified filePath   
                          and section
    """

    from configparser import ConfigParser

    parser = ConfigParser()     # Create a parser
    parser.read(filePath)       # Read config file
    db_cred = {}                # Get section, default to postgresql
    
    # Checks to see if section (postgresql) parser exists
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_cred[param[0]] = param[1]
    
    # Returns an error if a parameter is not listed in the initialization file
    else:
        raise Exception(f'Section {section} not found in the {filePath} file')
    return db_cred

def checkPostgreSQLConnection(db_cred: dict):
    """A function that checks connection settings and version of postgreSQL
    
    Arguments:
        - db_cred        - Connection parameters from config file
    """

    import psycopg2

    try:
        connection = psycopg2.connect(**db_cred)
        cursor = connection.cursor()
        
        # Print PostgreSQL Connection properties
        print (connection.get_dsn_parameters(),"\n")  
        
        # Print PostgreSQL version
        cursor.execute("SELECT version();")           
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to PostgreSQL", error)
    finally:
        # Closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                
def importDataFromPostgreSQL(sql_query: str,db_cred: dict):
    """A function that takes in a PostgreSQL query and outputs a pandas database 
    
    Arguments:
        - sql_query     - SQL-query to run
        - db_cred        - Connection parameters from config file
    Returns:
        - df            - DataFrame with Loaded Data
    """

    import psycopg2
    import pandas as pd

    try:
        connection = psycopg2.connect(**db_cred)
        cursor = connection.cursor()
        df = pd.read_sql_query(sql_query, connection)
        
        # Convert pandas dtype="object" columns to pd.StringDtype()
        for col in df.select_dtypes("object").columns:
            df[col] = df[col].astype(pd.StringDtype())
            
    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    return df

def importData(sql_query: str, db_cred: dict, table: str= None, 
    convert_dtypes: bool=True, return_meta_data: bool=False):
    """
    NOTE: This function will replace importDataFromPostgreSQL in future releases
    
    A function that takes in a PostgreSQL query and outputs a pandas database 
    
    Arguments:
        - sql_query         - SQL-query to run
        - db_cred           - Connection parameters from config file
        - table             - Possibility to provide table name where schema if 
                              should be imported if not found by regex
        - convert_dtypes    - Flag if data types should be converted using the 
                              data base schema for the used table
        - return_meta_data  - Flag if meta data should be returned 
    Returns:
        - df                - DataFrame with loaded data
        - (df_meta)         - DataFrame with loaded meta data (db schema), only
                              returned if return_meta_data == True
    """

    import psycopg2
    import pandas as pd
    import time
    import re

    connection = None
    
    try:
        
        # Get Data
        connection = psycopg2.connect(**db_cred)
        cursor = connection.cursor()
        df = pd.read_sql_query(sql_query, connection)
        
        # Get Meta Data  ############################
        if table == None:

            search_patterns = [
                r"(?<=\s)maximoworker_[a-z]*(?=\s[w|W])",
                r"(?<=\s)maximoworker_[a-z]*\Z"]

            for pat in search_patterns:
                regex_search = re.findall(pat,sql_query)
                if len(regex_search) == 1:
                    table = regex_search[0]
        
        if (table != None) & convert_dtypes:
            
            meta_data_query = f"""
                SELECT column_name,data_type,is_nullable
                FROM information_schema.columns 
                WHERE table_name = '{table}'"""
            df_meta = pd.read_sql(meta_data_query,connection)
            
            for col in df.columns:
                
                # If derived column exists (not avaliable in schema, do not convert)
                if col not in df_meta.column_name.unique():
                    print(f"WARNING: {col} not found in schema")
                    continue
            
                dtype = df_meta.loc[df_meta.column_name==col,"data_type"].item()   
                
                # Use Pandas New NA function
                if df[col].isna().sum() > 0:
                    df.loc[df[col].isna(),col] = pd.NA
                
                if dtype == 'integer':
                    df[col] = df[col].astype(pd.Int64Dtype())    # Groupby does't work. Still in experimental with 1.0.3
                elif dtype == 'character varying':
                    df[col] = df[col].astype(pd.StringDtype()) 
                elif dtype == 'timestamp with time zone':
                    df[col] = pd.to_datetime(df[col],infer_datetime_format=True,errors="coerce")
                    df[col] = df[col].dt.tz_localize(None)      # NOTE: This removes potential TimeZone information in DB
                elif dtype == 'numeric':
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                elif dtype == 'boolean':
                    df[col] = df[col].astype(bool)
                else:
                    raise(Exception(f"Datatype conversion {dtype} not implemented"))

        else:
            print("WARNING. No Dtype conversion. Wasn't able to find table name")
                    
    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    if return_meta_data:
        return df ,df_meta.loc[df_meta.column_name.isin(df.columns.tolist())]
    else:
        return df