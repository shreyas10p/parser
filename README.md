
Suppose you have access to three machines in your local area network. One is master machine and other two are slave machines. Each machine has server(django or any other) running on port 8000. Each server has capacity to process only two request simultaneously. Create a simple program that will receive request from the user’s web-browser and distribute the request to other servers depending on server capacity.

Example :Initially, all servers are currently in idle state. Suppose, user creates five request simultaneously that will be duly received by master machine’s server. The master server can process only two urls at a time, therefore, it redirects other two requests to Slave 1 and rest single request to Slave 2. Slave 1 & Slave 2 will produce the output and store in a Master server’s database. 
