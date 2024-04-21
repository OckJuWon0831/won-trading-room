-- Create database if not exists
CREATE DATABASE IF NOT EXISTS `stock_db`;

-- Use the database
USE `stock_db`;

CREATE TABLE IF NOT EXISTS `USERS` (
    `ID` VARCHAR(255) PRIMARY KEY,
    `PASSWORD` VARCHAR(255) NOT NULL
);

-- Create tables for each ticker if not exists
CREATE TABLE IF NOT EXISTS `AAPL` (
    `Date` DATE PRIMARY KEY,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);

CREATE TABLE IF NOT EXISTS `GOOG` (
    `Date` DATE PRIMARY KEY,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);

CREATE TABLE IF NOT EXISTS `META` (
    `Date` DATE PRIMARY KEY,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);

CREATE TABLE IF NOT EXISTS `NFLX` (
    `Date` DATE PRIMARY KEY,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);

CREATE TABLE IF NOT EXISTS `AMZN` (
    `Date` DATE PRIMARY KEY,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);
