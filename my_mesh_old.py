def make_mesh(p): #failed, need more fancy math
    id1 = 0
    id2 = np.argmin(np.sum((p[1:]-p[0])**2,axis=1))+1


    # p = np.array([[0,0],[1,0.2],[0,1],[0.5,1],[1,2]])
    ids = np.arange(len(p),dtype=int)

    todo_verts = [[id1,id2],[id2,id1]] #from,to
    done_vertices = []
    faces = []

    while True:#while True:
        if len(todo_verts)==0:
            break
        id1,id2 = todo_verts.pop(0)
        if [id1,id2] in done_vertices:
            continue

        p1 = p[id1]
        p2 = p[id2]
        # print('new',id1,id2,p1,p2)
        pe = (p1+p2)/2
        nT = (p2-p1)/np.sum((p2-p1)**2)**0.5 #from point 1 to point 2
        n = np.array([-nT[1],nT[0]]) 
        # print('n',n)
        pd = (p-pe)
        dis_lat = np.dot(pd,n)
        dis_ver = np.dot(pd,nT)
        filt = dis_lat>1e-8
        # print('dis',dis_lat)
        if np.any(filt):
            dis = 1*dis_ver**2 + dis_lat**2
            p_next = ids[filt][np.argmin(dis[filt])]
            faces.append([id1,p_next,id2])
            done_vertices.append([p_next,id1])
            done_vertices.append([id2,p_next])
            if [id1,p_next] not in done_vertices:
                todo_verts.append([id1,p_next])
            if [p_next,id2] not in done_vertices:
                todo_verts.append([p_next,id2])
            # print('todovert',p_next,todo_verts)
        done_vertices.append([id1,id2])
        # plt.plot(p[:,0],p[:,1],'.')
        # for i1,i2,i3 in faces:
        #     plt.plot(*p[[i1,i2,i3,i1]].T)
        # if len(todo_verts)>0: plt.plot(*p[todo_verts[0]].T,'r')
        # plt.show()
    done_vertices = list(set([tuple(v) for v in done_vertices if v[0]<v[1]]))
    return faces, done_vertices