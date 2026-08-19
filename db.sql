DROP DATABASE IF EXISTS english_trainer;

CREATE DATABASE english_trainer;

CREATE USER trainer_user WITH PASSWORD 'english_trainer_password';

GRANT ALL PRIVILEGES ON DATABASE english_trainer TO trainer_user;

-- Recreate the database with your user as owner
CREATE DATABASE english_trainer OWNER trainer_user;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE english_trainer TO trainer_user;

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO trainer_user;
GRANT CREATE ON SCHEMA public TO trainer_user;