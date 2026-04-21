# Deployment Information

This directory contains the scripts needed for the prototype of our Spotify customer churn prediction model. There is a FastAPI backend and an interactive Streamlit dashboard. 

**Note**: The dashboard is a work in progress, and will be improved in the future. 

## Prerequisites

Ensure there is a model registered in MLflow Model Registry. Launch the MLflow UI by running the following command in the terminal: 

```bash
# Start MLflow UI for visualization
mlflow ui --port 5000
```

## Running the FastAPI Server

We chose to use uvicorn to run the server. In a new terminal, run:

```bash
uvicorn app.main:app 
```
The API server will be available at: http://localhost:8000/docs 

## Running the Streamlit Dashboard

The dashboard can be directly executed using the following command:

```bash
streamlit run app/streamlit_app.py
```
The dashboard will be available at:

## Using the Dashboard

1. Check that the API is connected. If not, see intructions above. 

2. Input the required feature values for a user. 

3. Click "Predict Churn" and view results. 

