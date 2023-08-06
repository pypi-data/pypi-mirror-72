### Model manifest

Model consists of following items:

- name: str
- kind: str [HTML / API]
- pipelines: str
- schedule: int
- delay: int

- stages: List
- request: Dict
- pagination: Dict


### Stage manifest

Stage consists of following items:

- selector: str

- request: Dict
- subs: List

### Request manifest

Request consists of following items:
- links: Dict / key: str
- headers: Dict
- cookies: Dict
- data: Dict

- method: str
- timeout: int

\* based on request manifest location. If request is used in stage definition,
`key` is used to take value from parsed data dict. If request is used in model
definition, links are used to make request, for ex:

```json
{
    "request": {
        "links": {
            "link_name1": "https://example.com/path/to/resource/1/",
            "link_name2": "https://example.com/path/to/resource/2/"
        }
    }
}
```
