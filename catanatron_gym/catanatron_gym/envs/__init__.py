from catanatron_gym.envs.catanatron_env import CatanatronEnv

from gym.envs.registration import register

register(
    id="catanatron-v0",
    entry_point="catanatron_gym.envs:CatanatronEnv",
)
