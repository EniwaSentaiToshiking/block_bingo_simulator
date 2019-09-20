# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: py3.7.4
#     language: python
#     name: py3.7.4
# ---

# ## ビンゴブロックエリアとルールを元にした情報

# ## 仮想ビングブロックエリアの初期化
#
# ### random.seedの値を変更してもらえると組み合わせが変わります
# #### 常にバラバラな初期化を求めるあなた randam.seedをコメントアウトすればOKです

# + {"code_folding": [64, 149, 188]}
# ダイクストラ法 Left


INF = 10000000

yel = 'yellow'
gre = 'green'
blu = 'blue'
red = 'red'
bla = 'black'

# 走行体の方角
north = "North"
north_east = "Northeast"
east = "East"
south_east = "Southeast"
south = "South"
south_west = "Southwest"
west = "West"
north_west = "Northwest"



blocks_color = [yel, yel, gre, gre,  blu, blu,  red, red, bla]

block_bingo_area = [
(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
    
(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
    
(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
    
(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
    
(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
    
(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
    
(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
]

crosscircle_positions = [
(0, 0), (0, 2), (0, 4), (0, 6),
(2, 0), (2, 2), (2, 4), (2, 6),
(4, 0), (4, 2), (4, 4), (4, 6),
(6, 0), (6, 2), (6, 4), (6, 6)
]

blockcircle_positions = [
(1,1), (1,3), (1,5), (3,1), (3,5), (5,1), (5,3), (5,5)# 1,2,3,4,5,6,7,8
]

## ここがほしみ
first_set_block_positions = [
(0,0), (2,2), (4,0), (6,2), (0,4), (2,6), (4,4), (6,6)
]

first_set_colorblock_number = 8 #ここは数字でいただける？
first_set_blackblock_number = 6 # 黒ブロックが初期化で置かれるブロックサークルの位置

bonus_number = 4
##

#エッジの生成
block_bingo_area_edge=[
    # (j,i) -> (j, i+2) 右方向のエッジ
    ((0, 0), (0, 2),1), ((0, 2), (0, 4),1), ((0, 4), (0, 6),1),
    ((2, 0), (2, 2),1), ((2, 2), (2, 4),1), ((2, 4), (2, 6),1),
    ((4, 0), (4, 2),1), ((4, 2), (4, 4),1), ((4, 4), (4, 6),1),
    ((6, 0), (6, 2),1), ((6, 2), (6, 4),1), ((6, 4), (6, 6),1),
    # (j,i) -> (j, i-2) 左方向エッジ
    ((0, 6), (0, 4),1), ((0, 4), (0, 2),1), ((0, 2), (0, 0),1),
    ((2, 6), (2, 4),1), ((2, 4), (2, 2),1), ((2, 2), (2, 0),1),
    ((4, 6), (4, 4),1), ((4, 4), (4, 2),1), ((4, 2), (4, 0),1),
    ((6, 6), (6, 4),1), ((6, 4), (6, 2),1), ((6, 2), (6, 0),1),
    # (j,i) -> (j+2,i) 上方向エッジ
    ((0, 0), (2, 0),1), ((2, 0), (4, 0),1), ((4, 0), (6, 0),1),
    ((0, 2), (2, 2),1), ((2, 2), (4, 2),1), ((4, 2), (6, 2),1),
    ((0, 4), (2, 4),1), ((2, 4), (4, 4),1), ((4, 4), (6, 4),1),
    ((0, 6), (2, 6),1), ((2, 6), (4, 6),1), ((4, 6), (6, 6),1),
    # (j,i) -> (j-2,i) 下方向エッジ
    ((6, 0), (4, 0),1), ((4, 0), (2, 0),1), ((2, 0), (0, 0),1),
    ((6, 2), (4, 2),1), ((4, 2), (2, 2),1), ((2, 2), (0, 2),1),
    ((6, 4), (4, 4),1), ((4, 4), (2, 4),1), ((2, 4), (0, 4),1),
    ((6, 6), (4, 6),1), ((4, 6), (2, 6),1), ((2, 6), (0, 6),1),   
    #特殊エッジ交点サークルからブロックサークル
    ((0, 0), (1, 1),1), ((0, 2), (1, 1),1), ((0, 2), (1, 3),1), ((0, 4), (1, 3),1), ((0, 4), (1, 5),1), ((0, 6), (1, 5),1),
    
    ((2, 0), (1, 1),1), ((2, 2), (1, 1),1), ((2, 2), (1, 3),1), ((2, 4), (1, 3),1), ((2, 4), (1, 5),1), ((2, 6), (1, 5),1),
    ((2, 0), (3, 1),1), ((2, 2), (3, 1),1),                                                                ((2, 4), (3, 5),1), ((2, 6), (3, 5),1),
    
    ((4, 0), (3, 1),1), ((4, 2), (3, 1),1),                                                                ((4, 4), (3, 5),1), ((4, 6), (3, 5),1),
    ((4, 0), (5, 1),1), ((4, 2), (5, 1),1), ((4, 2), (5, 3),1), ((4, 4), (5, 3),1), ((4, 4), (5, 5),1), ((4, 6), (5, 5),1),
    
    ((6, 0), (5, 1),1), ((6, 2), (5, 1),1), ((6, 2), (5, 3),1), ((6, 4), (5, 3),1), ((6, 4), (5, 5),1), ((6, 6), (5, 5),1),
]


import networkx as nx # 経路探索用
import random #組み合わせよう
random.seed(42)

Graph = nx.DiGraph()

def init_block_bingo_areaL():
    # ブロックビンゴエリアの必要な情報を仮想ビンゴブロックエリアに追加していく
    Graph.add_nodes_from(block_bingo_area)

    for blockcircle_num, position in enumerate(blockcircle_positions, start=1):
        Graph.nodes[position]['set_block'] = False
        #Graph.nodes[position]['set_blackblock'] = False
        
        Graph.nodes[position]['blockcircle_number'] = blockcircle_num
        if position in {(1,1), (3,5)}: 
            Graph.nodes[position]['set_blockcircle_color'] = yel
        elif position in {(1,3), (5,1)}: 
             Graph.nodes[position]['set_blockcircle_color'] = gre
        elif position in {(1,5), (5,3)}:
             Graph.nodes[position]['set_blockcircle_color'] = red
        elif position in {(3,1), (5,5)}:
             Graph.nodes[position]['set_blockcircle_color'] = blu

        if blockcircle_num == first_set_colorblock_number:
            Graph.nodes[position]['set_block'] = True
            Graph.nodes[position]['set_blockcolor'] =  Graph.nodes[position]['set_blockcircle_color']

        if blockcircle_num == first_set_blackblock_number:
            Graph.nodes[position]['set_blockcolor'] = bla
           # Graph.nodes[position]['set_blackblock'] = True

    # 初期化の時，ブロックサークル上に置かれているブロックの色を特定，排除
    first_set_colorblock_postion = blockcircle_positions[first_set_colorblock_number-1]
    colorblock = Graph.nodes[first_set_colorblock_postion]['set_blockcircle_color']
    blocks_color.remove(colorblock)
    crosscircle_blockcolors = random.sample(blocks_color, 8)
    print('init put crosscircle blocks {} .\n'.format(crosscircle_blockcolors))
    
    #　交点サークル上にブロックを配置
    for color, position in enumerate(first_set_block_positions, start=0):
        Graph.nodes[position]['set_block'] = True
        Graph.nodes[position]['set_blockcolor'] = crosscircle_blockcolors[color]
        
    Graph.add_weighted_edges_from(block_bingo_area_edge)
    
    
def init_block_bingo_areaR():
    # ブロックビンゴエリアの必要な情報を仮想ビンゴブロックエリアに追加していく
    Graph.add_nodes_from(block_bingo_area)

    for blockcircle_num, position in enumerate(blockcircle_positions, start=1):
        Graph.nodes[position]['set_block'] = False
        Graph.nodes[position]['set_blackblock'] = True
        
        Graph.nodes[position]['blockcircle_number'] = blockcircle_num
        if position in {(1,5), (3,1)}: 
            Graph.nodes[position]['set_blockcircle_color'] = yel
        elif position in {(1,3), (5,5)}:
             Graph.nodes[position]['set_blockcircle_color'] = gre
        elif position in {(1,1), (5,3)}:
             Graph.nodes[position]['set_blockcircle_color'] = red
        elif position in {(3,5), (5,1)}:
             Graph.nodes[position]['set_blockcircle_color'] = blu

        if blockcircle_num == first_set_colorblock_number:
            Graph.nodes[position]['set_block'] = True
            Graph.nodes[position]['set_blockcolor'] =  Graph.nodes[position]['set_blockcircle_color']

        if blockcircle_num == first_set_blackblock_number:
            Graph.nodes[position]['set_blockcolor'] = bla
           # Graph.nodes[position]['set_blackblock'] = True
        
        if blockcircle_num == bonus_number:
            Graph.nodes[position]['set_blackblock'] = False

    # 初期化の時，ブロックサークル上に置かれているブロックの色を特定，排除
    first_set_colorblock_postion = blockcircle_positions[first_set_colorblock_number-1]
    colorblock = Graph.nodes[first_set_colorblock_postion]['set_blockcircle_color']
    blocks_color.remove(colorblock)
    crosscircle_blockcolors = random.sample(blocks_color, 8)
    print('init put crosscircle blocks {} .\n'.format(crosscircle_blockcolors))
    
    #　交点サークル上にブロックを配置
    for color, position in enumerate(first_set_block_positions, start=0):
        Graph.nodes[position]['set_block'] = True
        Graph.nodes[position]['set_blockcolor'] = crosscircle_blockcolors[color]
        
    Graph.add_weighted_edges_from(block_bingo_area_edge)
    
def goto_path_and_direction(shortest_route_list=shortest_route['path'], start_direction=east):
    robots_direction = start_direction
    moving_robots = shortest_route_list
    for i in range(len(moving_robots)-1):
        print("進む経路 : {} -> {},  現在の走行体の方向: {}".format(moving_robots[i], moving_robots[i+1], robots_direction) )
        # 北 
        if moving_robots[i][0] > moving_robots[i+1][0] and moving_robots[i][1] == moving_robots[i+1][1]:
            print("次の走行体の方向: 北\n")
            robots_direction = north
        # 北東
        elif moving_robots[i][0] > moving_robots[i+1][0] and moving_robots[i][1] < moving_robots[i+1][1]:
            print("次の走行体の方向: 北東\n")
            robots_direction = north_west
        # 東
        elif moving_robots[i][0] == moving_robots[i+1][0] and moving_robots[i][1] < moving_robots[i+1][1]:
            print("次の走行体の方向: 東\n")
            robots_direction = west
        # 南東
        elif moving_robots[i][0] < moving_robots[i+1][0] and moving_robots[i][1] < moving_robots[i+1][1]:
            print("次の走行体の方向: 南東\n")
            robots_direction = south_west
        #  南
        elif moving_robots[i][1] == moving_robots[i+1][1] and moving_robots[i][0] < moving_robots[i+1][0] :
            print("次の走行体の方向: 南\n")
            robots_direction = south
        #　南西
        elif moving_robots[i][0] < moving_robots[i+1][0] and moving_robots[i][1] > moving_robots[i+1][1]:
            print("次の走行体の方向: 南西\n")
            robots_direction = south_east
        # 西
        elif moving_robots[i][0] == moving_robots[i+1][0] and moving_robots[i][1] > moving_robots[i+1][1]:
            print("次の走行体の方向: 西\n")
            robots_direction = east
        # 北西
        elif  moving_robots[i][0] > moving_robots[i+1][0] and moving_robots[i][1] > moving_robots[i+1][1]:
            print("次の走行体の方向: 北西\n")
            robots_direction = north_east
    


# -

# ### L, Rコースの最短探索経路を出す

# LかRのどちらかで初期化
init_block_bingo_areaR()

# + {"code_folding": []}
# start = (4,6) #L
start = (4,6) # R
start_direction = east
determine_route_count=0

check_b_circle_list = []
while(determine_route_count<8):
    determine_route_count += 1
    print("{}".format(determine_route_count))
    #交点サークル上のブロックとブロックサークルの色が同じ場合距離を計算する
    route_list=[]
    for block_position in first_set_block_positions: #　運ぶブロックの個数分
        if not Graph.nodes[block_position]['set_block']: #ブロックが置かれてなかったらその地点からは考えなくていいよね
            continue
        for blockcircle_position in blockcircle_positions:
            if Graph.nodes[block_position]['set_blockcolor'] == Graph.nodes[blockcircle_position]['set_blockcircle_color'] and Graph.nodes[blockcircle_position]['set_block'] == False: # カラーブロックの経路
                carry_color = Graph.nodes[block_position]['set_blockcolor']
                move_path = nx.dijkstra_path(Graph, source=start, target=block_position, weight='weight')
                carry_path =  nx.dijkstra_path(Graph, source=block_position, target=blockcircle_position, weight='weight')
                one_route_path = move_path+carry_path[1:]
                one_route_cost = len(move_path)+len(carry_path[1:])
                route_list.append({'path': one_route_path, 'cost':one_route_cost, 'block_on_crosscircle_pos':move_path[-1], 'carry_color': carry_color})
            elif Graph.nodes[blockcircle_position]['blockcircle_number'] == bonus_number and Graph.nodes[block_position]['set_blockcolor'] == bla: #黒ブロックの経路
                carry_color = Graph.nodes[block_position]['set_blockcolor']
                move_path = nx.dijkstra_path(Graph, source=start, target=block_position, weight='weight')
                carry_path =  nx.dijkstra_path(Graph, source=block_position, target=blockcircle_position, weight='weight')
                one_route_path = move_path+carry_path[1:]
                one_route_cost = len(move_path)+len(carry_path[1:]) +30
                route_list.append({'path': one_route_path, 'cost':one_route_cost, 'block_on_crosscircle_pos':move_path[-1], 'carry_color': carry_color})
    
    # 最小の1ルートを決定する
    shortest_route={'path':[], 'cost':INF}
    for route in route_list:
        #180度回転をなくす処理
        for idx in range(len(route['path'])-2):
            if route['path'][idx] == route['path'][idx+2]: # (0,2)->(2,2)->(0,2)みたいな移動は180ターン使わないと無理だよね　だから排除
                route['cost'] = INF
        if  route['cost'] < shortest_route['cost']:
            shortest_route = route
    print(shortest_route)
    
    ## 走行体が移動した時の状態を表示
    goto_path_and_direction(shortest_route_list=shortest_route['path'], start_direction=start_direction)
        
    #走行体の現在位置とブロックの状態を更新
    #走行体の現在位置を更新
    if shortest_route['cost'] < 150:
        start = shortest_route['path'][-2]
        check_b_circle_list.append(shortest_route['path'][-1])
        #ブロックの状態を更新
        # ブロックサークル
        placed_blockcircle_position = shortest_route['path'][-1]
        Graph.nodes[placed_blockcircle_position]['set_block'] = True
        Graph.nodes[placed_blockcircle_position]['set_blockcolor'] = shortest_route['carry_color']
        # 交点サークル
        removed_block4crosscircle_position = shortest_route['block_on_crosscircle_pos']
        Graph.nodes[removed_block4crosscircle_position]['set_block'] = False
        Graph.nodes[removed_block4crosscircle_position]['set_blockcolor'] = None

# -

first_set_colorblock_postion = blockcircle_positions[first_set_colorblock_number-1]
first_set_colorblock_postion, check_b_circle_list

# ## 素材置き場

one_route_path

# + {"code_folding": []}
# carry_path[1:],len(carry_path[1:])

for g in Graph.nodes(data=True):
    print(g)

# crosscircle_blockcolors
# Graph.nodes[blockcircle_position[first_set_colorblock_number-1]]['set_blockcircle_color']
# shortest_route={'path':[], 'cost':INF}
# for route in route_list:
#     if  route['cost'] < shortest_route['cost']:
#         shortest_route = route
# shortest_route

# for block_position in blockcircle_position:
#     print(block_position)
#     print(first_set_blackblock_number == Graph.nodes[block_position]['blockcircle_number'])
    
# for blockcir_position in blockcircle_position:
#     print(blockcir_position)
#     Graph.nodes[blockcir_position]['set_blockcircle_color']
# start = shortest_route['path'][-2]
# start
# removed_block4crosscircle_position

## 走行体が移動した時の方向を表示(静的)
# robots_direction = east
# moving_robots = shortest_route['path']
# for i in range(len(moving_robots)-1):
#     print("進む経路 : {} -> {},  現在の走行体の方向: {}".format(moving_robots[i], moving_robots[i+1], robots_direction) )
#     # 北 
#     if moving_robots[i][0] > moving_robots[i+1][0] and moving_robots[i][1] == moving_robots[i+1][1]:
#         print("次の走行体の方向: 北\n")
#         robots_direction = north
#     # 北東
#     elif moving_robots[i][0] > moving_robots[i+1][0] and moving_robots[i][1] < moving_robots[i+1][1]:
#         print("次の走行体の方向: 北東\n")
#         robots_direction = north_west
#     # 東
#     elif moving_robots[i][0] == moving_robots[i+1][0] and moving_robots[i][1] < moving_robots[i+1][1]:
#         print("次の走行体の方向: 東\n")
#         robots_direction = west
#     # 南東
#     elif moving_robots[i][0] < moving_robots[i+1][0] and moving_robots[i][1] < moving_robots[i+1][1]:
#         print("次の走行体の方向: 南東\n")
#         robots_direction = south_west
#     #  南
#     elif moving_robots[i][1] == moving_robots[i+1][1] and moving_robots[i][0] < moving_robots[i+1][0] :
#         print("次の走行体の方向: 南\n")
#         robots_direction = south
#     #　南西
#     elif moving_robots[i][0] < moving_robots[i+1][0] and moving_robots[i][1] > moving_robots[i+1][1]:
#         print("次の走行体の方向: 南西\n")
#         robots_direction = south_east
#     # 西
#     elif moving_robots[i][0] == moving_robots[i+1][0] and moving_robots[i][1] > moving_robots[i+1][1]:
#         print("次の走行体の方向: 西\n")
#         robots_direction = east
#     # 北西
#     elif  moving_robots[i][0] > moving_robots[i+1][0] and moving_robots[i][1] > moving_robots[i+1][1]:
#         print("次の走行体の方向: 北西\n")
#         robots_direction = north_east
    
# shortest_route, robots_direction
## test
# (4, 6) -> (4, 4)
# 北 -> 北
# (4, 4) -> (4, 2)
# 北 -> 北
# (4, 2) -> (6, 2)
# 北 -> 西
# (6, 2) -> (4, 2)
# 北 -> 南
# (4, 2) -> (2, 2)
# 北 -> 北

# + {"code_folding": [1]}
count=0
block_bingo_area_co_ro = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)],

    [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)],

    [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)],

    [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)],

    [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6)],

    [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)],

    [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
]

