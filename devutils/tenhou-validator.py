#!/usr/bin/env python3
import json
import sys
import re
from typing import Any, Dict, List, Union

# Validation error
class ValidationError(Exception):
    pass

# Allowed end reasons
END_REASONS = {
    "和了", "流局", "全員不聴", "九種九牌", "四槓散了", "四家立直", "不明"
}

# Tile codes
VALID_TILES_NUM = set(
    [0, 60] +
    list(range(11, 20)) +  # Manzu 1–9
    list(range(21, 30)) +  # Pinzu 1–9
    list(range(31, 40)) +  # Souzu 1–9
    list(range(41, 48)) +  # Honors East–Dragon
    [51, 52, 53]           # Red fives
)
# For 初期配牌 (hai): no 0 or 60
VALID_TILES_HAI = VALID_TILES_NUM - {0, 60}

# Meld/discard codes: allow digits plus p/c/m/k/a/r
RE_MELD = re.compile(r'^[0-9apcmkr]+$')

def load_json(path: str) -> Any:
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def validate_top(obj: Any) -> None:
    if not isinstance(obj, dict):
        raise ValidationError("トップレベルはオブジェクトである必要があります")

    # title
    title = obj.get("title")
    if not (isinstance(title, list) and len(title) == 2 and all(isinstance(x, str) for x in title)):
        raise ValidationError("`title` は長さ2の文字列配列である必要があります")

    # name
    name = obj.get("name")
    if not (isinstance(name, list) and len(name) == 4 and all(isinstance(x, str) for x in name)):
        raise ValidationError("`name` は長さ4の文字列配列である必要があります")

    # rule
    rule = obj.get("rule")
    if not isinstance(rule, dict):
        raise ValidationError("`rule` はオブジェクトである必要があります")
    disp = rule.get("disp")
    if not (isinstance(disp, str)):
        raise ValidationError("`rule.disp` は文字列である必要があります")
    has_aka = "aka" in rule
    has_aka_specific = all(k in rule for k in ("aka51", "aka52", "aka53"))
    if not (has_aka ^ has_aka_specific):
        raise ValidationError("`rule` は `aka` または (`aka51`,`aka52`,`aka53`) のいずれか一方を持つ必要があります")
    if has_aka:
        aka = rule["aka"]
        if not (isinstance(aka, int) and aka >= 0):
            raise ValidationError("`rule.aka` は0以上の整数である必要があります")
    else:
        for k in ("aka51", "aka52", "aka53"):
            v = rule[k]
            if not (isinstance(v, int) and v >= 0):
                raise ValidationError(f"`rule.{k}` は0以上の整数である必要があります")

def validate_hand(hand: Any, idx: int) -> None:
    if not isinstance(hand, list):
        raise ValidationError(f"round[{idx}] は配列である必要があります")
    if len(hand) != 17:
        raise ValidationError(f"round[{idx}] の要素数は17である必要があります (found {len(hand)})")

    # 0: [kyoku, honba, kyotaku]
    info = hand[0]
    if not (isinstance(info, list) and len(info) == 3 and all(isinstance(x, int) and x >= 0 for x in info)):
        raise ValidationError(f"round[{idx}][0] は0以上の整数3要素配列である必要があります")

    # 1: scores
    scores = hand[1]
    if not (isinstance(scores, list) and len(scores) == 4 and all(isinstance(x, int) for x in scores)):
        raise ValidationError(f"round[{idx}][1] は長さ4の整数配列である必要があります")

    # 2,3: dora indicators
    for pos, name in ((2, "表ドラ"), (3, "裏ドラ")):
        arr = hand[pos]
        if not (isinstance(arr, list) and all(isinstance(x, int) and x in VALID_TILES_HAI for x in arr)):
            raise ValidationError(f"round[{idx}][{pos}] {name} は有効な牌コード整数配列です")

    # 4–15: players 0..3 blocks of [hai, take, dahai]
    for p in range(4):
        base = 4 + p*3
        # hai
        hai = hand[base]
        if not (isinstance(hai, list) and len(hai) == 13 and all(isinstance(x, int) and x in VALID_TILES_HAI for x in hai)):
            raise ValidationError(f"round[{idx}] player{p} の配牌 (idx {base}) は長さ13の有効牌整数配列です")
        # take
        take = hand[base+1]
        if not isinstance(take, list):
            raise ValidationError(f"round[{idx}] player{p} の取牌 (idx {base+1}) は配列である必要があります")
        for t in take:
            if isinstance(t, int):
                if t not in VALID_TILES_NUM:
                    raise ValidationError(f"round[{idx}] player{p} の取牌に無効な牌コード: {t}")
            elif isinstance(t, str):
                if not RE_MELD.match(t):
                    raise ValidationError(f"round[{idx}] player{p} の取牌に無効な文字列表現: {t}")
            else:
                raise ValidationError(f"round[{idx}] player{p} の取牌は整数または文字列である必要があります")
        # dahai
        dahai = hand[base+2]
        if not isinstance(dahai, list):
            raise ValidationError(f"round[{idx}] player{p} の打牌 (idx {base+2}) は配列である必要があります")
        for d in dahai:
            if isinstance(d, int):
                if d not in VALID_TILES_NUM:
                    raise ValidationError(f"round[{idx}] player{p} の打牌に無効な牌コード: {d}")
            elif isinstance(d, str):
                if not RE_MELD.match(d):
                    raise ValidationError(f"round[{idx}] player{p} の打牌に無効な文字列表現: {d}")
            else:
                raise ValidationError(f"round[{idx}] player{p} の打牌は整数または文字列である必要があります")

    # 16: end info
    end = hand[16]
    if not (isinstance(end, list) and len(end) >= 1 and isinstance(end[0], str) and end[0] in END_REASONS):
        raise ValidationError(f"round[{idx}][16] は有効な終局パターンである必要があります")
    # diff
    if len(end) >= 2:
        diff = end[1]
        if not (isinstance(diff, list) and len(diff) == 4 and all(isinstance(x, int) for x in diff)):
            raise ValidationError(f"round[{idx}] の diff は長さ4の整数配列である必要があります")
    # win info
    if len(end) >= 3 and end[0] == "和了":
        win = end[2]
        if not (isinstance(win, list) and len(win) >= 4):
            raise ValidationError(f"round[{idx}] の和了情報は要素4以上の配列である必要があります")
        # first three are ints, fourth is string
        if not all(isinstance(win[i], int) for i in range(3)):
            raise ValidationError(f"round[{idx}] の和了情報最初の3要素は整数である必要があります")
        if not isinstance(win[3], str):
            raise ValidationError(f"round[{idx}] の和了情報4番目は文字列である必要があります")

def validate(log: Any) -> None:
    validate_top(log)
    hands = log.get("log")
    if not isinstance(hands, list):
        raise ValidationError("`log` は配列である必要があります")
    for i, hand in enumerate(hands):
        validate_hand(hand, i)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/log.json")
        sys.exit(1)
    path = sys.argv[1]
    data = load_json(path)
    try:
        validate(data)
    except ValidationError as e:
        print(f"✗ ValidationError: {e}")
        sys.exit(1)
    print("✓ Validation succeeded")

if __name__ == "__main__":
    main()
