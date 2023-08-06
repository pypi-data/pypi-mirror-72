# Taktile-based deployment

## General logic
Users install the `tktl` CLI through 
```pip install taktile-cli```

They can then initialize a basic repo with
```
tktl init --name sample-deployment
```
For now, you need to install the client as follows:

```
git clone https://github.com/taktile-org/taktile-cli
pip install -e taktile-cli
```

Users instantiate the taktile client as `tktl = Tktl()` and supply: 
- `endpoints.py` with python functions
- `requirements.txt`

Within `endpoints.py`, users can supply datasets used for documentation and profiling of endpoints. This done by decorating the functions they want as endpoints:
```
@tktl.endpoint(kind="regression", data=data_test)
def predict_raw(df):
    pred model.predict(df)
    return pred
```

## Running the Docker images locally
```
tktl init --name sample-deployment
docker build -t tktl-local sample-deployment
docker run -d --rm --name tktl-local -p 80:80 tktl-local:latest
```

Then, check that it works by running
```
curl -X POST "http://0.0.0.0/binary" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d ' {
        "pclass":[0],
        "sex":["string"],
        "age":[0],
        "sibsp":[0],
        "parch":[0],
        "fare":[0],
        "embarked":["string"],
        "class":["string"],
        "who":["string"],
        "adult_male":[true],
        "deck":[0],
        "embark_town":["string"],
        "alive":["string"],
        "alone":[true]
        } '
```
You can stop the running container with `docker stop tktl-local`.
