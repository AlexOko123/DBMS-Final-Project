### Installation (linux debian)

1. Install and enable docker

2. 

```bash 
sudo docker run -d --name oracle-xe \
  -p 1521:1521 -p 5500:5500 \
  -e ORACLE_PASSWORD=YourPassword123 \
  gvenzl/oracle-xe
```

* To reset! *

```bash
sudo docker stop oracle-xe
sudo docker rm oracle-xe

```

- To connect:
```bash
sudo docker exec -it oracle-xe sqlplus system/YourPassword123@//localhost:1521/XEPDB1
```


3. Login info:
User	system (default admin)
Password	YourPassword123 (set by you)
Host	localhost (or your IP)
Port	1521
Service	XEPDB1


## For windows

```bash
docker run -d --name oracle-xe `
  -p 1521:1521 -p 5500:5500 `
  -e ORACLE_PASSWORD=YourPassword123 `
  gvenzl/oracle-xe
```
OR
`docker run -d --name oracle-xe -p 1521:1521 -p 5500:5500 -e ORACLE_PASSWORD=YourPassword123 gvenzl/oracle-xe`

## Todo

- Try to simplify/fix the bs4 calls, don't have to go layer by layer
- Remove array for already_called_directors, use SQL mechanisim instead


### Resources

- https://www.omdbapi.com/
- https://oracle.github.io/python-oracledb/
- https://python-oracledb.readthedocs.io/en/latest/user_guide/introduction.html
- https://www.dbvis.com/download/
- https://www.oracle.com/database/technologies/xe-downloads.html and https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html (not needed)
