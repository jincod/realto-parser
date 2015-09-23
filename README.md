Run flask app:
```
python app.py
```

Run celery:
```
celery -A tasks worker
```

*Required mongodb running (mongodb://localhost:27017/)*