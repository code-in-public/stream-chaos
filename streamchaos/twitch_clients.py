import os

from twitchAPI.twitch import Twitch
from twitchAPI.pubsub import PubSub
from twitchAPI.types import AuthScope
from twitchAPI.oauth import UserAuthenticator


class RedemptionPointsClient:

    def __init__(self, config):
        self.redemption_call_backs = {}
        self.pubsub = None
        self.points_redeem_uuid = None
        self.config = config

    def callback_points(self, uuid, data):
        """
        Extracted to the channel points
        Followers:
            MrsFabrik
            aquafunkalisticbootywhap
        """
        print('got points callback for UUID ' + str(uuid))

        # TODO Make sure this doesn't totally explode
        redemption_id = data['data']['redemption']['reward']['id']

        print('Redemption id is' + str(redemption_id))

        if redemption_id in self.redemption_call_backs:
            self.redemption_call_backs[redemption_id](data)
        else:
            print('Unexpected points redemption!!!!')

    def start(self):
        cfg = self.config

        # create instance of twitch API
        self.twitch = twitch = Twitch(cfg.client_id, cfg.client_secret)
        twitch.authenticate_app([])

        # get ID of user
        user_info = twitch.get_users(logins=['codeinpublic'])
        user_id = user_info['data'][0]['id']

        target_scope = [AuthScope.WHISPERS_READ, AuthScope.CHANNEL_READ_REDEMPTIONS]
        auth = UserAuthenticator(twitch, target_scope, force_verify=False)

        # this will open your default browser and prompt you with the twitch verification website
        token, refresh_token = auth.authenticate()

        twitch.set_user_authentication(token, target_scope, refresh_token)

        # starting up PubSub
        self.pubsub = pubsub = PubSub(twitch)
        pubsub.start()

        self.points_redeem_uuid = pubsub.listen_channel_points(user_id, self.callback_points)

    def stop(self):
        # you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
        self.pubsub.unlisten(self.points_redeem_uuid)
        self.pubsub.stop()

    @classmethod
    def run(cls, config):
        client = cls(config)
        client.start()

        # Prevents early termination
        input('press ENTER to close...')

        client.stop()