crosscircle_positions = [
    (0, 0), (0, 2), (0, 4), (0, 6),
    (2, 0), (2, 2), (2, 4), (2, 6),
    (4, 0), (4, 2), (4, 4), (4, 6),
    (6, 0), (6, 2), (6, 4), (6, 6),
]

blockcircle_positions_co_ro = [
    (1,1), (1,3), (1,5), 
    (3,1), (3,5), 
    (5,1), (5,3), (5,5)
    # 1,2,3,4,5,6,7,8
]

# print("[")
# for i in range(4):
#     for j in range(4):
#         if i+1 < 6:
#             print("({}, {},1),".format(block_bingo_area_co_ro[j][i], 
#                                        block_bingo_area_co_ro[j][i+2]))
#             count +=1
            
#         if i-1 > 0:
#             print("({}, {},1),".format(block_bingo_area_co_ro[j][i], 
#                                        block_bingo_area_co_ro[j][i-2]))
#             count +=1
            
#         if j+1 < 7:
#             print("({}, {},1),".format(crosscircle_positions[j][i],
#                                        crosscircle_positions[j+1][i]))
#             count+=1
            
#         if j-1 > -1:
#             print("({}, {},1),".format(crosscircle_positions[j][i], 
#                                            crosscircle_positions[j-1][i]))
#             count+=1
# print("]")

