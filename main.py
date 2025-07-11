import io
import csv
from datetime import datetime
import math
import matplotlib.pyplot as plt
DATE = '20250709'
def draw_trajectory(data, linear_speed, angular_speed_deg):
    """
    ログデータを解析し、軌跡を描画する関数

    Args:
        data (str): ログデータの文字列
        linear_speed (float): 1秒あたりの移動速度 (単位/秒)
        angular_speed_deg (float): 1秒あたりの旋回速度 (度/秒)
    """
    
    commands = []
    for row in data:
        # datetimeはマイクロ秒まで対応しているISOフォーマット
        timestamp_str = row[0]
        key = row[1].replace('"', '').strip()

        dt_object = datetime.fromisoformat(timestamp_str)
        commands.append((dt_object, key))

    # 初期状態
    x, y = 0.0, 0.0
    # 角度はラジアンで管理 (90度、つまりY軸プラス方向を初期向きとする)
    angle = math.pi / 2  
    # 旋回速度を度からラジアンに変換
    angular_speed_rad = math.radians(angular_speed_deg)

    # 軌跡を保存するリスト
    path_x = [x]
    path_y = [y]

    # 最初のコマンドは次のコマンドまでの動作を決定する
    for i in range(len(commands) - 1):
        start_time, key = commands[i]
        end_time, _ = commands[i+1]
        
        # 動作時間（秒）
        delta_t = (end_time - start_time).total_seconds()
        
        # キー入力に応じた処理
        if key == 'w':  # 前進
            x += linear_speed * math.cos(angle) * delta_t
            y += linear_speed * math.sin(angle) * delta_t
        elif key == 'x':  # 後進
            x -= linear_speed * math.cos(angle) * delta_t
            y -= linear_speed * math.sin(angle) * delta_t
        elif key == 'a':  # 左旋回
            angle += angular_speed_rad * delta_t
        elif key == 'd':  # 右旋回
            angle -= angular_speed_rad * delta_t
        elif key == 's':  # 停止
            # 位置も角度も変わらない
            pass

        path_x.append(x)
        path_y.append(y)

    # 軌跡の描画
    plt.figure(figsize=(10, 8))
    plt.plot(path_x, path_y, marker='o', linestyle='-', markersize=3, label='Trajectory')
    plt.plot(path_x[0], path_y[0], 'go', markersize=10, label='Start') # 開始点
    plt.plot(path_x[-1], path_y[-1], 'ro', markersize=10, label='End') # 終了点
    
    plt.title(F'speed={linear_speed:.2f}m/s, turn speed ={angular_speed_deg}°/s')
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box') # アスペクト比を1:1に
    plt.legend()
    
    # ファイルに保存
    plt.savefig(f'./output/{DATE}/{linear_speed:.2f}m,{angular_speed_deg}deg.png')
    print("軌跡の画像を保存")

# ----- ここから実行 -----
if __name__ == '__main__':
    data = []
    try:
        with open(f'./data/20250709/socket_log_20250709_130428.csv', 'r', encoding='utf-8', newline='') as file:
        # csvリーダーオブジェクトを作成
            csv_reader = csv.reader(file)
        
        # forループで一行ずつデータを処理
            for row in csv_reader:
            # rowは各列のデータが格納されたリスト
            # 例: ['2025-07-09 13:52:36.896223', ' "x"']
                #print(row)
                data.append(row)
            # 各データにアクセスする場合
            timestamp = row[0]
            value = row[1].strip() # 前後の空白を削除
            #print(f"日時: {timestamp}, 値: {value}")
            
    except FileNotFoundError:
        print("log.csvファイルが見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    # 描画関数の実行
    for i in range(10):
        for j in range(100):
            draw_trajectory(data, 0.1 + i*0.1, 14 + 0.1*j)