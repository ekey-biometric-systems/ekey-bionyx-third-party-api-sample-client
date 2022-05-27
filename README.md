# Introduction
ekey bionyx third-party API Python sample
This project contains Python sample code for creating, listing and deleting function webhooks for an ekey bionyx system.

# Requirements
To work with the third-party API you need a confirmed ekey bionyx account. To get a confirmed ekey bionyx account, first download the ekey bionyx app for Android or iOS from the platform stores.
Then launch the app and follow the instructions to create an account.
We recommend that you already have at least one registered device in your ekey bionyx system before starting to work with this API. Therefore, follow the instructions to activate an ekey bionyx device in the ekey bionyx app.
Finally, enable "Smart home connections" for your ekey bionyx system in the ekey bionyx app under "Settings".

# Run the sample in Python

- You will need to install dependencies using pip as follows:
```Shell
$ pip install -r requirements.txt
```

Run api_operation_sample.py from shell or command line.


# Running the app
To access the third-party API, you need to authenticate yourself with your ekey bionyx account. You will receive an access token after having logged into the ekey bionyx account.
This access token allows you to work with the ekey bionyx third-party API. Either you already have a valid token, which is not very likely the first time you run this app, or you must select the second option in the app.
The web browser will open and you will be asked to log in with your ekey bionyx credentials. If the authorization was successful, copy the redirected URL and paste it into the program prompt.

After you have provided a valid access token, the program will list all the systems that can be managed with this API. If you have not enabled "Smart home connections", you will not be able to create a webhook.
By default, the next operations are performed on the first system in the system list.

Now the program is ready to create, list or delete function webhooks.

# Creating a function webhook
You can see several webhook samples in the SampleWebHooks folder. You can either edit one of these samples with your own parameters or create your own webhook sample in this folder.
All webhook examples will appear in the Webhook Query workflow after you have selected the Create Webhook action in this program's workflow.  



