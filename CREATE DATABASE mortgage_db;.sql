CREATE DATABASE mortgage_db;
USE mortgage_db;
-- Table for Anonymous Alerts
-- We use UUIDs to ensure user privacy (No Names/Emails)
CREATE TABLE user_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_uuid VARCHAR(255) NOT NULL,
    target_rate DECIMAL(5, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

