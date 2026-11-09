from collections import deque

def circuit_route(active,width=53,height=7):
    """Connect every active cell by shortest orthogonal paths; never consume cells."""
    active=set(active)
    if not active:return [(0,0),(1,0),(1,1),(0,1),(0,0)]
    start=min(active);route=[start];remaining=active-{start}
    def shortest(origin,targets):
        queue=deque([origin]);parent={origin:None}
        while queue:
            current=queue.popleft()
            if current in targets:
                result=[]
                while current!=origin:result.append(current);current=parent[current]
                return list(reversed(result))
            x,y=current
            for nxt in ((x+1,y),(x,y+1),(x-1,y),(x,y-1)):
                if 0<=nxt[0]<width and 0<=nxt[1]<height and nxt not in parent:parent[nxt]=current;queue.append(nxt)
        raise ValueError('Unreachable contribution cell')
    while remaining:
        segment=shortest(route[-1],remaining);route+=segment;remaining.difference_update(segment)
    route+=shortest(route[-1],{start})
    if len(route)==1:
        x,y=start;nx=x+1 if x+1<width else x-1;route=[start,(nx,y),start]
    assert active.issubset(route)
    assert route[0]==route[-1]
    assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for a,b in zip(route,route[1:]))
    return route
