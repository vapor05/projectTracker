#!/bin/bash

cd ..

psql nbocchini -d projectTracker -f ddl/create_tables.sql

psql nbocchini -d projectTracker -f dml/populate_status.sql
