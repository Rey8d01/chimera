Install
=======

hosts - domains
---------------

    127.0.0.1 www.chimera.rey
    127.0.0.1 api.chimera.rey
    127.0.0.1 storage.chimera.rey

nginx
-----

    # storage
    server {
        listen 80;
        charset utf-8;
        root /dir/to/chimera/storage;
        server_name storage.chimera.rey;
    }

    # public
    server {
        listen 80;
        charset utf-8;
        root /dir/to/chimera/www/public;
        server_name www.chimera.rey;
        index index.html;
        client_max_body_size 5M;

        location / {
            try_files $uri /index.html;
        }

        location ~ \.(js|css|ico|htm|html|json)$ {
            try_files $uri =404;
        }
    }

    # api
    upstream backends {
        server 127.0.0.1:8888;
    }

    server {
        listen 80;
        client_max_body_size 50M;
        charset utf-8;
        server_name api.chimera.rey;

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://backends;
        }
    }
