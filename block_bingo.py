
# coding: utf-8

# ## ビンゴブロックエリアとルールを元にした情報

# In[9]:


INF = 10000000

yel = 'yellow'
gre = 'green'
blu = 'blue'
red = 'red'
bla = 'black'

blocks_color = [yel, yel, gre, gre,  blu, blu,  red, red, bla]

block_bingo_area = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
    (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
    (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]

crosscircle_position = [
    (0, 0), (0, 2), (0, 4), (0, 6),
    (2, 0), (2, 2), (2, 4), (2, 6),
    (4, 0), (4, 2), (4, 4), (4, 6),
    (6, 0), (6, 2), (6, 4), (6, 6)
]

blockcircle_position = [
    (1,1), (1,3), (1,5), (3,1), (3,5), (5,1), (5,3), (5,5)
]

first_set_block_position = [
    (0,0), (2,2), (4,0), (6,2), (0,4), (2,6), (4,4), (6,6)
]

first_set_colorblock_number = 8
first_set_blackblock_number = 6 


# ## 仮想ビングブロックエリアの初期化
# ### ノードの追加

# In[10]:


# ダイクストラ法 Left

import networkx as nx # 経路探索用
import random #組み合わせよう
random.seed(42)

Graph = nx.DiGraph()

# ブロックビンゴエリアの必要な情報を仮想ビンゴブロックエリアに追加していく
Graph.add_nodes_from(block_bingo_area)

for blockcircle_num, position in enumerate(blockcircle_position, start=1):
    Graph.nodes[position]['set_block'] = False
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

# 初期化の時，ブロックサークル上に置かれているブロックの色を特定，排除
colorblock = Graph.nodes[blockcircle_position[first_set_colorblock_number-1]]['set_blockcircle_color']
blocks_color.remove(colorblock)
crosscircle_blockcolors = random.sample(blocks_color, 8)
print('init put crosscircle blocks {} .'.format(crosscircle_blockcolors))

for color, position in enumerate(first_set_block_position, start=0):
    Graph.nodes[position]['set_block'] = True
    Graph.nodes[position]['set_blockcolor'] = crosscircle_blockcolors[color]


# ### エッジの追加

# In[11]:


#エッジの生成
block_bingo_area_edge=[
((0, 0), (0, 1),1),
((0, 0), (1, 0),1),
((1, 0), (1, 1),5),
((1, 0), (2, 0),1),
((1, 0), (0, 0),1),
((2, 0), (2, 1),1),
((2, 0), (3, 0),1),
((2, 0), (1, 0),1),
((3, 0), (3, 1),5),
((3, 0), (4, 0),1),
((3, 0), (2, 0),1),
((4, 0), (4, 1),1),
((4, 0), (5, 0),1),
((4, 0), (3, 0),1),
((5, 0), (5, 1),5),
((5, 0), (6, 0),1),
((5, 0), (4, 0),1),
((6, 0), (6, 1),1),
((6, 0), (5, 0),1),
((0, 1), (0, 2),1),
((0, 1), (0, 0),1),
((0, 1), (1, 1),5),
((1, 1), (1, 2),5),
((1, 1), (1, 0),5),
((1, 1), (2, 1),5),
((1, 1), (0, 1),5),
((2, 1), (2, 2),1),
((2, 1), (2, 0),1),
((2, 1), (3, 1),5),
((2, 1), (1, 1),5),
((3, 1), (3, 2),5),
((3, 1), (3, 0),5),
((3, 1), (4, 1),5),
((3, 1), (2, 1),5),
((4, 1), (4, 2),1),
((4, 1), (4, 0),1),
((4, 1), (5, 1),5),
((4, 1), (3, 1),5),
((5, 1), (5, 2),5),
((5, 1), (5, 0),5),
((5, 1), (6, 1),5),
((5, 1), (4, 1),5),
((6, 1), (6, 2),5),
((6, 1), (6, 0),1),
((6, 1), (5, 1),5),
((0, 2), (0, 3),1),
((0, 2), (0, 1),1),
((0, 2), (1, 2),1),
((1, 2), (1, 3),5),
((1, 2), (1, 1),5),
((1, 2), (2, 2),1),
((1, 2), (0, 2),1),
((2, 2), (2, 3),1),
((2, 2), (2, 1),1),
((2, 2), (3, 2),1),
((2, 2), (1, 2),1),
((3, 2), (3, 3),5),
((3, 2), (3, 1),5),
((3, 2), (4, 2),1),
((3, 2), (2, 2),1),
((4, 2), (4, 3),1),
((4, 2), (4, 1),1),
((4, 2), (5, 2),1),
((4, 2), (3, 2),1),
((5, 2), (5, 3),5),
((5, 2), (5, 1),5),
((5, 2), (6, 2),1),
((5, 2), (4, 2),1),
((6, 2), (6, 3),1),
((6, 2), (6, 1),1),
((6, 2), (5, 2),1),
((0, 3), (0, 4),1),
((0, 3), (0, 2),1),
((0, 3), (1, 3),5),
((1, 3), (1, 4),5),
((1, 3), (1, 2),5),
((1, 3), (2, 3),5),
((1, 3), (0, 3),5),
((2, 3), (2, 4),1),
((2, 3), (2, 2),1),
((2, 3), (3, 3),5),
((2, 3), (1, 3),5),
((3, 3), (3, 4),5),
((3, 3), (3, 2),5),
((3, 3), (4, 3),5),
((3, 3), (2, 3),5),
((4, 3), (4, 4),1),
((4, 3), (4, 2),1),
((4, 3), (5, 3),5),
((4, 3), (3, 3),5),
((5, 3), (5, 4),5),
((5, 3), (5, 2),5),
((5, 3), (6, 3),5),
((5, 3), (4, 3),5),
((6, 3), (6, 4),1),
((6, 3), (6, 2),1),
((6, 3), (5, 3),5),
((0, 4), (0, 5),1),
((0, 4), (0, 3),1),
((0, 4), (1, 4),1),
((1, 4), (1, 5),5),
((1, 4), (1, 3),5),
((1, 4), (2, 4),1),
((1, 4), (0, 4),1),
((2, 4), (2, 5),1),
((2, 4), (2, 3),1),
((2, 4), (3, 4),1),
((2, 4), (1, 4),1),
((3, 4), (3, 5),5),
((3, 4), (3, 3),5),
((3, 4), (4, 4),1),
((3, 4), (2, 4),1),
((4, 4), (4, 5),1),
((4, 4), (4, 3),1),
((4, 4), (5, 4),1),
((4, 4), (3, 4),1),
((5, 4), (5, 5),5),
((5, 4), (5, 3),5),
((5, 4), (6, 4),1),
((5, 4), (4, 4),1),
((6, 4), (6, 5),1),
((6, 4), (6, 3),1),
((6, 4), (5, 4),5),
((0, 5), (0, 6),1),
((0, 5), (0, 4),1),
((0, 5), (1, 5),5),
((1, 5), (1, 6),5),
((1, 5), (1, 4),5),
((1, 5), (2, 5),5),
((1, 5), (0, 5),5),
((2, 5), (2, 6),1),
((2, 5), (2, 4),1),
((2, 5), (3, 5),5),
((2, 5), (1, 5),5),
((3, 5), (3, 6),5),
((3, 5), (3, 4),5),
((3, 5), (4, 5),5),
((3, 5), (2, 5),5),
((4, 5), (4, 6),1),
((4, 5), (4, 4),1),
((4, 5), (5, 5),5),
((4, 5), (3, 5),5),
((5, 5), (5, 6),5),
((5, 5), (5, 4),5),
((5, 5), (6, 5),5),
((5, 5), (4, 5),5),
((6, 5), (6, 6),1),
((6, 5), (6, 4),1),
((6, 5), (5, 5),5),
((0, 6), (0, 5),1),
((0, 6), (1, 6),1),
((1, 6), (1, 5),5),
((1, 6), (2, 6),1),
((1, 6), (0, 6),5),
((2, 6), (2, 5),1),
((2, 6), (3, 6),1),
((2, 6), (1, 6),1),
((3, 6), (3, 5),5),
((3, 6), (4, 6),1),
((3, 6), (2, 6),1),
((4, 6), (4, 5),1),
((4, 6), (5, 6),1),
((4, 6), (3, 6),1),
((5, 6), (5, 5),5),
((5, 6), (6, 6),1),
((5, 6), (4, 6),1),
((6, 6), (6, 5),1),
((6, 6), (5, 6),1),
]


# In[12]:


Graph.add_weighted_edges_from(block_bingo_area_edge)


# In[14]:


# for g in Graph.nodes(data=True):
#     print(g)


# ### Lコースの最短探索経路を出す

# In[15]:


start = (4,0)
i=0
while(True):
    i += 1
    print("{}".format(i))
    if i >= 8:
        break
    #交点サークル上のブロックとブロックサークルの色が同じ場合距離を計算する
    route_list=[]
    for block_position in first_set_block_position: #　運ぶブロックの個数分
        if not Graph.nodes[block_position]['set_block']: #ブロックが置かれてなかったらその地点からは考えなくていいよね
            continue
        for blockcir_position in blockcircle_position:
            if Graph.nodes[blockcir_position]['set_block']:
                continue
            if Graph.nodes[block_position]['set_blockcolor'] == Graph.nodes[blockcir_position]['set_blockcircle_color']:
                carry_color =Graph.nodes[block_position]['set_blockcolor']
#                 print('color:{}'.format(carry_color))
                move_path = nx.dijkstra_path(Graph, source=start, target=block_position, weight='weight')
                carry_path =  nx.dijkstra_path(Graph, source=block_position, target=blockcir_position, weight='weight')
                one_route_path = move_path+carry_path
                one_route_cost = len(move_path)+len(carry_path)
#                 print('path and cost: {} {}'.format(one_route_path, one_route_cost))
                route_list.append({'path': one_route_path, 'cost':one_route_cost, 'block_on_crosscircle_pos':move_path[-1], 'carry_color': carry_color})
    # 最小の1ルートを決定する
    shortest_route={'path':[], 'cost':INF}
    for route in route_list:
        if  route['cost'] < shortest_route['cost']:
            shortest_route = route
    print(shortest_route)

    #走行体の現在位置とブロックの状態を更新
    #走行体の現在位置を更新
    start = shortest_route['path'][-2]
    #ブロックの状態を更新
    # ブロックサークル
    placed_blockcircle_position = shortest_route['path'][-1]
    Graph.nodes[placed_blockcircle_position]['set_block'] = True
    Graph.nodes[placed_blockcircle_position]['set_blockcolor'] = shortest_route['carry_color']
    # 交点サークル
    removed_block4crosscircle_position = shortest_route['block_on_crosscircle_pos']
    Graph.nodes[removed_block4crosscircle_position]['set_block'] = False
    Graph.nodes[removed_block4crosscircle_position]['set_blockcolor'] = None


# In[7]:


for g in Graph.nodes(data=True):
    print(g)
# crosscircle_blockcolors
# Graph.nodes[blockcircle_position[first_set_colorblock_number-1]]['set_blockcircle_color']
# shortest_route={'path':[], 'cost':INF}
# for route in route_list:
#     if  route['cost'] < shortest_route['cost']:
#         shortest_route = route
# shortest_route
# for block_position in first_set_block_position:
#     print(block_position)
#     print(Graph.nodes[block_position]['set_blockcolor'])
    
# for blockcir_position in blockcircle_position:
#     print(blockcir_position)
#     Graph.nodes[blockcir_position]['set_blockcircle_color']
# start = shortest_route['path'][-2]
# start
# removed_block4crosscircle_position


# ## 素材置き場

# In[ ]:


print(nx.dijkstra_path(Graph, source=(4,0), target=(5,3), weight='weight'))
print(nx.dijkstra_path_length(Graph, source=(4,0), target=(5,3), weight='weight'))
for pred in nx.dijkstra_predecessor_and_distance(G=Graph, source=(4,0), weight='weight'):
    print("{}\n".format(pred))


# In[7]:


get_ipython().run_line_magic('reset', '')
route_list = [[0, 5, 4, 2, 0, 0], [5, 0, 2, 0, 0, 6], [4, 2, 0, 3, 2, 0],
              [2, 0, 3, 0, 6, 0], [0, 0, 2, 6, 0, 4], [0, 6, 0, 0, 4, 0]]

import networkx as nx
import matplotlib.pyplot as plt
import math
get_ipython().run_line_magic('matplotlib', 'inline')

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


# In[17]:


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


# In[18]:


block_edge = [[(j,i)for i in range(7)]for j in range(7)]


# In[51]:


count=0
print("[")
for i in range(7):
    for j in range(7):
        if i+1 < 7:
            if i in {1,3,5}:
                print("({}, {},5),".format(block_edge[j][i], block_edge[j][i+1]))
            else:
                print("({}, {},1),".format(block_edge[j][i], block_edge[j][i+1]))
            count +=1
            
        if i-1 > -1:
            if i in {1,3,5}:
                print("({}, {},5),".format(block_edge[j][i], block_edge[j][i-1]))
            else:
                print("({}, {},1),".format(block_edge[j][i], block_edge[j][i-1]))
            count +=1
            
        if j+1 < 7:
            if j in {1,3,5}:
                print("({}, {},5),".format(block_edge[j][i], block_edge[j+1][i]))
            else:
                print("({}, {},1),".format(block_edge[j][i], block_edge[j+1][i]))
            count+=1
            
        if j-1 > -1:
            if j in {1,3,5}:
                print("({}, {},5),".format(block_edge[j][i], block_edge[j-1][i]))
            else:
                print("({}, {},1),".format(block_edge[j][i], block_edge[j-1][i]))
            count+=1
            
print("]")
count


# In[11]:


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


# In[30]:


Graph.nodes['set_block']


# In[15]:




