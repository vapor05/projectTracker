#!/bin/bash

export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/11/lib

cd ..

psql nbocchini -d projectTracker -f ddl/create_tables.sql

psql nbocchini -d projectTracker -f dml/populate_status.sql
