from env import TetrisEnv

env = TetrisEnv(render_mode="rgb_array")
obs = env.reset()

episode = 0
while episode < 10:
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    image = env.get_bitmap()
    image.save("tetris_output.jpg")
    # print(obs)

env.close()
