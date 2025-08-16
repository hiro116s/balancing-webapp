import io
import json

def solve_item_combination_to_json(data):
    """
    与えられたアイテムのリストから、各総重量の剰余(0-999)を
    達成するための最小アイテム数の組み合わせを計算し、JSON形式で出力します。

    Args:
        data (str): '(アイテム名,重量)' の形式のテキストデータ。
    """
    items = []
    # 1. テキストデータを解析し、(名前, 重さ) のタプルのリストを作成
    for line in io.StringIO(data).readlines():
        line = line.strip()
        if line:
            parts = line.split(',')
            name = parts[0]
            weight = int(parts[1])
            items.append((name, weight))

    # 2. 動的計画法（DP）テーブルの初期化
    # dp[k] = (最小アイテム数, アイテム名のリスト, 総重量)
    dp = [(float('inf'), [], 0) for _ in range(1000)]
    dp[0] = (0, [], 0)

    # 3. 各アイテムを順番に見てDPテーブルを更新
    for name, weight in items:
        for j in range(999, -1, -1):
            if dp[j][0] != float('inf'):
                current_count, current_list, current_total_weight = dp[j]
                
                new_total_weight = current_total_weight + weight
                new_k = new_total_weight % 1000
                new_count = current_count + 1
                
                if new_count < dp[new_k][0]:
                    new_list = current_list + [name]
                    dp[new_k] = (new_count, new_list, new_total_weight)

    # 4. 結果をJSON用のリストに格納
    results = []
    for k in range(1000):
        num_items, item_list, total_weight = dp[k]
        
        # 到達不可能な場合は、数値を0、リストを空にする
        if num_items == float('inf'):
            num_items = 0
            total_weight = 0
            item_list = []
        
        # 指定されたフィールド名で辞書を作成
        result_obj = {
            "k": k,
            "n": num_items,
            "total_weight": total_weight,
            "items": item_list
        }
        results.append(result_obj)
        
    # 5. リストをJSON形式の文字列に変換して出力
    # ensure_ascii=False で日本語の文字化けを防ぎ、indent=2 で整形
    print(json.dumps(results, ensure_ascii=False, indent=2))


# 提供されたテキストデータを変数に格納
input_data = """
円筒小(クリーム色),225
円筒小(クリーム色),225
円筒小(黄色),225
円筒小(KOKIN-CHAN),230
円筒小(メロンぱんまん),230
円筒小(カレーぱんまん),238
円筒小(DADANDAN),238
円筒大(青色),358
円筒大(ピンク色),358
円筒大(緑色),358
円筒大(黄色),347
ばいきんまん,430
あんぱんまん,420
立方体(クリーム色),220
立方体(クリーム色),220
立方体(クリーム色),220
立方体(クリーム色),220
立方体(クリーム色),220
直方体(クリーム色),345
直方体(クリーム色),345
直方体(黄色),345
直方体(ジャムおじさんとなぞの顔),355
三角柱(緑色),440
三角柱(黄色),457
三角柱(クリーム色),457
三角柱(クリーム色),457
ハーフパイプ(ピンク色),392
ハーフパイプ(クリーム色),392
四角いドーナツ(青色),651
四角いドーナツ(ピンク色),663
丸いドーナツ(黄色),446
大きい四角中(クリーム色),569
ハーフパイプ２個(緑色),705
チョコレート,268
"""

# プログラムを実行
solve_item_combination_to_json(input_data)
