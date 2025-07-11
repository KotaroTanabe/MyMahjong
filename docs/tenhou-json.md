**AIによる解説をベースにしているため、誤りが含まれる場合があります。**

# Tenhou.net/6 JSON Log Format
This document describes the structure of the JSON logs output by the
`events_to_tenhou_json` helper in the **core** package. The format is
modeled after the logs produced by `tenhou.net/6`.

Logs can be generated directly from engine events or converted from a
newline separated MJAI log using the `mjai_log_to_tenhou_json` helper.

## Overview

A log object has four top-level keys:

```json
{
  "title": ["", ""],
  "name": ["A", "B", "C", "D"],
  "rule": {"disp": "MyMahjong", "aka": 0},
  "log": []
}
```

- `title` – metadata embedded at the start of the long replay URL.
- `name` – player names in table order.
- `rule` – rule display string and red dora count.
- `log` – an array of per-hand records.

## Hand Array

Each hand is represented as an array. Elements are:

1. `[kyoku, honba, kyotaku]` – kyoku, honba count and riichi
   stick count.
2. `[score0, score1, score2, score3]` – starting scores.
3. `[dora1, dora2, ...]` – numeric tile codes for dora indicators.
4. `[ura1, ura2, ...]` – numeric tile codes for ura dora indicators.
5. `[hai0_1, …, hai0_13]` – starting hand for player 0.
6. `[take0_1, …, take0_n]` - taken tile for player 0.
7. `[dahai0_1, …, dahai0_m]` - discarded tile for player 0.
8. `[hai1_1, …, hai1_13]` – starting hand for player 1.
9. `[take1_1, …, take1_n]` – taken tile for player 1.  
10. `[dahai1_1, …, dahai1_m]` – discarded tile for player 1.  
11. `[hai2_1, …, hai2_13]` – starting hand for player 2.  
12. `[take2_1, …, take2_n]` – taken tile for player 2.  
13. `[dahai2_1, …, dahai2_m]` – discarded tile for player 2.  
14. `[hai3_1, …, hai3_13]` – starting hand for player 3.  
15. `[take3_1, …, take3_n]` – taken tile for player 3.  
16. `[dahai3_1, …, dahai3_m]` – discarded tile for player 3.
17. `["和了", [Δ0, Δ1, Δ2, Δ3], result_info]` – win result,
    `["流局", [Δ0, Δ1, Δ2, Δ3]]` - drawn (someone is tenpai), or
    `["(end reason)"]` - drawn, no point difference. "(end reason)"="全員不聴", "九種九牌", "四槓散了", ...

`result_info` is an array used by `tenhou.net/6` to describe the
winning hand.  It typically begins with the winning player index and
the losing player (or the winner again when tsumo) followed by the hand
value string and yaku list.

Tiles use the numeric codes from `tenhou.net/6`:

```
11–19: characters
21–29: circles
31–39: bamboo
41–47: honor tiles
51-53: aka 5 hai (man for 51, pin for 52, sou for 53)
```

Meld calls such as chi, pon and kan are encoded as strings beginning with
`c`, `p` or `m` followed by the tile codes, for example `c111213` for
a chi using 1-2-3 characters. The `result_info` array lists the winning
and losing players, a hand value string and the yaku.

Our implementation currently supports only a subset of this
specification:

- Ura dora indicators are recorded but only revealed in the log when a
  hand is won.
- The result array stores only score deltas and a simple win record
  without detailed point strings or yaku information.

Despite these limitations, the produced logs can be consumed by tools
expecting the basic `tenhou.net/6` structure.

