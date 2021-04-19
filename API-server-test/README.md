# How to run

###### First thing first.
Clone the repository
`git clone https://github.com/polyrize/interview-server.git`

To run the server you have 2 option. one run the server.py file
or you can build and run the docker container, instructions as follows
### Run the server.py
Change to the repository directory
```bash
$ cd interview-server
```

Install dependencies
```bash
$ pip install -r requirements.txt
```

Run server.py
```bash
$ python server.py
```
### Using Docker
Change to the repository directory
```bash
$ cd interview-server
```
build the docker image
```bash
docker build -t interview-server .
```
Run it.
```bash
docker run -p 8000:8000 interview-server
```
In both cases server will be available in `http://localhost:8000`

 # API Refrence

 ## Authentication
 You first must authenticate with the API to gain access.
 The following endpoint will return an access token which in turn should be added to the `Authorization` header

 Username and password will be provided.

 | Endpoint  | Method | Params                                                             | Response                                                           | Example |
|-----------|--------|--------------------------------------------------------------------|--------------------------------------------------------------------|---------|
| /api/auth | POST   | Json Body: ``` {   "username": "test",   "password": "1234" }  ``` |  ``` { "access_token":"ververylongstringwithnumbersandstuff" } ``` |         |


 ### *All endpoints require the following headers*
 ```
 "Content-Type": "application/json"
 "Authorization": "Bearer {your_token_here}"
 ```

## Endpoints

| Endpoint              | Method | Params                                                                                                                 | Returns            | Example |
|-----------------------|--------|------------------------------------------------------------------------------------------------------------------------|--------------------|---------|
| /api/poly             | GET    |                                                                                                                        | List of PolyData   |         |
| /api/poly             | POST   | json body: ```json {   "data": [     {       "key": "key1",       "val": "val1",       "valType": "str"     }   ] }``` | The created object |         |
| /api/poly/<object_id> | GET    | object_id: int - Representing the object id                                                                            | PolyData           |         |
| /api/poly/<object_id> | DELETE | object_id: int - Representing the object id  to delete                                                                 | `204` Empty Response |         |

# PolyData
The object that return from the above endpoints.
```json
{
  "object_id": 65656,
  "data": [
    {
      "key": "key1",
      "val": "val1",
      "valType": "str"
    }
  ]
}
```