for c_p in crosscircle_positions:
    for b_p in blockcircle_positions_co_ro:
        print("({}, {},1),".format(c_p, b_p))
        count +=1
count
# -

print(nx.dijkstra_path(Graph, source=(4,0), target=(5,3), weight='weight'))
print(nx.dijkstra_path_length(Graph, source=(4,0), target=(5,3), weight='weight'))
for pred in nx.dijkstra_predecessor_and_distance(G=Graph, source=(4,0), weight='weight'):
    print("{}\n".format(pred))


# +
def dijkstra(s,n,w,cost):
    #始点sから各頂点への最短距離
    #n:頂点数,　w:辺の数, cost[u][v] : 辺uvのコスト(存在しないときはinf)
    d = [float("inf")] * n
    used = [False] * n
    d[s] = 0
    
    while True:
        v = -1
        #まだ使われてない頂点の中から最小の距離のものを探す
        for i in range(n):
            if (not used[i]) and (v == -1):
               v = i
            elif (not used[i]) and d[i] < d[v]:
                v = i
        if v == -1:
               break
        used[v] = True
               
        for j in range(n):
               d[j] = min(d[j],d[v]+cost[v][j])
    return d

################################
n,w = map(int,input().split()) #n:頂点数　w:辺の数

cost = [[float("inf") for i in range(n)] for i in range(n)] 
#cost[u][v] : 辺uvのコスト(存在しないときはinf この場合は10**10)
for i in range(w):
    x,y,z = map(int,input().split())
    cost[x][y] = z
    cost[y][x] = z
