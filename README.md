# Connector for ShowAds API

Simple application that validates and processes customer data and calls ShowAds to show them banner next time they visit the website.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Running Tests](#running-tests)

## Requirements
- Docker

## Installation

1. Clone the repo
2. Rename .env.example to .env
3. *Edit .env file (optional)*
4. *Replace dataset in "/data/data.csv" with your own (optional)*
5. Build the image `docker build -t showads-connector:latest .`
6. Run the image using `docker run --rm showads-connector:latest`

## Running tests

After building the image you can simply run `docker run --rm showads-connector:latest pytest`