"""generative_agents.utils.arguments"""

import os
import json
import copy
from typing import Any


def load_dict(str_dict: str, flavor: str = "json") -> dict:
    """Safe version: supports both file path & JSON string with detailed error reporting."""
    import os, json, copy

    if not str_dict:
        return {}

    # --- 1️⃣ 当传入是路径 ---
    if isinstance(str_dict, str) and os.path.isfile(str_dict):
        try:
            with open(str_dict, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except Exception as e:
            raise IOError(f"[load_dict] 无法读取文件: {str_dict}\n错误: {e}")

        if not content:
            raise ValueError(f"[load_dict] 文件为空: {str_dict}")

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"[load_dict] 文件不是有效 JSON: {str_dict}\n错误: {e}")

    # --- 2️⃣ 当传入是 JSON 字符串 ---
    elif isinstance(str_dict, str):
        try:
            return json.loads(str_dict)
        except json.JSONDecodeError as e:
            raise ValueError(f"[load_dict] 输入字符串不是有效 JSON，错误: {e}")

    # --- 3️⃣ 当传入是字典对象 ---
    elif isinstance(str_dict, dict):
        return copy.deepcopy(str_dict)

    # --- 4️⃣ 其他类型 ---
    raise TypeError(f"[load_dict] 不支持的输入类型: {type(str_dict)} (值={str_dict})")

def save_dict(dict_obj: Any, path: str, indent: int = 2) -> str:
    """Save dict object

    Parameters
    ----------
    dict_obj:
        The object that can be load as dict.
    path: str
        The output path.
    indent: int
        The indent

    Returns
    -------
    path: str
        The output path.
    """

    with open(path, "w") as f:
        f.write(json.dumps(load_dict(dict_obj), indent=indent, ensure_ascii=False))
    return path


def update_dict(src_dict: dict, new_dict: dict, soft_update: bool = False) -> dict:
    """Update src_dict with new_dict.

    Parameters
    ----------
    src_dict: dict
        The source dict.
    new_dict: dict
        The new dict.
    soft_update: bool
        Whether to update the source dict, False to force update.

    Returns
    -------
    dict_obj: dict
        The updated dict.
    """

    if not src_dict:
        return new_dict
    if not new_dict:
        return src_dict
    assert isinstance(src_dict, dict) and isinstance(
        new_dict, dict
    ), "update_dict only support dict, get src {} and new {}".format(
        type(src_dict), type(new_dict)
    )
    for k, v in new_dict.items():
        if not src_dict.get(k):
            src_dict[k] = v
        elif isinstance(v, dict):
            v = update_dict(src_dict.get(k, {}), v, soft_update)
            src_dict[k] = v
        elif not soft_update:
            src_dict[k] = v
    return src_dict


def dump_dict(dict_obj: dict, flavor: str = "table:2") -> str:
    """Dump the config to string.

    Parameters
    ----------
    src_dict: dict
        The source dict.
    flavor: str
        The flavor for dumps.

    Returns
    -------
    str_dict: string
        The dumped string.
    """

    if not dict_obj:
        return ""
    if flavor.startswith("table:"):

        def _get_lines(value, indent=0):
            max_size = int(flavor.split(":")[1]) - indent - 2
            lines = []
            for k, v in value.items():
                if v is None:
                    continue
                if isinstance(v, (dict, tuple, list, set)) and not v:
                    continue
                if isinstance(v, dict) and len(str(k) + str(v)) > max_size:
                    lines.append("{}{}:".format(indent * " ", k))
                    lines.extend(_get_lines(v, indent + 2))
                elif (
                    isinstance(v, (tuple, list, set))
                    and len(str(k) + str(v)) > max_size
                ):
                    lines.append("{}{}:".format(indent * " ", k))
                    for idx, ele in enumerate(v):
                        if isinstance(ele, dict) and len(str(ele)) > max_size:
                            lines.append(
                                "{}[{}.{}]:".format((indent + 2) * " ", k, idx)
                            )
                            lines.extend(_get_lines(ele, indent + 4))
                        else:
                            lines.append(
                                "{}<{}>{}".format((indent + 2) * " ", idx, ele)
                            )
                elif isinstance(v, bool):
                    lines.append(
                        "{}{}: {}".format(indent * " ", k, "true" if v else "false")
                    )
                elif hasattr(v, "__name__"):
                    lines.append(
                        "{}{}: {}({})".format(indent * " ", k, v.__name__, type(v))
                    )
                else:
                    lines.append("{}{}: {}".format(indent * " ", k, v))
            return lines

        lines = _get_lines(dict_obj) or [
            "  {}: {}".format(k, v) for k, v in dict_obj.items()
        ]
        return "\n".join(lines)
    return json.dumps(dict_obj, ensure_ascii=False)


def dict_equal(dict_a: dict, dict_b: dict) -> bool:
    """Check if two dicts are the same.

    Parameters
    ----------
    dict_a: dict
        The A dict.
    dict_b: dict
        The B dict.

    Returns
    -------
    equal: bool
        Whether two dicts are the same.
    """

    if not isinstance(dict_a, dict) or not isinstance(dict_b, dict):
        return False
    if dict_a.keys() != dict_b.keys():
        return False
    for k, v in dict_a.items():
        if not isinstance(v, type(dict_b[k])):
            return False
        if isinstance(v, dict) and not dict_equal(v, dict_b[k]):
            return False
        if v != dict_b[k]:
            return False
    return True


def copy_dict(dict_obj: dict) -> dict:
    """Deepcopy dict object

    Parameters
    ----------
    dict_obj: dict
        The source dict.

    Returns
    -------
    dict_obj: dict
        The copied dict.
    """

    if not dict_obj:
        return {}
    try:
        return copy.deepcopy(dict_obj)
    except:  # pylint: disable=bare-except
        new_dict = {}
        for k, v in dict_obj.items():
            if isinstance(v, (list, tuple)):
                new_dict[k] = [copy_dict(e) for e in v]
            elif isinstance(v, dict):
                new_dict[k] = copy_dict(v)
            else:
                new_dict[k] = v
        return new_dict


def map_dict(dict_obj: dict, mapper: callable) -> dict:
    """Apply mapper to dict object

    Parameters
    ----------
    dict_obj: dict
        The source dict.
    mapper: callable
        The mapper function.

    Returns
    -------
    new_dict: dict
        The mapped dict.
    """

    if not dict_obj:
        return {}
    new_dict = {}
    for k, v in dict_obj.items():
        if isinstance(v, (tuple, list)):
            new_dict[k] = [
                map_dict(mapper(e), mapper) if isinstance(e, dict) else mapper(e)
                for e in v
            ]
        elif isinstance(v, dict):
            new_dict[k] = map_dict(mapper(v), mapper)
        else:
            new_dict[k] = mapper(v)
    return new_dict