print(dijkstra(0,n,w,cost))
# -

block_edge = [[(j,i)for i in range(7)]for j in range(7)]

from pulp import *
import networkx as nx
g = nx.fast_gnp_random_graph(8, 0.26, 1).to_directed()
# source, sink = 0, 2 # 始点, 終点
# r = list(enumerate(g.edges()))
# m = LpProblem() # 数理モデル
# x = [LpVariable('x%d'%k, lowBound=0, upBound=1) for k, (i, j) in r] # 変数(路に入るかどうか)
# m += lpSum(x) # 目的関数
# for nd in g.nodes():
#     m += lpSum(x[k] for k, (i, j) in r if i == nd) == lpSum(x[k] for k, (i, j) in r if j == nd) + {source:1, sink:-1}.get(nd, 0) # 制約
# #     print(m)
# m.solve()
# print([(i, j) for k, (i, j) in r if value(x[k]) > 0.5])

Graph.nodes['set_block']

# +
# %reset
route_list = [[0, 5, 4, 2, 0, 0], [5, 0, 2, 0, 0, 6], [4, 2, 0, 3, 2, 0],
              [2, 0, 3, 0, 6, 0], [0, 0, 2, 6, 0, 4], [0, 6, 0, 0, 4, 0]]

import networkx as nx
import matplotlib.pyplot as plt
import math
# %matplotlib inline

