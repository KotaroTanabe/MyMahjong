"""Tenhou log validator.

Checks the structure produced by :mod:`core.tenhou_log` and raises
:class:`ValidationError` on failure.
"""
from __future__ import annotations

import json
from typing import Any, Dict


class ValidationError(Exception):
    """Raised when a log fails validation."""


TenhouLog = Dict[str, Any]


def validate_tenhou(log: TenhouLog) -> None:
    """Validate ``log`` parsed from a Tenhou JSON string."""
    if not isinstance(log, dict):
        raise ValidationError("トップレベルはオブジェクトである必要があります")

    title = log.get("title")
    if (
        not isinstance(title, list)
        or len(title) != 2
        or not all(isinstance(x, str) for x in title)
    ):
        raise ValidationError("title は長さ2の文字列配列である必要があります")

    names = log.get("name")
    if (
        not isinstance(names, list)
        or len(names) != 4
        or not all(isinstance(x, str) for x in names)
    ):
        raise ValidationError("name は長さ4の文字列配列である必要があります")

    rule = log.get("rule")
    if (
        not isinstance(rule, dict)
        or "disp" not in rule
        or "aka" not in rule
        or not isinstance(rule["disp"], str)
        or rule["disp"] == ""
        or not isinstance(rule["aka"], int)
        or rule["aka"] < 0
    ):
        raise ValidationError("rule は disp:非空文字列, aka:0以上 のオブジェクトである必要があります")

    rounds = log.get("log")
    if not isinstance(rounds, list) or len(rounds) < 1:
        raise ValidationError("log は半荘を1つ以上含む配列である必要があります")

    for idx, rd in enumerate(rounds):
        validate_round(rd, idx)


def validate_round(rd: Any, idx: int) -> None:
    if not isinstance(rd, list) or len(rd) < 5:
        raise ValidationError(f"round[{idx}] は配列かつ要素数5以上が必要です")

    ju_info = rd[0]
    if (
        not isinstance(ju_info, list)
        or len(ju_info) != 3
        or not all(isinstance(x, int) and x >= 0 for x in ju_info)
    ):
        raise ValidationError(f"round[{idx}][0] の局情報は全て0以上の整数である必要があります")

    defen = rd[1]
    if (
        not isinstance(defen, list)
        or len(defen) != 4
        or not all(isinstance(x, int) for x in defen)
    ):
        raise ValidationError(f"round[{idx}][1] defen は長さ4の整数配列である必要があります")

    tile_counts: Dict[int, int] = {}

    for arr_idx in (2, 3):
        arr = rd[arr_idx]
        if not isinstance(arr, list) or not all(isinstance(x, int) and 11 <= x <= 47 for x in arr):
            raise ValidationError(f"round[{idx}][{arr_idx}] は11<=牌<=47の整数配列である必要があります")
        for x in arr:
            tile_counts[x] = tile_counts.get(x, 0) + 1

    # starting hands
    for pos in range(4, 8):
        hand = rd[pos]
        if not isinstance(hand, list) or not all(isinstance(x, int) and 11 <= x <= 47 for x in hand):
            raise ValidationError(f"round[{idx}][{pos}] は11<=牌<=47の整数配列である必要があります")
        for x in hand:
            tile_counts[x] = tile_counts.get(x, 0) + 1

    # per-player action arrays
    for pos in range(8, len(rd) - 1):
        arr = rd[pos]
        if not isinstance(arr, list):
            raise ValidationError(f"round[{idx}][{pos}] は配列である必要があります")
        for item in arr:
            if isinstance(item, int):
                if not 11 <= item <= 47:
                    raise ValidationError(f"round[{idx}][{pos}] の牌番号は11<=x<=47である必要があります")
                tile_counts[item] = tile_counts.get(item, 0) + 1
            elif not isinstance(item, str):
                raise ValidationError(f"round[{idx}][{pos}] の要素は整数か文字列である必要があります")

    for tile, cnt in tile_counts.items():
        if cnt > 4:
            raise ValidationError(f"round[{idx}] 牌番号{tile}が{cnt}回出現しています（上限4）")

    end = rd[-1]
    if not isinstance(end, list) or not isinstance(end[0], str):
        raise ValidationError(f"round[{idx}] の終局情報は文字列先頭の配列である必要があります")
    if end[0] in {"流局", "liuju"}:
        if len(end) != 1:
            raise ValidationError(f"round[{idx}] 流局 は要素1のみである必要があります")
    elif end[0] in {"和了", "hule"}:
        if (
            len(end) < 2
            or not (isinstance(end[1], list) and len(end[1]) == 4 and all(isinstance(x, int) for x in end[1]))
        ):
            raise ValidationError(f"round[{idx}] 和了 の点数配列は長さ4の整数配列である必要があります")
    else:
        raise ValidationError(f"round[{idx}] 終局情報 name は liuju/流局 または hule/和了 のいずれかである必要があります")


def load_and_validate(path: str) -> None:
    """Load ``path`` as JSON and validate it."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    validate_tenhou(data)
    print(f"{path} のバリデーションに成功しました")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使い方: python -m core.tenhou_validator <ファイル名>")
        raise SystemExit(1)
    load_and_validate(sys.argv[1])
