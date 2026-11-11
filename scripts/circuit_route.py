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


def spark_gate(points,occluders,fade=6,projection=(1,0,0,1)):
    """Fade the entire spark cluster before its moving center enters a package."""
    from math import hypot,ceil
    lengths=[hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
    total=sum(lengths) or 1;elapsed=0;samples=[]
    for a,b,length in zip(points,points[1:],lengths):
        count=max(1,ceil(length/2))
        for i in range(count):
            f=i/count;x=a[0]+(b[0]-a[0])*f;y=a[1]+(b[1]-a[1])*f
            pa,pb,pc,pd=projection;x,y=pa*x+pc*y,pb*x+pd*y
            distance=min((hypot(max(left-x,0,x-right),max(top-y,0,y-bottom)) for left,top,right,bottom in occluders),default=fade)
            samples.append(((elapsed+length*f)/total,min(1,distance/fade)))
        elapsed+=length
    samples.append((1,samples[0][1] if samples else 1));result=[]
    for item in samples:
        while len(result)>1:
            a,b=result[-2:]
            if abs((b[1]-a[1])*(item[0]-b[0])-(item[1]-b[1])*(b[0]-a[0]))>1e-7:break
            result.pop()
        result.append(item)
    return result
