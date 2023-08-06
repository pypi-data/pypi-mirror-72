import os
import json
import platform


class OSProfileError(BaseException):
    pass


class OSProfile:

    def __init__(self, appname=None, profile=None, options=None):
        if appname is not None and profile is not None:
            # Unix style profile path
            if platform.system() != 'Windows':
                self.path = os.path.join(
                    os.environ['HOME'], '.config', appname)
            # Windows style profile path
            else:
                self.path = os.path.join(
                    os.environ['USERPROFILE'], 'AppData', 'Local', appname)

            self.profile = profile
            self.options = options
            self._init_profile()

        else:
            raise OSProfileError('OSProfile init error.')

    def _init_profile(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        if not self.profile in os.listdir(self.path):
            with open(os.path.join(self.path, self.profile), 'w') as f:
                f.write(json.dumps(self.options, ensure_ascii=False, indent=4))

    def read_profile(self):
        with open(os.path.join(self.path, self.profile), 'r') as f:
            return json.loads(f.read())

    def update_profile(self, kwargs):
        profile = self.read_profile()
        for key, value in zip(kwargs.keys(), kwargs.values()):
            profile[key] = value

        with open(os.path.join(self.path, self.profile), 'w') as f:
            f.write(json.dumps(profile, ensure_ascii=False, indent=4))
