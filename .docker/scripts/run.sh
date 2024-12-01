#!/bin/bash

# Start the Dagster webserver in the background
dagster-webserver -h 0.0.0.0 -p 3000 &

# Start the Dagster daemons
dagster-daemon run