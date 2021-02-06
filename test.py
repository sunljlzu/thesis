from bayes_opt import BayesianOptimization

def black_box_function(x, y):
    return -x**2 -(y-1)**2 + 1

pbounds = {'x': (2, 4), 'y': (-3, 3)}
optimizer = BayesianOptimization(
    f=black_box_function,
    pbounds=pbounds,
    verbose=2,
    random_state=1
)

optimizer.maximize(
    init_points=2,
    n_iter=30,
)

print(optimizer.max)