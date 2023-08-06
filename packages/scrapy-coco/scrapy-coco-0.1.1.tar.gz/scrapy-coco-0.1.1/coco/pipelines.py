import json
from typing import Any, Union


async def dump_to_file(model, page_results):
    file_name = f'output/{model.name}'

    if model.pagination:
        file_name += f'_{model.pagination.page}'

    file_name += '.json'

    with open(file_name, 'w') as stream:
        json.dump(page_results, fp=stream, ensure_ascii=False, indent=4)


async def to_int(raw: Any, **_) -> Union[Any, int]:
    if not isinstance(raw, str) or not raw.isdigit():
        return raw
    return int(raw)


async def to_float(raw: Any, **_):
    if not isinstance(raw, str):
        return raw

    return float(raw) if raw.replace('.', '', 1).isdigit() else raw