## Legends
```jsonc
{
  "title": [ string /* タイトル用文字列１ */, string /* タイトル用文字列２ */ ],
  "name": [ string /* 東家（起家） */, string /* 南家 */, string /* 西家 */, string /* 北家 */ ],
  "rule": {
    "disp": string /* ルール表示名（任意プロパティ）（例："般南喰赤"） */,
    /* --- 以下いずれか一方を必須 --- */
    // 形式A: 赤ドラ数を一律で指定
    "aka":  number /* 赤ドラ使用数 */,
    // 形式B: 赤ドラを個別で指定
    "aka51": number /* 赤５萬使用数 */,
    "aka52": number /* 赤５筒使用数 */,
    "aka53": number /* 赤５索使用数 */,
  },
  "log": [
    /* 以下を局数分繰り返し */
    [
      /* 0: 局情報 */
      [ 
        kyoku_num    /* 場風は0~3=東,4~7=南,8~11=西,12~15=北. n%4が局数*/, 
        honba_num     /* 本場数 */,
        kyotaku_num   /* 供託リーチ棒数 */
      ],

      /* 1: 局開始時点の持ち点（４要素） */
      [ score0, score1, score2, score3 ],

      /* 2: 表ドラ表示牌（数値コードの配列） */
      [ dora1, dora2, … ],

      /* 3: 裏ドラ表示牌（同上） */
      [ ura1, ura2, … ],

      /* 4–6: player 0（起家） */
      [hai0_1, …, hai0_13],   /* 配牌13枚 */
      [take0_1, …, take0_n0],   /* 取牌一覧 （ツモ牌、嶺上牌、または他家から鳴いた牌） */
      [dahai0_1, …, dahai0_m0],  /* 打牌一覧 （捨てた牌、または加槓・暗槓した牌） */
      /* 打牌数は、ツモ和了時や九種九牌宣言時は(取牌数-1)枚。それ以外は取牌と同数) */

      /* 7–9: player 1（player 0 の下家, i.e. 東1局時点での南家） */
      [hai1_1, …, hai1_13],
      [take1_1, …, take1_n1],
      [dahai1_1, …, dahai1_m1],

      /* 10–12: player 2（player 0 の対面, i.e. 東1局時点での西家） */
      [hai2_1, …, hai2_13],
      [take2_1, …, take2_n2],
      [dahai2_1, …, dahai2_m2],

      /* 13–15: player 3（player 0 の上家, i.e. 東1局時点での北家） */
      [hai3_1, …, hai3_13],
      [take3_1, …, take3_n3],
      [dahai3_1, …, dahai3_m3],

      /* 牌コード
        0: スキップ（取牌が大明槓のときのみ、出牌としてこれを使用する）
        11-19: マンズ1-9
        21-29: ピンズ1-9
        31-39: ソーズ1-9
        41-47: 字牌（東南西北白發中）
        51: 赤５萬
        52: 赤５筒
        53: 赤５索
        60: ツモ切り

        // 鳴き・リーチ表現
        // 取牌の表現
        p: ポン牌（例："4545p45"は下家からポンした牌が白）
        c: チー牌（例："c252627"は上家からチーした牌が５筒、自分が出したのが６７筒）
        m: 大明カン牌（例："25m252525"は上家からカンした牌が５筒。大明槓に対応する出牌は`0`(skip)）
        誰から鳴いたかにより、`p`, `m`の出現位置が変わります。(`c`は上家しか行えないため固定)
        鳴きの種類を`x`, 牌を`h1`,`h2`,`h3`としたとき、
        上家から`h1`を鳴いた場合は`xh1h2h3`
        対面から`h2`を鳴いた場合は`h1xh2h3`
        下家から`h3`を鳴いた場合は`h1h2xh3`
        大明カン`m`の場合は牌が4つになります。牌を`h0`（※4つすべて同じ牌）としたとき、
        上家から`h0`を鳴いた場合は`mh0h0h0h0`
        対面から`h0`を鳴いた場合は`h0mh0h0h0`
        下家から`h0`を鳴いた場合は`h0h0mh0h0`

        // 出牌の表現
        k: 加カン牌（例："2525k2525"は対面からポンした５筒３枚に対して加カン。加カンは出牌側に記載）
        a: 暗カン牌（例："252525a52"はそのプレイヤー自身がカンした牌が５筒３枚+赤５筒. アンカンは出牌側に記載し、リンシャンは次の取牌）
        r: リーチ牌（例："r12"はリーチ宣言した牌が２萬）
      // 加槓・暗槓の表現
        上家から鳴いた`h0`に加槓した場合は`kh0h0h0h0h0`
        対面から鳴いた`h0`に加槓した場合は`h0kh0h0h0h0`
        下家から鳴いた`h0`に加槓した場合は`h0h0kh0h0h0`
        暗槓(`a`)の場合は自分の牌を鳴く扱いとなるため、`h0h0h0ah0`となります。

        */
        [
          end_pattern_str, /* "和了", "流局", "全員不聴", "九種九牌", "四槓散了",　"四家立直", "不明" */
          [ diff0, diff1, diff2, diff3 ],          /* 1: 点数の増減（なければ省略） */
          /* 2: 和了情報（和了時限定） */
          [
            win_player, /* 和了者のplayer number */
            deal_in_player, /* 放銃者のplayer number（ツモ和了時は和了者を記入） */
            win_player, /* 和了者のplayer number（重複理由は不明） */
            point_str, /* 例："跳満3000-6000点", */
            ...yaku_str[] /*  例："立直(1飜)", "門前清自摸和(1飜)", "ドラ(3飜)", "赤ドラ(1飜)" */
          ]
          /* ダブロンの場合は、上記のdiff, 和了情報をもう１セット記入する */
        ]
    ],
    /* 以上を局数分繰り返す */
  ]
}
```

