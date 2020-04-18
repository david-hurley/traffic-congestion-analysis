# Analysis of COVID-19 Impact on Traffic Congestion in Vancouver Area

Code to collect drive time data from the Google Maps Distance Matrix API and store it in an Amazon Web Services (AWS) DynamoDB database. 
The data is collected using Python code run on a schedule in AWS Lambda. The Distance Matrix API is used to request the estimated drive time between two points as if you were departing now.
The data is processed and visualized using a Jupyter Notebook. 
