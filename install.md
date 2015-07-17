hosts

127.0.0.1 www.chimera.rey
127.0.0.1 api.chimera.rey
127.0.0.1 control.chimera.rey
127.0.0.1 storage.chimera.rey

nginx


# storage
server {
	listen 80;
    charset utf-8;
    root /var/www/chimera/storage;
    server_name storage.chimera.rey;
}

# public
server {
	listen 80;
    charset utf-8;
    root /var/www/chimera/public;
    server_name www.chimera.rey;
    index index.html;

	# Allow file uploads
	client_max_body_size 50M;

    location / {
    	try_files $uri /index.html;
    }

    location ~ \.(js|css|ico|htm|html|json)$ {
    	root /var/www/chimera/www/public;
        try_files $uri =404;
    }

}

# api
upstream frontends {
    server 127.0.0.1:8888;
    #server 127.0.0.1:8000;
    #server 127.0.0.1:8001;
    #server 127.0.0.1:8002;
    #server 127.0.0.1:8003;
}

server {
    listen 80;
    client_max_body_size 50M;
    charset utf-8;
    server_name api.chimera.rey;

    #location / {
    #    try_files $uri /index;
    #}

    # location ^~ /static/ {
    #     root /var/www;
    #     if ($query_string) {
    #         expires max;
    #     }
    # }
    # location = /favicon.ico {
    #     rewrite (.*) /static/favicon.ico;
    # }
    # location = /robots.txt {
    #     rewrite (.*) /static/robots.txt;
    # }

    location / {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://127.0.0.1:8888/;
        #proxy_pass http://frontends;
    }
}

# private
server {
	listen 80;
    charset utf-8;
    root /var/www/chimera;
    server_name control.chimera.rey;

	# Allow file uploads
	client_max_body_size 50M;

    location / {
    	root /var/www/chimera/www/private;
        index index.html;
    }

    location ~ \.(js|css|ico|htm|html|json)$ {
    	root /var/www/chimera/www/private;
        try_files $uri =404;
    }

	location /(.*) {
		proxy_pass_header Server;
		proxy_set_header Host $http_host;
		proxy_redirect off;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Scheme $scheme;
		proxy_pass http://frontends;
	}
}

h2. python

tornado
motorengine
bcrypt