# ノード数、各エッジコストなどを初期情報route_listから取得
node_count = len(route_list)
edges = [[i, j, route_list[i][j]] for i in range(node_count) for j in range(node_count) if route_list[i][j] != 0]

G=nx.Graph() 

#6点準備。初期色は黒を指定
G.add_nodes_from(list(range(node_count)), color= "k")

# エッジコストも含め点を繋ぐ。初期色は黒を指定
G.add_weighted_edges_from(edges, color= "k")

# 座標設定
pos={} 
pos[0]=(0,0) 
pos[1]=(2,2) 
pos[2]=(3,0)
pos[3]=(1,-3)
pos[4]=(4,-2)
pos[5]=(5,1)

#ノード色をリスト化
node_labels = { n: d['color'] for n,d in G.nodes(data=True) }
node_colors = [ node_labels[key] for key in node_labels ]

#エッジの始点と終点の組合わせとエッジコストを辞書の形で格納。
#G.edge(data=True) でエッジセットを辞書の形で得れる。(Falseは(u, v)タプルのみ)
edge_labels_weight = { (u,v): d['weight'] for u,v,d in G.edges(data=True) }
edge_labels_colors = { (u,v): d['color'] for u,v,d in G.edges(data=True) }
edge_colors = [edge_labels_colors[key] for key in edge_labels_colors]

