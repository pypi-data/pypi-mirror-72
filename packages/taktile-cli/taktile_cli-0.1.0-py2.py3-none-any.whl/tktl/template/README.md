# Taktile-based deployment

## General logic
Users install the `tktl` client library through 
```pip install taktile-cli```

They can then initialize a basic repo with
```
tktl init --kind sklearn-regression 
```
For now, you need to install the client as follows:

```
pip install -e .tktl/taktile-client
```

Users instantiate the taktile client as `tktl = Tktl()` and supply: 
- `endpoints.py` with python functions
- `requirements.txt`

Within `endpoints.py`, users can supply datasets used for documentation and profiling of endpoints. This done through
```
data_test = tktl.data_from_parquet("data.pqt", label="survived")
```
Then, they decorate the functions they want as endpoints as follows:
```
@tktl.endpoint(kind="regression", data=[data_test])
def predict_raw(df):
    pred model.predict(df)
    return pred
```

## Building the Docker images

```
docker build -t tktl-1 --build-arg USERCODE=. -f .tktl/Dockerfile .
```

## Running the Docker images locally
```
docker run --rm --name tktl-1-local -p 80:80 tktl-1:latest
```
and then check that it works by running
```
curl -X POST "http://0.0.0.0/predict_function" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"pclass\":[0], \
        \"sex\":[\"string\"], \
        \"age\":[0], \
        \"sibsp\":[0], \
        \"parch\":[0], \
        \"fare\":[0], \
        \"embarked\":[\"string\"], \
        \"class\":[\"string\"], \
        \"who\":[\"string\"], \
        \"adult_male\":[true], \
        \"deck\":[0], \
        \"embark_town\":[\"string\"], \
        \"alive\":[\"string\"], \
        \"alone\":[true] \
        }"
```


## Automated Upload to GitHub Packages
Upon starting a PR, the image will be built and send to GitHub packages automatically.

## Sales Pitch for the deployment piece
* Simplicity: Endpoint generation is as simple as it could be
* Flexibility: Business logic, multiple endpoints, and multiple models per endpoint possible
* Documentation: Automated documentation of endpoints
* Feature validation: Automated validation of features

## Likes
* Use of FastAPI instead of Flask (async support)
* Docker images much smaller than MLFlow, typically very fast when caching is enabled (but not on GH actions)

## Dislikes
* Dependency on S3 for model and data assets. Currently, the Docker image is not sufficient to replicate predictions. We need to cache.
