
# 绘制网络图以及指定节点和级别进行查询

import re
import networkx as nx
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] #显示中文

# 此处只是为了展示，暂时用txt替代MySQL传入
txtfile = open(r'E:\mysql数据库\1-70.ann', 'r', encoding='utf-8').readlines()
# print(txtfile[:3])

#将实体与关系数据分开
entity = []
relation = []
for i in txtfile:
    if i[0] == 'T':
        entity.append(i)
    else:
        relation.append(i)

# print(relation)

#将实体名称、类别与编号提取出来
entity = [i.strip('\n').split('\t') for i in entity]
entity = [[i[0],i[1].split(' ')[0], i[-1]] for i in entity]
# print(entity[:5])
#在实体表中插入数据
# #提取实体名，去重;需要提前查看数据库已有的实体名称 需要表名称
entitymin = [i[-1] for i in entity]
entitymin = list(set(entitymin))
# print(entitymin[:5])

#将三元组提取出来
relation = [re.split("[\tA:' ']",i) for i in relation]
relation = [[i[1],i[4],i[7]] for i in relation]
# print(relation[:5])

dicen = dict([('病症',1),('病名',2),('诊断方案',3),('治疗方案',4),('药名',5),('其它',6)])
dicre =  dict([('包含',1),('治疗',2),('危险因素',3),('辅助诊断',4),('特征',5),('并发',6),('别名',7),('作用',8),('条件',9)])
# print(dicre['包含'])

# #将三元组中的实体编号替换成实体名称
for r in relation:
    # r[0] = dicre[r[0]]
    for e in entity:
        if r[1] == e[0]:
            r[1] = e[-1]
            # r.insert(0,e[1])
        if r[-1] == e[0]:
            r[-1] = e[-1]
            # r.append(e[1])
    r.append(r[0])
# print(relation[:5])
relation = [tuple(r[1:]) for r in relation]
# print(relation[:5])
lista = []
for i in relation:
    if i[-1] == '别名':
        lista.append([i[1], i[0], i[-1]])
relation += lista
# print(lista)
# print(relation[:5])

plt.figure(3, figsize=(48, 27)) # 这里控制画布的大小，可以说改变整张图的布局
plt.subplot(111)
M = nx.DiGraph()
M.add_weighted_edges_from(relation) 
    #传入数据,格式[('甲状腺疾病', '甲状腺功能亢进症', '包含'), ('甲状腺疾病', '甲状腺功能减退', '包含')]
edge_labels = nx.get_edge_attributes(M, 'weight') #取出实体之间的关系
pos =  nx.random_layout(M)
# pos = nx.spring_layout(G, iterations=30) #设置画图的样式
nx.draw(M, pos,edge_color="grey", node_size=80) #设置点的位置
nx.draw_networkx_edge_labels(M,pos, edge_labels=edge_labels, font_size=10) #边的格式设置
nx.draw(M,pos, node_size=120, with_labels=True,font_size = 10) #节点设置
plt.savefig("imag.png")
plt.show()

#---------------------查找节点----------------------------------
# nx.draw(M, with_labels=True)##plt.savefig("imag3.png")#plt.show()
def get_neigbors(g, node, depth=1):
    output = {}
    output1 = []
    layers = dict(nx.bfs_successors(g, source=node, depth_limit=depth))
    nodes = [node]
    for i in range(1,depth+1):
        output[i] = []
        for x in nodes:
            output[i].extend(layers.get(x,[]))
            output1.extend(layers.get(x,[]))
        nodes = output[i]
    print('这是节点：',output)
    return output1##print(get_neigbors(M, '990', depth = 4))#[23,12,14,23,45,65,78]
def newlist(M, a, alist):
    alist.insert(0,a)
    newlistcon = list()
    for index, name in enumerate(alist[:-1]):
        for name1 in alist[index+1:]:
            if M.get_edge_data(name,name1) != None:
                relation = M.get_edge_data(name,name1)['weight']
                newlistcon.append([name, name1, relation])
    lista = []
    for i in newlistcon:
        if i[-1] == '别名':
            lista.append([i[1], i[0], i[-1]])
    newlistcon += lista
    return newlistcon#print('这是新数据',newlist(M, '990', get_neigbors(M, '990', depth = 4)))
node,depth = '甲状腺疾病',2
liststrnewcon = newlist(M, node, get_neigbors(M, node, depth = depth))
G = nx.DiGraph()
plt.figure(3, figsize=(32,18)) # 这里控制画布的大小，可以说改变整张图的布局
plt.subplot(111)
G.add_weighted_edges_from(liststrnewcon) #传入数据
edge_labels = nx.get_edge_attributes(G, 'weight') #取出实体之间的关系
# pos = nx.spring_layout(G, iterations=30) #设置画图的样式
pos =  nx.random_layout(G)
# pos = nx.spectral_layout(G)

nx.draw(G, pos,edge_color="grey", node_size=80) #设置点的位置
nx.draw_networkx_edge_labels(G,pos, edge_labels=edge_labels, font_size=15) #边的格式设置
nx.draw(G,pos, node_size=1500,node_color = 'skyblue',node_shape = 's', with_labels=True,font_size = 15,edge_color = 'red') #节点设置
plt.savefig("imag_jia1.png")
plt.show()

#---------------------end----------------------------------
