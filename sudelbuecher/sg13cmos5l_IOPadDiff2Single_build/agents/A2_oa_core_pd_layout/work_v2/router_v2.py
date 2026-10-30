class GridRouter:
    """Two-layer (Metal1 = 0, Metal2 = 1) router on a non-uniform grid: regular lines at `pitch` plus the centre
    lines of the pins (so a node can sit exactly on a 0.29 um track at 0.21 um spacing). Node squares are
    width x width; wires and via pads are unions of node squares. All spacing is geometric: a node is free for
    net k if its square keeps the spacing to every shape of another net (cell metal: M1_b / Mn_b, and M1_e /
    Mn_e next to the wide parts, as the deck's M1.e / M2.e; router wires: M1_b / Mn_b), and if it either overlaps
    net k's own cell metal by >= 0.05 um or keeps the spacing to it (no slivers / notches)."""

    def __init__(self, bbox, rules, dbu, pitch=0.27, width=0.29, margin=0.12, pref=("H", "V"), nonpref=1.6,
                 via_cost=6.0, turn_cost=1.5, nets=64, extra_x=(), extra_y=()):
        self.R, self.dbu = rules, dbu
        u = lambda v: int(round(v / dbu))
        self.u = u
        self.P, self.W, self.h = u(pitch), u(width), u(width / 2)
        self.margin = u(margin)
        g = u(rules["grid"])
        bb = bbox.to_itype(dbu)
        self.bb = bb
        snap = lambda v: int(math.ceil(v / g) * g)
        lox, hix = snap(bb.left + self.margin + self.h), bb.right - self.margin - self.h
        loy, hiy = snap(bb.bottom + self.margin + self.h), bb.top - self.margin - self.h
        xs = set(range(lox, hix + 1, self.P)) | {int(round(x / g)) * g for x in extra_x if lox <= x <= hix}
        ys = set(range(loy, hiy + 1, self.P)) | {int(round(y / g)) * g for y in extra_y if loy <= y <= hiy}
        self.xs = np.array(sorted(xs), dtype=np.int64)
        self.ys = np.array(sorted(ys), dtype=np.int64)
        self.xl, self.yl = self.xs.tolist(), self.ys.tolist()
        self.NX, self.NY = len(self.xs), len(self.ys)
        self.N = self.NX * self.NY
        self.pref = pref
        self.nonpref, self.via_cost, self.turn_cost = nonpref, via_cost, turn_cost
        self.mask = np.zeros((nets, 2, self.NX, self.NY), dtype=bool)   # mask[k]: nodes net k makes unusable
        self.band = {}                                                     # net -> own-metal sliver band
        self.viablk = np.zeros((self.NX, self.NY), dtype=bool)
        self.paths, self.vias, self.ports = {}, {}, {}
        self.s_narrow = (u(rules["M1_b"]), u(rules["Mn_b"]))               # M1.b, M2.b
        self.s_wide = (u(rules["M1_e"]), u(rules["Mn_e"]))                 # M1.e, M2.e
        self.w_wide = (u(rules["M1_e_w"]), u(rules["Mn_e_w"]))
        self.min_ov = u(0.05)
        assert self.W >= u(max(rules["M1_a"], rules["Mn_a"])), "wire narrower than M1.a / M2.a"
        assert self.h - u(rules["V1_a"] / 2) >= u(rules["V1_c1"]), "pad too small for the Via1 enclosure V1.c1"
        assert 2 * self.P - self.W >= max(self.s_narrow), "pitch too small for M1.b / M2.b"

    # ---- rasterization ---------------------------------------------------------------------------------
    def _rng(self, arr, lo, hi):
        """indices with lo < arr[i] < hi (strict)"""
        return int(np.searchsorted(arr, lo, side="right")), int(np.searchsorted(arr, hi, side="left")) - 1

    def _raster_box(self, b, bloat, out):
        i0, i1 = self._rng(self.xs, b.left - bloat, b.right + bloat)
        j0, j1 = self._rng(self.ys, b.bottom - bloat, b.top + bloat)
        if i0 <= i1 and j0 <= j1:
            out[i0:i1 + 1, j0:j1 + 1] = True

    def _raster(self, reg, bloat, out):
        for poly in reg.each():
            for tz in poly.decompose_trapezoids(db.Polygon.TD_htrapezoids):
                self._raster_box(tz.bbox(), bloat, out)

    def add_obstacle(self, metal, reg, k):
        """reg: shapes of net index k (0 = unknown) on metal M1 / M2."""
        L = 0 if metal == "M1" else 1
        ww = self.w_wide[L]
        wide = reg.sized(-(ww // 2)).sized(ww // 2) & reg
        blk = np.zeros((self.NX, self.NY), dtype=bool)
        self._raster(reg, self.s_narrow[L] + self.h, blk)
        self._raster(wide, self.s_wide[L] + self.h, blk)
        self.mask[k, L] |= blk
        if k:
            inner = np.zeros((self.NX, self.NY), dtype=bool)
            self._raster(reg, self.h - self.min_ov, inner)
            band = self.band.setdefault(k, np.zeros((2, self.NX, self.NY), dtype=bool))
            band[L] |= blk & ~inner

    def add_via_obstacle(self, reg):
        self._raster(reg, self.u(self.R["V1_b"]) + self.u(self.R["V1_a"] / 2), self.viablk)

    def free(self, k):
        f = (self.mask.sum(axis=0) - self.mask[k]) == 0
        if k in self.band:
            f &= ~self.band[k]
        return f

    def nid(self, L, i, j):
        return (L * self.NX + i) * self.NY + j

    def terminal_nodes(self, metal, term, k):
        L = 0 if metal == "M1" else 1
        hit = np.zeros((self.NX, self.NY), dtype=bool)
        self._raster(term, self.h - self.min_ov, hit)
        hit &= self.free(k)[L]
        ii, jj = np.nonzero(hit)
        return {self.nid(L, int(i), int(j)) for i, j in zip(ii, jj)}

    def edge_nodes(self, side, rng, k):
        f = self.free(k)[1]
        out = set()
        if side in ("top", "bottom"):
            j = self.NY - 1 if side == "top" else 0
            for i in range(self.NX):
                x = self.xl[i] * self.dbu
                if f[i, j] and (rng is None or rng[0] <= x <= rng[1]):
                    out.add(self.nid(1, i, j))
        else:
            i = self.NX - 1 if side == "right" else 0
            for j in range(self.NY):
                y = self.yl[j] * self.dbu
                if f[i, j] and (rng is None or rng[0] <= y <= rng[1]):
                    out.add(self.nid(1, i, j))
        return out

    # ---- search ----------------------------------------------------------------------------------------
    def route_net(self, k, groups):
        free = self.free(k)
        fb = free.reshape(-1).tobytes()
        vb = (~self.viablk).reshape(-1).tobytes()
        tree = set(groups[0])
        rest = [set(g) for g in groups[1:]]
        paths, vias = [], []
        while rest:
            targets = set().union(*rest)
            path = self._astar(tree, targets, fb, vb)
            if path is None:
                return False, "no path to %d of %d terminal groups" % (len(rest), len(groups) - 1)
            end = path[-1]
            for g in rest:
                if end in g:
                    rest.remove(g)
                    tree |= g
                    break
            tree |= set(path)
            paths.append(path)
            vias += [a % self.N for a, b in zip(path[:-1], path[1:]) if a // self.N != b // self.N]
        self.paths.setdefault(k, []).extend(paths)
        self.vias.setdefault(k, []).extend(vias)
        self._commit(k, paths, vias)
        return True, "%d branches, %d vias" % (len(paths), len(vias))

    def _astar(self, sources, targets, fb, vb):
        NX, NY, N, P = self.NX, self.NY, self.N, float(self.P)
        xl, yl = self.xl, self.yl
        pts = [(xl[(t % N) // NY], yl[t % NY]) for t in targets]
        if len(pts) > 80:
            pts = pts[::len(pts) // 80 + 1]
        INF = float("inf")

        def hfun(x, y):
            return min(abs(x - a) + abs(y - b) for a, b in pts) / P
        best, parent, heap = {}, {}, []
        for s in sources:
            if fb[s]:
                st = s * 5 + 4
                best[st] = 0.0
                rem = s % N
                heapq.heappush(heap, (hfun(xl[rem // NY], yl[rem % NY]), 0.0, st))
        cost = {}
        for L in (0, 1):
            cost[(L, "H")] = 1.0 if self.pref[L] == "H" else self.nonpref
            cost[(L, "V")] = 1.0 if self.pref[L] == "V" else self.nonpref
        tc, vc = self.turn_cost, self.via_cost
        while heap:
            f, g, st = heapq.heappop(heap)
            if g > best.get(st, INF):
                continue
            node, d = divmod(st, 5)
            if node in targets:
                path = [node]
                while st in parent:
                    st = parent[st]
                    if st // 5 != path[-1]:
                        path.append(st // 5)
                path.reverse()
                return path
            L, rem = divmod(node, N)
            i, j = divmod(rem, NY)
            x, y = xl[i], yl[j]
            for nd, di, dj in ((0, 1, 0), (1, -1, 0), (2, 0, 1), (3, 0, -1)):
                ni, nj = i + di, j + dj
                if ni < 0 or nj < 0 or ni >= NX or nj >= NY:
                    continue
                nn = node + di * NY + dj
                if not fb[nn]:
                    continue
                if nd < 2:
                    c = abs(xl[ni] - x) / P * cost[(L, "H")]
                else:
                    c = abs(yl[nj] - y) / P * cost[(L, "V")]
                if d != 4 and d != nd:
                    c += tc
                ng = g + c
                ns = nn * 5 + nd
                if ng < best.get(ns, INF):
                    best[ns] = ng
                    parent[ns] = st
                    heapq.heappush(heap, (ng + hfun(xl[ni], yl[nj]), ng, ns))
            on = (1 - L) * N + rem
            if fb[on] and vb[rem]:
                ng = g + vc
                ns = on * 5 + 4
                if ng < best.get(ns, INF):
                    best[ns] = ng
                    parent[ns] = st
                    heapq.heappush(heap, (ng + hfun(x, y), ng, ns))
        return None

    def _commit(self, k, paths, vias):
        for path in paths:
            for n in path:
                L, b = self.node_box(n)
                self._raster_box(b, self.s_narrow[L] + self.h, self.mask[k, L])
        a = self.u(self.R["V1_a"] / 2)
        for rem in vias:
            i, j = divmod(rem, self.NY)
            x, y = self.xl[i], self.yl[j]
            self._raster_box(db.Box(x - a, y - a, x + a, y + a), self.u(self.R["V1_b"]) + a, self.viablk)

    # ---- output ----------------------------------------------------------------------------------------
    def node_box(self, n):
        L, rem = divmod(n, self.N)
        i, j = divmod(rem, self.NY)
        x, y = self.xl[i], self.yl[j]
        return L, db.Box(x - self.h, y - self.h, x + self.h, y + self.h)

    def wire_region(self, metal, k):
        L0 = 0 if metal == "M1" else 1
        r = db.Region()
        for path in self.paths.get(k, []):
            for n in path:
                L, b = self.node_box(n)
                if L == L0:
                    r.insert(b)
        if L0 == 1 and k in self.ports:
            r.insert(self.ports[k][1])
        return r.merged()

    def via_region(self, k):
        r = db.Region()
        a = self.u(self.R["V1_a"] / 2)
        for rem in self.vias.get(k, []):
            i, j = divmod(rem, self.NY)
            x, y = self.xl[i], self.yl[j]
            r.insert(db.Box(x - a, y - a, x + a, y + a))
        return r

    def port_pin_box(self, k, side):
        """The edge node net k reached: its square extended to the block edge (the pin box)."""
        for path in self.paths.get(k, []):
            for n in (path[0], path[-1]):
                L, rem = divmod(n, self.N)
                i, j = divmod(rem, self.NY)
                x, y = self.xl[i], self.yl[j]
                hit = ((side == "top" and j == self.NY - 1) or (side == "bottom" and j == 0) or
                       (side == "right" and i == self.NX - 1) or (side == "left" and i == 0))
                if L == 1 and hit:
                    b, h = self.bb, self.h
                    box = {"top": db.Box(x - h, y - h, x + h, b.top), "bottom": db.Box(x - h, b.bottom, x + h, y + h),
                           "right": db.Box(x - h, y - h, b.right, y + h),
                           "left": db.Box(b.left, y - h, x + h, y + h)}[side]
                    self.ports[k] = ((i, j), box)
                    return box
        return None

    def stats(self, k):
        n = {0: 0, 1: 0}
        for path in self.paths.get(k, []):
            for a, b in zip(path[:-1], path[1:]):
                if a // self.N == b // self.N:
                    L, ba = self.node_box(a)
                    _, bb_ = self.node_box(b)
                    n[L] += abs(ba.left - bb_.left) + abs(ba.bottom - bb_.bottom)
        return dict(M1=round(n[0] * self.dbu, 2), M2=round(n[1] * self.dbu, 2), vias=len(self.vias.get(k, [])))


