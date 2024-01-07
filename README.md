# JSONSchemaDiscovery
This repository contains a 'compose.yaml' which when executed installs all the required dependencies to run this tool

# What you need 
Ensure that you have `docker compose` installed on your local machine. You can check this by running the following command:
```docker compose version```

# Build and run the tool
After cloning the repository into your local machine and navigating into the folder, Start up the containers by running the following command in your terminal:
```
docker compose up -d
```
The above command launches two containers in detached mode: `mongodb` for the database and `jsonschema` for the JSONSchemaDiscovery tool. The tool runs in development mode, and you can access the GUI at http://localhost:4200/ once the application server is fully loaded. You can register using any email address and password of your choice to access the dashboard area.

# Running the smoke test
To run `smoke.sh` from inside the container, execute the following command to enter into the running container:
```
    docker exec -it jsonschema /bin/bash
```
Ensure that both containers are still running before executing the above command. To check this, run: ```docker ps```. Once inside the `jsonschema` container, execute this command:
```
./smoke.sh
```
This outputs the version of the JSONSchemaDiscovery tool as well as the Node.js version installed.

# Generating the pdf
While the docker image is being built, the Makefile is triggered to generate a PDF file in the `ReproEngReport` folder. To regenerate this PDF report file again, first, execute the clean command:
``` 
make clean
```
The above command removes all the generated files produced from executing the Makefile. Once all files have been removed, execute the following command to generate the PDF file again:
``` 
make report
```

This command generates the PDF again inside the `ReproEngReport` folder. To ensure that this file has been generated, you can simply display all contents in the `ReproEngReport` folder with this command: 
```
ls ReproEngReport/
```

To copy the `ReproEngReport` folder from the container to the host file system, run the following command outside the container:
``` 
docker cp jsonschema:/home/kali/JSONSchemaDiscovery/ReproEngReport .
```