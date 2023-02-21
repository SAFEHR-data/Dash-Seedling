CREATE DATABASE [feature-store]
GO

USE [feature-store];
GO

CREATE TABLE features (
    Id INT NOT NULL IDENTITY,
    Name TEXT NOT NULL,
    Value TEXT,
    PRIMARY KEY (Id)
);
GO

INSERT INTO [features] (Name, Value)
VALUES 
('Example 1', '1'),
('Example 2', '42'); 
GO
