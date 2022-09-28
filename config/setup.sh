#!/bin/sh
#
# Setup ELK and TLS

set -e

ELASTICSEARCH_URL=https://es-master:9200
KIBANA_URL=https://kibana:5601

CERT_DIR=config/certs
CA_CERT=$CERT_DIR/ca/ca.crt
CA_KEY=$CERT_DIR/ca/ca.key


check_environment_variables()
{
    echo "Checking environment variables"

    if [ x${ELASTICSEARCH_PASSWORD} == x ]; then
        echo "Set the ELASTICSEARCH_PASSWORD environment variable in the .env file";
        exit 1;
    elif [ x${ELASTICSEARCH_USERNAME} == x ]; then
        echo "Set the ELASTICSEARCH_USERNAME environment variable in the .env file";
        exit 1;
    elif [ x${KIBANA_PASSWORD} == x ]; then
        echo "Set the KIBANA_PASSWORD environment variable in the .env file";
        exit 1;
    fi;
}

create_self_signed_ca()
{
    if [ ! -f $CERT_DIR/ca.zip ]; then
        echo "Creating self-signed Certificate Authority";
        bin/elasticsearch-certutil ca --silent --pem -out $CERT_DIR/ca.zip;
        unzip $CERT_DIR/ca.zip -d $CERT_DIR;
    fi;
}

create_certificates()
{
    if [ ! -f $CERT_DIR/certs.zip ]; then
        echo "Creating crt and key certificates";
        bin/elasticsearch-certutil cert --silent \
            --pem -out $CERT_DIR/certs.zip \
            --in config/instances.yml \
            --ca-cert $CA_CERT --ca-key $CA_KEY;
        unzip $CERT_DIR/certs.zip -d $CERT_DIR;
    fi;

    echo "Setting file permissions"
    chown -R root:root $CERT_DIR;
    find . -type d -exec chmod 750 \{\} \;;
    find . -type f -exec chmod 640 \{\} \;;
}

set_kibana_system_user()
{
    echo "Setting kibana_system password";

    until curl -s -X POST --cacert $CA_CERT \
        -u elastic:$ELASTICSEARCH_PASSWORD \
        -H "Content-Type: application/json" \
        $ELASTICSEARCH_URL/_security/user/kibana_system/_password -d "
        {
            \"password\":\"$KIBANA_PASSWORD\"
        }" | grep -q "^{}"; do
        sleep 10;
    done;
}

create_elasticsearch_index_role()
{
    echo "Creating index privileges role";

    curl -X POST --cacert $CA_CERT \
        -u elastic:$ELASTICSEARCH_PASSWORD \
        -H "Content-Type: application/json" \
        $ELASTICSEARCH_URL/_security/role/happy_admin?pretty -d"
        {
            \"indices\": [
            {
                \"names\": [\"users\"],
                \"privileges\": [\"all\"]
            }]
        }";
}

create_elasticsearch_regular_user()
{
    echo "Creating regular user with admin privileges";

    curl -X POST --cacert $CA_CERT \
        -u elastic:$ELASTICSEARCH_PASSWORD \
        -H "Content-Type: application/json" \
        $ELASTICSEARCH_URL/_security/user/$ELASTICSEARCH_USERNAME -d"
        {
            \"password\": \"${ELASTICSEARCH_PASSWORD}\",
            \"enabled\": true,
            \"roles\": [\"kibana_admin\", \"kibana_system\", \"happy_admin\"]
        }";
}

check_environment_variables
create_self_signed_ca
create_certificates

echo "Waiting for Elasticsearch availability";
until curl -s --cacert $CA_CERT $ELASTICSEARCH_URL | grep -q "missing authentication credentials"; do sleep 10; done;

set_kibana_system_user
create_elasticsearch_index_role
create_elasticsearch_regular_user

echo "Waiting for Kibana availability";
until curl -s --insecure -I $KIBANA_URL | grep -q "HTTP/1.1 302 Found"; do sleep 10; done;

echo "All done!";
