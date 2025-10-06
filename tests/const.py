LOG_TEMPLATE = (
    "{pri}{nginx_datetime} {host} nginx: "
    "{ip} client42 admin {log_datetime} "
    '"{method} {uri} {protocol}" 200 1024 "-" "Mozilla/5.0"'
)


DEFAULT_LOG_VALUES = {
    "pri": "<134>",
    "nginx_datetime": "Sep 15 18:25:43",
    "host": "my-nginx-host",
    "ip": "31.28.159.255",
    "log_datetime": "[15/Sep/2025:18:25:43 +0200]",
    "method": "GET",
    "uri": "/index.html",
    "protocol": "HTTP/1.1",
}
