#psql

CREATE DATABASE mynotes;
 
-- Create user for database
CREATE ROLE mynotes WITH LOGIN ENCRYPTED PASSWORD 'mynotes' CREATEDB;
-- Edit September 25/2015 : 
-- For security Only set CREATEDB permission
-- Which is required for the Django tests
 
-- Grant privileges to the user to access database
GRANT ALL PRIVILEGES ON DATABASE mynotes TO mynotes;

#export DATABASE_URL=postgres://mynotes:mynotes@localhost:5432/mynotes
#service  postgresql start