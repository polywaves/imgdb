import os
import oracledb


connection = oracledb.connect(
  user=os.environ["ORACLE_USER"],
  password=os.environ["ORACLE_PASSWORD"],
  port=os.environ["ORACLE_PORT"],
  host=os.environ["ORACLE_HOST"],
  service_name=os.environ["ORACLE_SERVICE_NAME"]
)