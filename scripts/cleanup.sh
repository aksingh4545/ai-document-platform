#!/bin/bash

# Delete files older than 7 days
find /opt/app/uploads -type f -mtime +7 -delete

echo "Cleanup done at $(date)" >> /opt/app/logs/cleanup.log
