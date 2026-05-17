CREATE TABLE IF NOT EXISTS users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    phone_number VARCHAR(10) UNIQUE NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    user_password VARCHAR NOT NULL,
    user_role VARCHAR DEFAULT 'standard'
);

-- IOT device tables
CREATE TABLE IF NOT EXISTS device (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    device_type VARCHAR NOT NULL,
    device_location VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS device_subscriber (
    device_id INT REFERENCES device (id) PRIMARY KEY,
    subscriber_id INT REFERENCES users (id) NOT NULL
);

CREATE TABLE IF NOT EXISTS reading (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    device_id INT REFERENCES device (id) NOT NULL,
    alert_needed BOOLEAN NOT NULL,
    alert_sent BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS uv_reading (
    reading_id INT REFERENCES reading (id) PRIMARY KEY,
    uva INT,
    uvb INT
);

CREATE TABLE IF NOT EXISTS internal_state_reading (
    reading_id INT REFERENCES reading (id) PRIMARY KEY,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2)
);

CREATE TABLE IF NOT EXISTS grass_reading (
    reading_id INT REFERENCES reading (id) PRIMARY KEY,
    surface_temp DECIMAL(5,2),
    soil_moisture DECIMAL(5,2)
);

-- Job and Equipment tables
CREATE TABLE IF NOT EXISTS job (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    overseer INT REFERENCES users (id) NOT NULL, 
    assigner INT REFERENCES users (id),
    description TEXT NOT NULL,
    date_assigned TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    date_finished TIMESTAMPTZ,
    hours_required INT
);

CREATE TABLE IF NOT EXISTS equipment (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    price INT
);

CREATE TABLE IF NOT EXISTS job_equipment (
    id INT GENERATED ALWAYS AS IDENTITY,
    job_id INT REFERENCES job (id) NOT NULL,
    equipment_id INT REFERENCES equipment (id) NOT NULL,
    quantity INT DEFAULT 1,
    PRIMARY KEY (id, job_id, equipment_id)
);

-- User Messaging Tables
CREATE TABLE IF NOT EXISTS conversation (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    conversation_name VARCHAR
);

CREATE TABLE IF NOT EXISTS user_conversation (
    convo_id INT REFERENCES conversation (id) NOT NULL,
    user_id INT REFERENCES users (id) NOT NULL,
    PRIMARY KEY (convo_id, user_id)
);

CREATE TABLE IF NOT EXISTS message (
    id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    convo_id INT REFERENCES conversation (id) NOT NULL,
    sender INT REFERENCES users (id) NOT NULL,
    job_id INT REFERENCES job (id), -- nullable, most messages don't reference a job
    content TEXT,
    sent_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    PRIMARY KEY (id, convo_id)
);
