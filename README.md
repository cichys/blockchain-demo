[Tutorial](https://www.ibm.com/developerworks/cloud/library/cl-develop-blockchain-app-in-python/index.html)


```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

python3 node_server.py
python3 app/run.py
```


```
http POST http://127.0.0.1:8000/new_transaction author=me content=mytransaction
http GET http://127.0.0.1:8000/chain
http GET http://127.0.0.1:8000/mine
http GET http://127.0.0.1:8000/pending_tx
http POST http://127.0.0.1:8000/add_nodes ...
http POST http://127.0.0.1:8000/add_block ...

http POST http://127.0.0.1:5000/submit author=me content=mytransaction
```