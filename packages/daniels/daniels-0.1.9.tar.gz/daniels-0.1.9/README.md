# Daniels

Inside, you'll find Daniel. Daniel is Harvested Financial's open source contribution. He's the slack bot we use for all of our monitoring -- you can import him and have him talk to various channels in slack, alerting people he needs to talk with.

A few potential use cases include pipeline monitoring, event alerts, and production error notifications. For small teams who don't have time to watch everything at once but also can't just wait until they notice things have broken, Daniel can be invaluable.  


He's written in python and can be installed via: 

    pip install daniels
    
You'll also need to install a slack bot verision of Daniel. We have our own, but can't release him just yet. All you need for _your_ daniel-enabled workspace is to add in a slack bot API token for a bot you've made, add the bot to the relevant channels you want to hear code updates from, and reference the slack_token in the code. You can refernce the token via environment variables (recommended), or by directly passing in token in the code (not recommneded for production). If no token is passed, Daniel searches via os for a "slack_token" exported variable and throws an error if he can't find one.

A sample use of him is:

```python
import daniels

daniel = daniels.Daniel(token='your-token-here', channel='target-channel', emoticon= " :dollar: ")

msg = "Hi, I'm Daniel."
daniel.say(msg)  # n.b. must pass string

# we like passing dollars on either side of a Daniel's message to identify it quickly, you don't have to
msg_two = "Here's a message with no emoticons around it."  
daniel.say(msg_two, enders=False)

# uploading is supported too
file_path = 'some_path/some_file.txt'
daniel.upload_file('title of file', file_path)
```
