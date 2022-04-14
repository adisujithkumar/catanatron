import random
from catanatron_gym.envs.catanatron_env import CatanatronEnv
import gym

from catanatron_gym.features import get_feature_ordering

features = get_feature_ordering()


def get_p0_num_settlements(obs):
    indexes = [
        i
        for i, name in enumerate(features)
        if "NODE" in name and "SETTLEMENT" in name and "P0" in name
    ]
    return sum([obs[i] for i in indexes])


def test_gym():
    env = CatanatronEnv()

    first_observation = env.reset()  # this forces advanced until p0...
    assert len(env.get_valid_actions()) >= 50  # first seat at most blocked 4 nodes
    assert get_p0_num_settlements(first_observation) == 0

    action = random.choice(env.get_valid_actions())
    second_observation, reward, done, info = env.step(action)
    assert first_observation != second_observation
    assert reward == 0
    assert not done
    assert len(env.get_valid_actions()) in [2, 3]

    assert second_observation[features.index("BANK_DEV_CARDS")] == 25
    assert second_observation[features.index("BANK_SHEEP")] == 19
    assert get_p0_num_settlements(second_observation) == 1

    reset_obs = env.reset()
    assert reset_obs != second_observation
    assert get_p0_num_settlements(reset_obs) == 0

    env.close()


def test_gym_registration_and_api_works():
    env = gym.make("catanatron_gym:catanatron-v0")
    observation = env.reset()
    for _ in range(1000):
        action = random.choice(env.get_valid_actions())  # type: ignore
        observation, reward, done, info = env.step(action)
        if done:
            observation = env.reset()
    env.close()
