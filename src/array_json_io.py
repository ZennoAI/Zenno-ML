from bentoml.io import IODescriptor
from typing import List, Any
from ast import literal_eval

class ArrayJSONIODescriptor(IODescriptor[List[dict]]):
    """
    Custom IODescriptor for handling an array of JSON data.
    """
    _mime_type = "application/json"

    def __init__(self):
        super().__init__()

    def _from_sample(self, sample: List[dict]) -> List[dict]:
        return sample

    def to_spec(self) -> dict:
        return {
            "type": "array",
            "items": {
                "type": "object",
            }
        }
        
    def openapi_components(self):
      return {
          "components": {
              "schemas": {
                  "arrayJsonSchema": {
                      "type": "array",
                      "items": {
                          "type": "object",
                          "properties": {
                              "title": {"type": "string"},
                              "url": {"type": "string"},
                              "content": {"type": "string"},
                              "success": {"type": "string"},
                              # Add more properties based on your JSON structure
                          },
                      },
                  },
              },
          },
      }

        
    def openapi_request_body(self):
      # pass
        return {
            "content": {
                self._mime_type: {
                    "schema": {"$ref": "#/components/schemas/arrayJsonSchema"}
                }
            }
        }
    
    def input_type(self) -> List[dict]:
        return List[dict]

    async def from_http_request(self, request) -> List[dict]:
      try:
          body_bytes = await request.body()
          json_data = body_bytes.decode('utf-8')
          data = literal_eval(json_data)
        
          if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
              raise ValueError("Input data is not a valid array of JSON objects")
          
          return data
      except Exception as e:
          raise ValueError(f"Error parsing JSON from HTTP request: {str(e)}")


    async def to_http_response(self, obj: List[dict], ctx=None) -> Any:
        return obj

    async def from_proto(self, field) -> List[dict]:
        try:
            return field
        except Exception as e:
            raise ValueError(f"Error converting from protobuf: {str(e)}")

    async def to_proto(self, obj: List[dict]) -> Any:
        try:
            return obj
        except Exception as e:
            raise ValueError(f"Error converting to protobuf: {str(e)}")

