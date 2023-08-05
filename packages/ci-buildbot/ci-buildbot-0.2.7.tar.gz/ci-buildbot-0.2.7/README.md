# ci-buildbot

`ci-buildbot` is a command line tool to do slack messaging from CodePipelines.  `ci-buildbot` acts as a Slack App in
order to do its work.

To install:

```
pyenv virtualenv 3.6.5 ci-buildbot
pyenv local ci-buildbot
pip install -r requirements.txt
pip install -e .
```

Now set up the environment:

```
cp etc/environment.text .env
```

You'll need to know two things: 

* `SLACK_API_TOKEN`: this your Slack app's Oath token
* `CHANNEL`: this is the channel you want `ci-buildbot` to post into.  Note that if this is a private channel, you'll
	need to invite the `ci-buildbot` app into that channel before you'll see any messages.

Now you can run the main command, `buildbot`:

```
buildbot --help
```
