[Tutorial](https://www.ibm.com/developerworks/cloud/library/cl-develop-blockchain-app-in-python/index.html)


```
source env/bin/activate
flask run
```


```
http POST http://127.0.0.1:5000/new_transaction author=me content=mytransaction
http GET http://127.0.0.1:5000/chain
http GET http://127.0.0.1:5000/mine
http GET http://127.0.0.1:5000/pending_tx
http POST http://127.0.0.1:5000/add_nodes ...
http POST http://127.0.0.1:5000/add_block ...
```