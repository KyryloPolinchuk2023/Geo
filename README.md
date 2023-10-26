# API Documentation

## Base URL

The base URL for this API is `http://localhost:5000`. 

## Endpoints

### Fields Nearby

- **URL**: `/fields_nearby`
- **Method**: `GET`
- **Description**: Retrieves geographic fields that are located nearby a specified point.
- **Parameters**:
  - `lon` (float, required): Longitude of the reference point.
  - `lat` (float, required): Latitude of the reference point.
  - `distance` (float, required): Search radius distance in meters.
  - `crop` (string, optional): Filter results by crop type.
- **Response**:
  - `200 OK` with a JSON object containing a list of nearby fields.
  - `200 OK` with message "There are no fields".

### Fields Inside

- **URL**: `/fields_inside`
- **Method**: `GET`
- **Description**: Retrieves geographic fields that are located inside a specified polygon.
- **Parameters**:
  - `lon1`, `lat1`, `lon2`, `lat2`, `lon3`, `lat3`, `lon4`, `lat4` (float, required): Coordinates of the polygon vertices.
  - `crop` (string, optional): Filter results by crop type.
- **Response**:
  - `200 OK` with a JSON object containing a list of nearby fields.
  - `200 OK` with message "There are no fields".

### Fields Intersect

- **URL**: `/fields_intersect`
- **Method**: `GET`
- **Description**: Retrieves geographic fields that intersect with a specified polygon.
- **Parameters**:
  - `lon1`, `lat1`, `lon2`, `lat2`, `lon3`, `lat3`, `lon4`, `lat4` (float, required): Coordinates of the polygon vertices.
  - `crop` (string, optional): Filter results by crop type.
- **Response**:
  - `200 OK` with a JSON object containing a list of nearby fields.
  - `200 OK` with message "There are no fields".

### Fields Data

- **URL**: `/fields_data`
- **Method**: `GET`
- **Description**: Retrieves aggregated data for fields in a specified region.
- **Parameters**:
  - `region` (string, required): The region code for which data is requested.
- **Response**:
  - `200 OK` with a JSON object containing total area, total yield, and average yield for fields in the specified region.
  - `200 Ok` if the `region` parameter is missing with message "error": "Region not found or no data available.".
  - `200 Ok` Region not found or no data available if no result.

## Response Format

- The response is in JSON format.

## Rate Limit

There is a result limit of 10,000 records for all endpoints. If the result exceeds this limit, you will receive a message to refine your query.
Message: "Result limit exceeded. Please refine your query."
Quantity of result is shown in logs.
