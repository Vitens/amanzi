def fmin(func, x0, args=(), xtol=1e-4, ftol=1e-4,
            maxiter=None, maxfev=None, return_all=False):

    import math
    import copy

    # Standard Nelder–Mead coefficients (SciPy defaults)
    alpha = 1.0   # reflection
    gamma = 2.0   # expansion
    rho   = 0.5   # contraction
    sigma = 0.5   # shrink

    def dist(a, b):
        return math.sqrt(sum((ai - bi)**2 for ai, bi in zip(a, b)))

    x0 = list(x0)
    N = len(x0)

    if maxiter is None:
        maxiter = N * 200
    if maxfev is None:
        maxfev = N * 200

    # --- Initial simplex ---
    sim = [x0]
    for k in range(N):
        y = copy.copy(x0)
        if y[k] != 0:
            y[k] = (1 + 0.05) * y[k]
        else:
            y[k] = 0.00025
        sim.append(y)

    fsim = [func(x, *args) for x in sim]
    nfev = len(fsim)
    iterations = 0

    if return_all:
        allvecs = [copy.copy(sim[0])]

    # --- Main loop ---
    while nfev < maxfev and iterations < maxiter:

        # Order
        indices = sorted(range(N + 1), key=lambda i: fsim[i])
        sim = [sim[i] for i in indices]
        fsim = [fsim[i] for i in indices]

        # Convergence check (SciPy-style)
        max_dist = max(dist(sim[0], sim[i]) for i in range(1, N+1))
        max_fdiff = max(abs(fsim[0] - fsim[i]) for i in range(1, N+1))

        if max_dist <= xtol and max_fdiff <= ftol:
            break

        # Centroid (exclude worst point)
        xbar = [
            sum(sim[i][j] for i in range(N)) / N
            for j in range(N)
        ]

        # Reflection
        xr = [xbar[j] + alpha * (xbar[j] - sim[-1][j]) for j in range(N)]
        fxr = func(xr, *args)
        nfev += 1

        if fsim[0] <= fxr < fsim[-2]:
            sim[-1] = xr
            fsim[-1] = fxr

        elif fxr < fsim[0]:
            # Expansion
            xe = [xbar[j] + gamma * (xr[j] - xbar[j]) for j in range(N)]
            fxe = func(xe, *args)
            nfev += 1

            if fxe < fxr:
                sim[-1] = xe
                fsim[-1] = fxe
            else:
                sim[-1] = xr
                fsim[-1] = fxr

        else:
            # Contraction
            if fxr < fsim[-1]:
                # Outside contraction
                xc = [xbar[j] + rho * (xr[j] - xbar[j]) for j in range(N)]
            else:
                # Inside contraction
                xc = [xbar[j] - rho * (xbar[j] - sim[-1][j]) for j in range(N)]

            fxc = func(xc, *args)
            nfev += 1

            if fxc <= fxr:
                sim[-1] = xc
                fsim[-1] = fxc
            else:
                # Shrink
                for i in range(1, N + 1):
                    sim[i] = [
                        sim[0][j] + sigma * (sim[i][j] - sim[0][j])
                        for j in range(N)
                    ]
                    fsim[i] = func(sim[i], *args)
                nfev += N

        iterations += 1
        if return_all:
            allvecs.append(sim[0][:])

    result = {
        "x": sim[0],
        "fun": fsim[0],
        "nit": iterations,
        "nfev": nfev,
        "success": (iterations < maxiter and nfev < maxfev)
    }

    if return_all:
        result["allvecs"] = allvecs

    return result