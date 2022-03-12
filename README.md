# TinyNewsServer
The TinyNews Server for our Mobile Apps & Services class project.

## Implementation
Currently the server side just acts as a cache + API for the NewsCatcher API we are using. If time allows, we may add our own summary implementation.

## Usage
Create a file named `newscatcher_api_key` with the following format:

`{"api-key":"<YOUR_API_KEY>"}`

To get data into the database [schema found here](https://github.com/ananthsd/TinyNewsSchema) use the `locally_store` and `db_store_from_local` functions. Currently they are separated, but they can be trivially chained and automated.
We current don't do this for testing purposes and to minimize the amount of API calls we do.