## Example JSON data
[牌譜サンプル | 嶺上ツモ](https://tenhou.net/6/#json=%7B%22title%22%3A%5B%22%22,%22%22%5D,%22name%22%3A%5B%22A%E3%81%95%E3%82%93%22,%22B%E3%81%95%E3%82%93%22,%22C%E3%81%95%E3%82%93%22,%22D%E3%81%95%E3%82%93%22%5D,%22rule%22%3A%7B%22disp%22%3A%22%E8%88%AC%E5%8D%97%E5%96%B0%E8%B5%A4%22,%22aka%22%3A1%7D,%22log%22%3A%5B%5B%5B5,0,0%5D,%5B29300,2700,48500,19500%5D,%5B32,11%5D,%5B43,38%5D,%5B11,12,12,12,14,15,18,24,52,33,35,36,43%5D,%5B45,24,32,14,25,23,21,29%5D,%5B43,18,11,45,15,32,60,60%5D,%5B14,17,17,23,34,34,34,41,42,43,46,46,47%5D,%5B21,27,27,27,25,29,44,23,37%5D,%5B43,42,14,47,41,60,60,21,60%5D,%5B11,18,19,22,24,28,28,37,39,39,41,42,43%5D,%5B21,41,38,45,17,27,13,47,13%5D,%5B43,42,39,11,45,28,24,13,60%5D,%5B13,13,16,17,24,31,31,32,33,35,53,39,39%5D,%5B22,19,25,35,16,16,12,28,16,26%5D,%5B31,60,39,39,22,%22r17%22,60,60,%22161616a16%22%5D,%5B%22%E5%92%8C%E4%BA%86%22,%5B-2000,-4000,-2000,9000%5D,%5B3,3,3,%22%E6%BA%80%E8%B2%AB2000-4000%E7%82%B9%22,%22%E7%AB%8B%E7%9B%B4(1%E9%A3%9C)%22,%22%E5%B6%BA%E4%B8%8A%E9%96%8B%E8%8A%B1(1%E9%A3%9C)%22,%22%E9%96%80%E5%89%8D%E6%B8%85%E8%87%AA%E6%91%B8%E5%92%8C(1%E9%A3%9C)%22,%22%E3%83%89%E3%83%A9(1%E9%A3%9C)%22,%22%E8%B5%A4%E3%83%89%E3%83%A9(1%E9%A3%9C)%22%5D%5D%5D%5D%7D&ts=0)より
```json
{"title":["",""],"name":["Aさん","Bさん","Cさん","Dさん"],"rule":{"disp":"般南喰赤","aka":1},"log":[[[5,0,0],[29300,2700,48500,19500],[32,11],[43,38],[11,12,12,12,14,15,18,24,52,33,35,36,43],[45,24,32,14,25,23,21,29],[43,18,11,45,15,32,60,60],[14,17,17,23,34,34,34,41,42,43,46,46,47],[21,27,27,27,25,29,44,23,37],[43,42,14,47,41,60,60,21,60],[11,18,19,22,24,28,28,37,39,39,41,42,43],[21,41,38,45,17,27,13,47,13],[43,42,39,11,45,28,24,13,60],[13,13,16,17,24,31,31,32,33,35,53,39,39],[22,19,25,35,16,16,12,28,16,26],[31,60,39,39,22,"r17",60,60,"161616a16"],["和了",[-2000,-4000,-2000,9000],[3,3,3,"満貫2000-4000点","立直(1飜)","嶺上開花(1飜)","門前清自摸和(1飜)","ドラ(1飜)","赤ドラ(1飜)"]]]]}
```

## Validation

The `core.tenhou_validator` module provides a simple checker that ensures
logs follow this specification.

Validate a JSON log file with:

```bash
python devutils/tenhou_validator.py path/to/log.json
```
