#!/usr/bin/env bash
host="$1"
shift
cmd="$@"

until nc -z "$host" 6379; do
  echo "Waiting for Redis at $host..."
  sleep 2
done

exec $cmd
