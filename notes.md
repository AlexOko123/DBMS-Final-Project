### Installation (linux debian)

1. Install and enable docker

2. 

```bash 
docker run -d --name oracle-xe \
  -p 1521:1521 -p 5500:5500 \
  -e ORACLE_PASSWORD=YourPassword123 \
  gvenzl/oracle-xe
```

* To reset! *

```bash
sudo docker stop oracle-xe
sudo docker rm oracle-xe

```


3. Login info:
User	system (default admin)
Password	YourPassword123 (set by you)
Host	localhost (or your IP)
Port	1521
Service	XEPDB1



## Todo

- Try to simplify/fix the bs4 calls, don't have to go layer by layer
- Remove array for already_called_directors, use SQL mechanisim instead