# 描画
nx.draw_networkx_labels(G, pos, font_color="w")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_weight)
nx.draw(G, pos, node_color=node_colors, edge_color=edge_colors)

plt.show() 

def changeColorOfFixedNode(node_colors, unfixed_nodes):
    diff = list(set(list(range(6))) - set(unfixed_nodes))
    for d in diff:
        node_colors[d] = "r"
    return node_colors

minimum_distances_from_startnode = [math.inf] * node_count
minimum_distances_from_startnode[0] = 0
unfixed_nodes = list(range(6))
previous_fixed_nodes = [-1]*node_count

while len(unfixed_nodes) != 0:
    possible_min_distance_from_startnode = math.inf
    for node_index in unfixed_nodes:
        if node_index == 0:
            possible_min_distance_from_startnode = 0
            min_distance_node = 0
        if possible_min_distance_from_startnode > minimum_distances_from_startnode[node_index]:
            possible_min_distance_from_startnode = minimum_distances_from_startnode[node_index]
            min_distance_node = node_index
    min_distance_node_edges = route_list[min_distance_node]
    for i, min_distance_node_edge in enumerate(min_distance_node_edges):
        if min_distance_node_edge == 0:
            continue
        else:
            if minimum_distances_from_startnode[i] > min_distance_node_edge + minimum_distances_from_startnode[min_distance_node]:
                    minimum_distances_from_startnode[i] = min_distance_node_edge + minimum_distances_from_startnode[min_distance_node]
                    previous_fixed_nodes[i] = min_distance_node
    unfixed_nodes.remove(min_distance_node)

    print ("possible_min_distance_from_startnode = " + str(possible_min_distance_from_startnode))
    print ("min_distance_node = " + str(min_distance_node))
    print ("minimum_distances_from_startnode = " + str(minimum_distances_from_startnode))
    print ("minimum_distances_from_startnode[{min_distance_node}] = ".format(min_distance_node=min_distance_node) + str(minimum_distances_from_startnode[min_distance_node]))
    print ("previous_fixed_nodes = " + str(previous_fixed_nodes))
    print ("unfixed_nodes = " + str(unfixed_nodes))
    
    if min_distance_node != 0:
        fixed_edge = (previous_fixed_nodes[min_distance_node], min_distance_node) 
        edge_labels_colors[fixed_edge] = "r"
        edge_colors = [edge_labels_colors[key] for key in edge_labels_colors]

    node_colors = changeColorOfFixedNode(node_colors, unfixed_nodes)
    nx.draw_networkx_labels(G, pos, font_color="w")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_weight)
    nx.draw(G,pos, node_color=node_colors, edge_color=edge_colors)
    plt.show()
    
print("-----経路-----")
previous_node = node_count - 1
while previous_node != -1:
    if previous_node !=0:
        print(str(previous_node) + " <- ", end='')
    else:
        print(str(previous_node))
    previous_node = previous_fixed_nodes[previous_node]

print("-----距離-----")
print(minimum_distances_from_startnode[node_count - 1])
# -




