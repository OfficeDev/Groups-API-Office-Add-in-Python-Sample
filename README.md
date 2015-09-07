# Groups-API-Office-Add-in-Python-Sample
This repository contains a Python/Django code sample that connects to the Office 365 Groups API as both a stand-alone web application and from within an Office add-in.

For a video introduction to the sample, see "Office Dev Show - Episode 7 - Getting Started with Python | Office Dev Show | Channel 9" at https://channel9.msdn.com/Shows/Office-Dev-Show/Office-Dev-Show-Episode-7-Getting-Started-with-Python

## Environment Setup ##
Python developers have several development environments to choose from. This project was built in Visual Studio 2015 with the Python tools for Visual Studio. These tools have been available for a while and come as an installation option in Visual Studio 2015. If you are using something other than Visual Studio, you can certainly export the individual files and re-leverage them in a different IDE.

Office 365 applications are secured by Azure Active Directory, which comes as part of an Office 365 subscription. If you do not have an Office 365 Subscription or associated it with Azure AD, then you should follow the steps to [Set up your Office 365 development environment](https://msdn.microsoft.com/office/office365/HowTo/setup-development-environment "Set up your Office 365 development environment") from MSDN.

## Registering the App ##
The first step in developing an application that connects to Office 365 is registering an application with Azure AD.

1. Sign-in to the [Azure Management Portal](https://manage.windowsazure.com "Azure Management Portal") using an account that has administrator access to the Azure AD Directory for Office 365.
2. Locate and select the **Active Directory** option towards the bottom of the left navigation (if you don't have a full Azure subscription, it might be your only option).
3. In the directory listing, select the directory associated with the Office 365 subscription you want to work with.
4. Next, select the **Applications** tab in the top navigation:
![Applications tab](http://i.imgur.com/nv168lw.png)
5. Click on the **ADD** button at the bottom center of the footer to launch the add application dialog:
![Add application in Azure AD](http://i.imgur.com/GbyS3u4.png)
6. Select **Add an application my organization is developing**
7. On the next screen, provide a **Name** for the application, keep the **Type** set to **Web Application and/or Web API** and click the next arrow.
8. Next, provide a **Sign-On URL** (points to where you want tokens returned http://localhost:8888/login) and **App ID URI** (any globally unique URI such as https://tenant.onmicrosoft.com/MyPythonGroupsApp). Don't worry, these values can be changed later:
![Applicationi Sign-on URL and URI](http://i.imgur.com/ZwnTyP5.png)
9. Click the check button to provision the new application in Azure AD.
10. When the application finishes provisioning, click on the **Configure** tab in the top navigation.
11. Locate the **CLIENT ID** and copy it to notepad...we will configure this as a setting in PHP later.
12. Locate the **Application is multi-tenant** field and toggle it to **YES** (this allows any organization to use the application). 
13. Because the application supports both stand-alone and Office add-in scenarios, we need to add separate reply URLs for each. The Office add-in uses separate URL routes pre-fixed with an /addin path (ex: http://localhost:8888/login and http://localhost:8888/addin/login). Add this in REPLY URL section:
![Reply URLs](http://i.imgur.com/27B0Sew.png)
14. Locate the **Keys** section and use the drop-down to generate a new 2 year key. Please note that the key (also referred to as a password or secret) will only display after clicking the Save button in the footer. This is the only time the key can ever be displayed, so make sure to copy it to notepad so we can use it later:
![Application keys](http://i.imgur.com/ScmVcDU.png)
15.  After saving/retrieving the key, locate the **permissions to other applications** section at the bottom of the screen.
16.  Use the **Add Application** button to launch the Permissions to other applications dialog.
17.  Locate the **Office 365 unified API (preview)** application, select it, then click the check button to close the dialog:
![Permissions to other applications](http://i.imgur.com/16yCo3A.png)
18.  Back on the main configuration screen, locate the **Office 365 unified API (preview)** application you added in the **permissions to other applications** section, click on the Delegated Permissions dropdown and add permissions for **Access directory as the signed in user** and **Read all groups (preview)**:
![Permissions](http://i.imgur.com/61a6wP2.png)
19.   Click the **Save** button in the footer one last time to save the changes you made to permissions.

## Updating authhelper.py ##
The solution contains a authhelper.py file (located in the app folder), which contains all the settings specific to the application. It needs to be updated with many of the values captured from the application registration process we just finished in Azure Active Directory. Specifically, values for client_id and client_secret should be updated to reflect the values from your application registration in Azure AD.

1. client_id should be set to the value from **Step 11** above
2. client_secret should be set to the value from **Step 14** above

Here is the complete authhelper.py file: 

    from urllib.parse import quote, urlencode
    import requests
    
    # Client ID and secret from Azure AD
    client_id = '1e06f32d-531a-42ae-917e-40b9904bb5a3'
    client_secret = 'YcvFcqm0knHADJboSLxT3Ampq+Em9M6xgkgf0KFgy3A='
	...

## Running the Stand-alone Web Application ##
There isn't anything tricky about the stand-alone web application. When it launches, it will look for a cached refresh token. If one exists, it will use it to get a new access token and query Office 365 Groups. If it doesn't have a cached token, it will redirect the user to a login page that will ultimately acquire a token and put it into cache.
## Running the Office Add-in ##
The solution contains and Office Add-in project (MyPythonGroups.Office), which contains the add-in manifest that is deployed to Office. Unfortunately, Visual Studio does not currently support associating a Python web project with the Office project. The only thing we loose is the ability to automatically update the add-in manifest with the URL of our app. However, we can easily do this manually:

> NOTE: at the time of this publication, Office Add-ins were not yet supported in Office for Mac. If you are developing Python on a Mac, you might need to use the add-in catalog deployment approach and test the add-in in Excel Online (ie - in a browser). 

1. Open the MyGroupsPython.Office.xml file (located in the MyPythonGroups.Office project) and update the DefaultValue attribute of the SourceLocation element to the location you are running the Python website (default is http://localhost:8888/addin/groups). You must point to the addin/groups view to have Python include the Office.js scripts it needs to interact with Excel:

    	<SourceLocation DefaultValue="http://localhost:8888/addin/groups" />

2. Save the changes to the MyGroupsPython.Office.xml and start debugging. Excel will likely launch before the website is running:
![Failed to load](http://i.imgur.com/3d9G8ab.png)
3. Click the Retry button once the website has started and the add-in should load correctly:
![Success add-in](http://i.imgur.com/rZvDOJ3.png)

> NOTE: Office add-ins must register any domain they will display in AppDomains section of the add-in manifest. This application has registered login.microsoftonline.com, which is the normal login page for Office 365. If you use a federated login, the add-in will not function as the federated login screen will get kicked out into a popup. It is possible to build a functional add-in with federation/popups, but was not the focus of this app.
