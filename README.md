# Read me: 
# Setting Up the FireGuard Application in a Local Kubernetes Environment
This guide walks you through the process of setting up the FireGuard application on your local machine using Minikube and Kubernetes. Follow the steps below to deploy the application and access it through a local service.

## Prerequisites for Running This Repository:
Before you start, ensure you have the following prerequisites installed on your machine:
 * DockerDeskop. Install [here](https://www.docker.com/products/docker-desktop/)
 * Minikube - For creating a local Kubernetes cluster. Install [Here](https://minikube.sigs.k8s.io/docs/start/)
 * Kubectl - For interacting with the Kubernetes cluster. Install [Here](https://kubernetes.io/docs/tasks/tools/)

## Getting Started:
Navigate to the directory containing the Kubernetes configuration files for the FireGuard application using the command line:
```sh
cd "...\FireGuard\kubernetes_files"
```

## Starting Minikube:
Start your Minikube environment with the following command:

```sh
minikube start
```
This command initializes a local Kubernetes cluster using Docker as the driver. It prepares Kubernetes along with necessary addons like the storage-provisioner and the default-storageclass for persistent storage needs.

## Verifying Minikube and Setting Contexts:
Once Minikube has started, verify that your kubectl is configured to use the "minikube" cluster and the "default" namespace by default:
```sh
kubectl config get-contexts
```

## Deploying the FireGuard Application
Deploy the FireGuard application by applying the Kubernetes manifests in the following order:

1. Apply the secrets configuration:
```sh
kubectl apply -f metclient-secret.yaml
```
2. Deploy the FireGuard application:
```sh
kubectl apply -f frcm-deployment.yaml
```
3. Expose the FireGuard application via a LoadBalancer service:
```sh
kubectl apply -f port-service.yaml
```
## NB! the previous step will most likely take some  time to download the docker file.
## Verifying the Application Deployment:
Check the status of the deployed resources (pods, services, deployments, etc.) to ensure everything is up and running:
```sh
kubectl get all
```
## NB! run the previous step until it is running before going further.
## Accessing the FireGuard Service:
Finally, access the FireGuard service through Minikube by running:
```sh
minikube service fireguard-service
```
This command automatically opens the service in your default browser or displays a URL that you can use to access the application.

The url will give empty json shown under:
```json
{
    "detail": "Not Found"
}
```
That because the API call is not correct. Use the IP and port provided and run the API call below in your web brownser or postman. 
```sh
http://<ip>:<port>/api/v1/fireriskAfterStartDate?start_date=2024-03-10&days=3&longitude=5.32415&latitude=60.39299
```
Congratulations you're the best! You have successfully deployed and accessed the FireGuard application in your local Kubernetes environment using Minikube. This setup is ideal for development and testing purposes. Remember, as you're using the Docker driver on Windows, keep the terminal open to maintain the service tunnel.
# To exit run
```sh
{
    minikube stop
}
```
