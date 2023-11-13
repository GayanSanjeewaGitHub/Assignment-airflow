# Assignment-airflow

Step 1: Enable the Rest API in Airflow

You need to edit the airflow config file as by default airflow does not accept any request through REST API. Browse airflow.cfg file and set auth_backends as

You can also restart the web server if this is not working and You can also check the REST API, You simply need to pass the Authorization in the form of username:password where the username of the airflow user and password is the password of that user.

Step 2: Enable CORS

Write these lines below the [API] section in airflow.cfg and also replace https://exampleclientapp1.com and https://exampleclientapp2.com with your website name or localhost. You can also refer here to know more about CORS.

Step 3: Test the API by Listing all your dags available

We can list all our dags by hitting GET request on /api/v1/dags endpoint. If you are running airflow on your localhost you can get all your dags by hitting GET request to http://localhost:8080/api/v1/dags also don’t forget to set the Authorization.



you may need to restart the docker , you changes will go away . So commit them and run new container , stop the current one. Same result can be archieved in deferrent way by restarting the services.

 sudo docker commit 24bd9f7adc1c airflow:5
sudo docker stop 24bd9f7adc1c
 sudo docker run -d -p 8080:8080  airflow:5
names and ID will chnages for you.but to confirm check the chnages

 sudo docker exec -it 8cf0f8701200 /bin/bash
As you know your chnages are in the dag file , then the web service and scheduler get your dags.

if your are working in a windows machine , but your docker is runing in WS ubuntu you may need to parse file into docker container.

you can use docker cp command

other wise as a best practise , you can mount your docker path to local path as you prefer , by passing the command with docker ..-v …. (volume).



I have defined the provide_context=True.

So I can access that from the function as below.

  variable = kwargs['dag_run'].conf.get('environment_type')
with that changes we can trigger the end points , based on our choice


def process_data(**kwargs):
    environment_type = kwargs['dag_run'].conf.get('environment_type')       # XComs allow tasks to exchange small amounts of metadata
    kwargs['ti'].xcom_push(key='environment_type', value=environment_type) #cross-communication mechanism in Airflow
    environment_type = kwargs['ti'].xcom_pull(task_ids='process_data', key='environment_type')
    if environment_type == 'development':
        return 'file_creation_development'
    elif environment_type == 'production':
        return 'file_creation_production'
    else:
        raise ValueError(f"Invalid environment_type: {environment_type}. Allowed values