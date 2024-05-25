import sys
from collections import deque

def Blossom(graph,num):
    #输入:顶点个数为num的完全图graph,以邻接矩阵形式给出,顶点标号从1~num

    INF = sys.maxsize
    MAXN = num+1
    
    class Edge:
        def __init__(self, u=0, v=0, w=0):
            self.u = u
            self.v = v
            self.w = w
    
    n=num  #给出的完全图的顶点数
    n_x=0
    g = [[Edge() for _ in range(MAXN * 2 + 1)] for _ in range(MAXN * 2 + 1)]
    flower = [[] for _ in range(MAXN * 2 + 1)]
    lab = [0] * (MAXN * 2 + 1)
    match = [0] * (MAXN * 2 + 1)
    slack = [0] * (MAXN * 2 + 1)
    st = [0] * (MAXN * 2 + 1)
    pa = [0] * (MAXN * 2 + 1)
    flower_from = [[0] * (MAXN + 1) for _ in range(MAXN * 2 + 1)]
    S = [-1] * (MAXN * 2 + 1)
    vis = [0] * (MAXN * 2 + 1)
    q = deque()
    
    weight_cap=200
    
    t = 0  #在get_lca里用

    def e_delta(e):
        return lab[e.u] + lab[e.v] - g[e.u][e.v].w * 2

    def update_slack(u, x):
        if not slack[x] or e_delta(g[u][x]) < e_delta(g[slack[x]][x]):
            slack[x] = u

    def set_slack(x):
        slack[x] = 0
        for u in range(1, n + 1):
            if g[u][x].w > 0 and st[u] != x and S[st[u]] == 0:
                update_slack(u, x)

    def q_push(x):
        if x <= n:
            q.append(x)
        else:
            for i in range(len(flower[x])):
                q_push(flower[x][i])

    def set_st(x, b):
        st[x] = b
        if x > n:
            for i in range(len(flower[x])):
                set_st(flower[x][i], b)

    def get_pr(b, xr):
        pr = flower[b].index(xr)
        if pr % 2 == 1:
            flower[b][1:] = reversed(flower[b][1:])
            return len(flower[b]) - pr
        return pr

    def set_match(u, v):
        match[u] = g[u][v].v
        if u > n:
            e = g[u][v]
            xr = flower_from[u][e.u]
            pr = get_pr(u, xr)
            for i in range(pr):
                set_match(flower[u][i], flower[u][i ^ 1])  #i^1即与1异或(二进制)
            set_match(xr, v)
            flower[u] = flower[u][pr:] + flower[u][:pr]

    def augment(u, v):
        while True:
            xnv = st[match[u]] #注意这时候的match[u]还不是v
            set_match(u, v)
            if not xnv:
                return
            set_match(xnv, st[pa[xnv]])
            u = st[pa[xnv]]
            v = xnv

    def get_lca(u, v):
        #找出最近共同祖先
        nonlocal t #允许内层函数调用并修改外部函数的变量（如果没有nonlocal就无法修改）
        t += 1
        while u or v:
            if u:
                if vis[u] == t:
                    return u
                vis[u] = t
                u = st[match[u]]
                if u:
                    u = st[pa[u]]
            u, v = v, u
        return 0
    
    def add_blossom(u, lca, v):
        nonlocal n_x
        b = n + 1
        while b <= n_x and st[b]:
            b += 1
        if b > n_x:
            n_x += 1
        lab[b] = 0
        S[b] = 0
        match[b] = match[lca]
        flower[b] = [lca]

        x = u
        while x != lca:
            flower[b].append(x)
            y = st[match[x]]
            flower[b].append(y)
            q_push(y)
            x = st[pa[y]]
        
        flower[b][1:] = reversed(flower[b][1:])

        x = v
        while x != lca:
            flower[b].append(x)
            y = st[match[x]]
            flower[b].append(y)
            q_push(y)
            x = st[pa[y]]

        set_st(b, b)
        for x in range(1, n_x + 1):
            g[b][x].w = g[x][b].w = 0
        for x in range(1, n + 1):
            flower_from[b][x] = 0
        for i in range(len(flower[b])):
            xs = flower[b][i]
            for x in range(1, n_x + 1):
                if not g[b][x].w or e_delta(g[xs][x]) < e_delta(g[b][x]):
                    g[b][x] = g[xs][x]
                    g[x][b] = g[x][xs]
            for x in range(1, n + 1):
                if flower_from[xs][x]:  #不等于0就代表xs包含x
                    flower_from[b][x] = xs
        set_slack(b)

    def expand_blossom(b):
        for i in range(len(flower[b])):
            set_st(flower[b][i], flower[b][i])
        xr = flower_from[b][g[b][pa[b]].u]
        pr = get_pr(b, xr)
        for i in range(0,pr,2):
            pa[flower[b][i]] = g[flower[b][i + 1]][flower[b][i]].u
            S[flower[b][i]] = 1
            S[flower[b][i + 1]] = 0
            slack[flower[b][i]] = 0
            set_slack(flower[b][i + 1])
            q_push(flower[b][i + 1])
        S[xr] = 1
        pa[xr] = pa[b]
        for i in range(pr + 1, len(flower[b])):
            S[flower[b][i]] = -1
            set_slack(flower[b][i])
        st[b] = 0
        
    def on_found_edge(e):
        u, v = st[e.u], st[e.v]
        if S[v] == -1:
            pa[v] = e.u
            S[v] = 1
            nu = st[match[v]]
            slack[v] = slack[nu] = 0
            S[nu] = 0
            q_push(nu)
        elif S[v] == 0:
            lca = get_lca(u, v)
            if not lca:
                augment(u, v)
                augment(v, u)
                return True
            else:
                add_blossom(u, lca, v)
        return False
    
    def matching():
        nonlocal q  #确保这里的q和外面定义的是同一个，而不是重新定义一个新的
        # 初始化S和slack
        for i in range(1, n_x + 1):
            S[i] = -1
            slack[i] = 0
        q = deque()  # 清空队列

        # 将所有未匹配点加入队列并设为偶点
        for x in range(1, n_x + 1):
            if st[x] == x and not match[x]:
                pa[x] = 0
                S[x] = 0
                q_push(x)

        if not q:
            return False  # 所有点都有匹配

        while True:
            while q:
                u = q.popleft()
                if S[st[u]] == 1:
                    continue
                for v in range(1, n + 1):
                    if g[u][v].w > 0 and st[u] != st[v]:
                        if e_delta(g[u][v]) == 0:
                            if on_found_edge(g[u][v]):
                                return True
                        else:
                            update_slack(u, st[v])

            # 修改lab值
            d = INF
            for u in range(1, n + 1):
                if S[st[u]] == 0:
                    d = min(d, lab[u])
            for b in range(n + 1, n_x + 1):
                if st[b] == b and S[b] == 1:
                    d = min(d, lab[b] / 2)   #//表示整数除
            for x in range(1, n_x + 1):
                if st[x] == x and slack[x]:
                    if S[x] == -1:
                        d = min(d, e_delta(g[slack[x]][x]))
                    elif S[x] == 0:
                        d = min(d, e_delta(g[slack[x]][x]) / 2)  #//表示整数除

            for u in range(1, n + 1):
                if S[st[u]] == 0:
                    if lab[u] == d:
                        return False
                    lab[u] -= d
                elif S[st[u]] == 1:
                    lab[u] += d

            for b in range(n + 1, n_x + 1):
                if st[b] == b:
                    if S[b] == 0:
                        lab[b] += d * 2
                    elif S[b] == 1:
                        lab[b] -= d * 2

            q = deque()  # 清空队列
            for x in range(1, n_x + 1):
                if st[x] == x and slack[x] and st[slack[x]] != x and e_delta(g[slack[x]][x]) == 0:
                    if on_found_edge(g[slack[x]][x]):
                        return True

            for b in range(n + 1, n_x + 1):
                if st[b] == b and S[b] == 1 and lab[b] == 0:
                    expand_blossom(b)

        return False

    def init_weight_graph():
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                g[u][v] = Edge(u, v, weight_cap-graph[u][v])  #生成的图的边长与原先的图“互补”，原先长的变短，短的变长，从而得到WMPM


    #下面是主函数
    match = [0] * (2 * MAXN + 1)
    n_x = n  # 一开始没有花
    n_matches = 0
    tot_weight = 0
    for u in range(n + 1):
        st[u] = u
        flower[u].clear()
    w_max = 0
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            flower_from[u][v] = u if u == v else 0
            w_max = max(w_max, g[u][v].w)
    for u in range(1, n + 1):
        lab[u] = w_max

    #初始化加权图
    init_weight_graph()

    while matching():
        n_matches += 1
    for u in range(1, n + 1):
        if match[u] and match[u] < u:
            tot_weight += g[u][match[u]].w

    #下面生成配对的match
    match_pair=[]
    for u in range(1, n + 1):
        if match[u]>u:
            match_pair.append((u,match[u]))
    #return tot_weight,n_matches,match_pair
    return match_pair
