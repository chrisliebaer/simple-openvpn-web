#!/bin/sh

set -e

if [ -z "$PASSWORD_FILE" ]; then
		echo "PASSWORD_FILE not set"
		exit 1
fi

if [ -z "$username" ]; then
		echo "username not set"
		exit 1
fi

if [ -z "$password" ]; then
		echo "password not set"
		exit 1
fi

while read -r line; do
		if [ "$username:$password" = "$line" ]; then
				exit 0
		fi
done < "$PASSWORD_FILE"

exit 1