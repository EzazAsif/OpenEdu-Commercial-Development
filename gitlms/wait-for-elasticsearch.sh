#!/bin/bash
set -e

echo "Waiting for Elasticsearch..."

until curl -s http://elasticsearch:9200 >/dev/null; do
  >&2 echo "Elasticsearch is unavailable - sleeping"
  sleep 5
done

>&2 echo "Elasticsearch is up - continuing"
