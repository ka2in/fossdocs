.. meta::
   :keywords: joomla, vps, sharedhosting, serveradmin, webdev, migration, unmanagedvps

===================================================================
Migrating a Joomla website from shared hosting to an unmanaged VPS 
===================================================================

Published on May 11, 2022 by Fayçal Alami-Hassani `@gnufcl@fosstodon.org <https://fosstodon.org/@gnufcl>`_

.. figure:: pics/talk-to-me-mini.jpg
   :alt: Migrating Joomla from shared hosting to VPS
   :align: center

   Picture by Stéphane Wootha Richard under `CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/deed.en>`_ License

Migrating a website from a shared hosting plan to an unmanaged VPS might seem a daunting task at the beginning. Depending on your acquaintance with server administration, it may take you a few days to several weeks to gather all the relevant information and organize the required steps in a structured, logical way to set up a custom migration project. 

There are plenty of resources about the topic, both online and offline. However, most of them only describe a tiny part of the entire process.

The biggest challenges that you might face when migrating from shared hosting to an unmanaged VPS are related to the following topics:

- Software stack to use, i.e. operating system, database technology, web server, and programming language.  

- Backup, data transfer, and restore strategy.

- Choosing between server administration with the Linux command line (CLI) or GUI-based hosting panels such as cPanel, Plesk, and Froxlor.

- User permission management.

- DNS settings and configuration.

- Testing the website before the actual domain transfer.

- SSL certificate management.

In this tutorial, you will learn how to migrate a Joomla website from a shared hosting provider to an unmanaged VPS server.

.. Note::

	When we talk about virtual private servers (VPS), we distinguish between two main categories: *managed* vs. *unmanaged* VPS. Put in a few words, An unmanaged VPS plan gives you full control over the technical aspects of your server management and administration. There is no technical support to resolve issues and you are responsible for maintaining your server, including the installation of patches and updates, among other things.

.. _Requirements:     

Prerequisites
==============

This tutorial assumes that you already have the following:

- LAMP stack installed on your VPS server. LAMP is short for "Linux + Apache + MySQL + PHP".

- Non-root user with sudo privileges on your VPS server.

- SSH access to your VPS server.

Before you follow this guide, make sure to configure your environment accordingly.

.. _Credentials: 

Performing the backup on your shared hosting account
====================================================

To backup your website files and the corresponding database, follow these steps: 

#. Login to your shared hosting account.

#. In your cPanel, go to **File Manager** > **public_html**.

	.. figure:: pics/file-manager-cpanel.png
		:alt: File Manager in cPanel
		:align: center

#. Inside the **public_html** directory, check your database login credentials in the file 'configuration.php'. You should look for the following entries:

   - ``public $user``: Database user name
   - ``public $password``: Database password
   - ``public $db``: Database name
   - ``public $dbprefix``: Database prefix  

	.. figure:: pics/public-html.png
		:alt: public_html in the cPanel
		:align: center

#. In the cPanel main menu, go to **Backup** > **Databases** > **MySQL® Database Wizard**.

	.. figure:: pics/mysql-database-wizard.png
		:alt: public_html in the cPanel
		:align: center

   The Backup Wizard provides multiple options. Select **Full or Partial Backup** > **Select Partial Backup** > **MySQL Databases**. This will allow you to download a backup of the MySQL database(s) of your Joomla website to your local machine.

	.. figure:: pics/partial-backup-db.png
		:alt: public_html in the cPanel
		:align: center 

#. Login to the backend of your Joomla website.

	.. figure:: pics/backend-login-joomla.png
		:alt: public_html in the cPanel
		:align: center

	.. raw:: latex

		\newpage

#. To backup the website files, we will use an extension called `Akeeba Backup <https://www.akeeba.com/products/akeeba-backup.html>`_. 

 	.. figure:: pics/akeeba-backup-backend.png
		:alt: public_html in the cPanel
		:align: center

#. Before making a backup with akeeba, make sure to _`disable SSL`. To do so, navigate to **System** > **Global Configuration** > **Server** > **Force HTTPS**. Select the option **None** from the drop-down menu.

	.. figure:: pics/global-configuration-joomla.png
		:alt: public_html in the cPanel
		:align: center

	.. raw:: latex

		\newpage

#. Next, go to **Components** > **Akeeba Backup** > **One-Click Backup** > **Default Backup Profile**

	.. figure:: pics/akeeba-backup-demo.png
		:alt: public_html in the cPanel
		:align: center

#. Once the backup process has completed, click on the "**i**" button below the green "**Download**" button on the right to display your "**Backup Archive Information**".

	..	note::

		An Akeeba backup file has a ``.jpa`` extension.

	.. figure:: pics/akeeba-backup-management.png
		:alt: public_html in the cPanel
		:align: center

#. In your shared hosting account, navigate to the location of your Akeeba backup file through **File Manager** > **public_html** > **path-to-akeeba-backup**. Download the .jpa file to your local machine.

#. Now that you have downloaded your backup file, you need to re-enable SSL for your entire website. On your shared hosting account, navigate to the folder ``public_html`` and open the file "configuration.php".

   Search for the entry ``public $force_ssl`` and switch the value from 0 to 2: 

	.. code-block:: php

		public $force_ssl = 2

#. Save your changes and return to your Joomla Backend. Go to **System** > **Global Configuration** > **Server**. 

#. Navigate to the option **Force HTTPS** and select **Entire Site** from the drop-down menu.

#. Download the `Akeeba Kickstart Core <https://www.akeeba.com/products/akeeba-kickstart.html>`_ by clicking on the button **Download Core**.

#. In the next page that will open, click on the green button **Download Core v.xxx**, where xxx refers to the current version number. This will download a .zip file containing the file ``kickstart.php``. We will place this php file in the root of our site to restore the Joomla backup.  

Preparing your new VPS server to host your website
===================================================

.. figure:: _static/pics/joomla-vps/spacedog-repairman-mini.png
   :alt: Preparing your new VPS server
   :align: center
   :width: 400

   "Spacedog Repairman" by `Katharsisdrill <https://katharsisdrill.art>`_ under `CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`_ License


You need to test your website on the new VPS before performing the actual domain transfer from your shared hosting to the new VPS.

Option 1: Adding an entry to your hosts file
---------------------------------------------

On linux systems, the ``/etc/hosts`` file maps hostnames to IP addresses. 

To edit the hosts file on your system, type the following command:

.. code-block:: bash

	$ sudo nano /etc/hosts

Add the following lines to the bottom of the hosts file:

.. code-block:: bash
	:linenos:
	
	IP_address_of_your_VPS 	domainname.com
	IP_address_of_your_VPS 	www.domainname.com

Replace domainname.com by your actual domain name, then press ``Ctrl + O`` to save your changes and ``Ctrl + X`` to close the nano editor.

Clearing the DNS cache after updating your hosts file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Note:: 

	On some Linux systems, you may need to flush the DNS cache in order to update the domain resolution to the new IP address. On Debian-based distros, caching DNS queries is performed with the ``systemd-resolved`` daemon.

To find out if ``systemd-resolved`` is running on your system, type the following command in your terminal:

.. code-block:: bash

	$ sudo systemctl is-active systemd-resolved 

If the output shows the status **active**, it means that the daemon is up and running.

To clear the DNS cache, run the following command:

.. code-block:: bash
	
	$ sudo systemd-resolve --flush-caches

You can now check the cache size with the command:

.. code-block::
	
	$ sudo systemd-resolve --statistics

The entry ``Current Cache Size: 0`` will appear in the output if the DNS cache has been cleared successfully. 


Option 2: Adjusting the DNS records
----------------------------------- 

For testing purposes, you can create a ``DNS Zone`` for your domain on the new VPS server. The ``DNS Zone`` section allows you to configure your domain for the different services that you intend to provide.

Suppose that you already have a domain that is registered with another service provider. To avoid any service interruptions before transferring your domain to a new provider, you can add a DNS zone before you begin the domain name transfer process.
		
.. Warning:: 

	Make sure to configure the DNS servers accordingly to take the DNS zone into account.

Adding a ``DNS Zone`` generally involves the following steps:

		- Entering a domain name in the ``DNS Zone`` section
		- Choosing whether you want to enable minimal records, the default is ``No``
		- Checking the pricing details
		- Confirming the Special Terms for the Webdomain and the General terms of service

#. Login to your shared hosting account.

#. In your cPanel, go to **Domains** > **Zone Editor**.

	.. figure:: pics/dns-zone-editor.png
   		:alt: DNS Zone editor
   		:align: center

#. In your **Zone Editor**, go to **Actions**, then select the tab **+A Record**. A new window with the title **Add an A Record for “yourdomain.com”** will open.

	.. figure:: pics/a-record-dns.png
   		:alt: A Record DNS
   		:align: center

#. In the **Name** field, enter your fully-qualified domain name (FQDN) by appending a dot at the end of your domain name: ``joomla-domain.com.``.

	.. figure:: pics/a-record-dns-name.png
   		:alt: A Record DNS Name
   		:align: center

   	.. raw:: latex

		\newpage

#. In the **Address** field, enter the IP address of your new Virtual Private Server (VPS). Remember that you want the DNS server from your shared hosting plan to point to your new VPS. By doing so, you can test if everything is working fine before requesting a domain transfer.

	.. figure:: pics/a-record-dns-address.png
   		:alt: A Record DNS Address
   		:align: center

Uploading the required files to your VPS server
------------------------------------------------

To restore the Joomla website on your new VPS server, you will need these three files:

#. The Akeeba backup file with the ``.jpa`` extension

#. The SQL dump file that we have generated with the Backup Wizard in cPanel

#. The ``kickstart.php`` file that we have extracted from the Akeeba Kickstart Core

To upload each of these files to your VPS server via ssh, use the ``scp`` command as shown below:

.. code-block:: bash

	$ scp -P PORT-NUMBER /PATH/TO/FILE USER@IP-ADDRESS:PATH/TO/DESIRED/DESTINATION

Replace the parameters of the scp command by their actual values, i.e.:

.. table::
   :class: tight-table
   :widths: 30 70

   +---------------+--------------------------------------------------------------------------------------------------------------------------+
   | Parameter     | Description                                                                                                              |
   +===============+==========================================================================================================================+
   | PORT-NUMBER   | the port number your are using to connect to your VPS server through ssh. The default port number for ssh connections is |
   |               | 22, but you can set a different port number for your ssh connection.                                                     |
   +---------------+--------------------------------------------------------------------------------------------------------------------------+
   | /PATH/TO/FILE | the path to the file that you want to upload to your VPS server                                                          |
   +---------------+--------------------------------------------------------------------------------------------------------------------------+
   | USER          | The active ssh user. You will find all your ssh credentials in the corresponding section on your customer page. If stil  |
   |               | doubt, contact your VPS provider.                                                                                        |
   +---------------+--------------------------------------------------------------------------------------------------------------------------+
   | IP-ADDRESS    | The IP address of your VPS server                                                                                        |
   +---------------+--------------------------------------------------------------------------------------------------------------------------+

Creating an empty MySQL database
--------------------------------

In the section `Performing the backup on your shared hosting account`_, you made a backup of your MySQL database. You will now create an empty database on your VPS to import the SQL dump file.

Login to MySQL by typing the following command in your VPS terminal:

.. code-block:: bash

	$ mysql -u root -p

Once you enter your password, you will get access to the MySQL shell prompt. Now, you will create a new database with the following command:

.. code-block:: sql

	mysql> CREATE DATABASE new_database;

.. Note::

	You can replace the value `new_database` by a name that suits your needs. When choosing a name for your MySQL database, follow these naming convention rules:

	- Use lowercase
	- Use only alphabetical characters
	- Do not use numeric characters
	- Avoid using prefixes
	- Give your database a self-explanatory name

If everything went fine, the shell prompt will display the following output:

.. code-block:: sql
	:linenos:

	Output
	Query OK, 1 row affected (0.00 sec)

Importing the SQL dump into your new database
----------------------------------------------

We will now assign a user `bob` to our newly created database by typing the command below. Make sure to change the username ``bob`` and the deafult ``password`` to a strong password of your own:

.. code-block:: sql

	mysql> CREATE USER 'bob'@'localhost' IDENTIFIED BY 'password';

Use the key combination ``Ctrl + D`` to leave the MySQL shell prompt. 

In the VPS terminal, you can now import the SQL dump file with the following command:

.. code-block:: bash

	$ mysql -u 'username' -p 'new_database' < 'data-dump.sql'

Setting up a virtual host on your VPS
-------------------------------------

At the beginning of this guide, we mentioned in the :ref:`Requirements <Requirements>` section that we will use Apache as a web server in our stack. Apache allows you to configure multiple virtual hosts, making it possible to host more than one domain on a single server. 

In our particular scenario, this means that we can host all the following domains on our VPS, as long we have sufficient storage, RAM, CPU, and IOPS resources:

- techwriting-website.com
- webdev-website.net
- infosec-website.org
- etc.

#. Before you set up a virtual host, make sure that Apache is up and running on your VPS. To do so, type the following command:

   .. code-block:: bash

		$ sudo systemctl start apache2

#. To start the Apache2 server automatically on boot, use the following command:

   .. code-block:: bash

		$ sudo systemctl enable apache2

#. From now on, you will have to create a dedicated folder under ``/var/www`` for each new domain that you want to host on your VPS. For instance, to create the domain that will host your Joomla backup on the new VPS, type the following command:

   .. code-block:: bash

		$ sudo mkdir /var/www/joomla-domain

   Replace the parameter ``joomla-domain`` by the actual domain name that your are using for your Joomla website.

#. Assign ownership of the newly created directory with the ``$USER`` environment variable by using the command below. The ``$USER`` environment variable is identical to the ``$LOGNAME`` environment variable, which represents the currently logged-in user:
   
   .. code-block:: bash
		
		$ sudo chown -R $USER:$USER /var/www/joomla-domain

#. Make sure that you granted the correct web root permissions by typing the command below. The folder's owner should have **read/write/execute** permissions, while group and others should only have **read/execute** privileges.


   .. code-block:: bash

		$ sudo chmod -R 755 /var/www/joomla-domain

	
   .. Note::

		The default permissions on a web server are 755 for directories and 644 for files.

#. In order for Apache to serve your content, you need to create an "Apache virtual host configuration file". To do so, we will create a new empty file with the nano editor:

   .. code-block:: bash

		$ sudo nano /etc/apache2/sites-available/joomla-domain.conf

   Put the following directives inside the configuration file:

   .. code-block:: bash
	   	:linenos: 

		<VirtualHost *:80>
		ServerAdmin webadmin@localhost
		ServerName joomla-domain
		ServerAlias www.joomla-domain
		DocumentRoot /var/www/joomla-domain
		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined
		</VirtualHost>

   .. Note:: 

		The email provided in the field ServerAdmin\ :sup:`[2]` is a placeholder. Make sure to use a working email address where the administrator of your Joomla domain can receive notifications. Also replace the parameters ``joomla-domain``\ :sup:`[3]` and ``www.joomla-domain``\ :sup:`[4]` by the actual domain name of your Joomla website.

   Once you have entered the relevant information, press ``Ctrl + O`` to save your changes and ``Ctrl + X`` to close the nano editor. 

#. We will now use a sample ``index.html`` file to check if our virtual host is working properly. To do so, we will create a new empty file with the nano editor:

   .. code-block:: bash

		$ sudo nano /var/www/joomla-domain/index.html

   .. raw:: latex

		\newpage

   Add the following lines in the empty file:

   .. code-block:: html
   		:linenos:

   		<html>
   		  <head>
   			<title>Welcome to my joomla-domain</title>
   		  </head>
   		  <body>
   			<h1>The joomla-domain virtual host is up and running</h1>
   		  </body>
   		</html>

#. **a2ensite** is a script that allows you to enable a specific site within the Apache2 configuration. This is achieved by creating symlinks (short for symbolic links) within the ``/etc/apache2/sites-enabled`` directory. 
   
   We will use **a2ensite** to enable our newly created site on the VPS. To do so, type the command:

   .. code-block:: bash

   		$ sudo a2ensite joomla-domain.conf

#. In the same manner that **a2ensite** adds symbolic links to enable a specific site, **a2dissite** removes symbolic links to disable a site. 

   In our particular case, we will use a2dissite to disable the default configuration file called ``000-default.conf``. 

   This default file is a fallback for all the requests that do not specify a configuration file.

   To disable the default configuration file, type the following command:

   .. code-block:: bash

   		$ sudo a2dissite 000-default.conf

#. Make sure that your configuration does not contain any erros by running the following command:

   .. code-block:: bash

   		$ sudo apache2ctl configtest

   If everything is fine, you should get the following output:

   .. code-block:: bash
		:linenos:

		Output
		Syntax OK

#. Each time you modify the Apache configuration, you need to restart the Apache service. Use the following command to restart Apache:

   .. code-block:: bash

   		$ sudo systemctl restart apache2

#. To check that the web server is serving your content now, go to ``http://joomla-domain`` in your browser. You should see the following output:

	**The joomla-domain virtual host is up and running** 

Restoring your Joomla website on the VPS
========================================

To restore your Joomla website on the VPS server, you first have to move the file ``kickstart.php`` and your Akeeba backup file ``backup-file.jpa`` to the root of your site on the VPS, i.e. inside the folder ``/var/www/joomla-domain``. 

#. If you have not already placed both files in the root of your Joomla site, open the terminal, then navigate to the folder containing both files. Next, type the following commands:

   .. code-block:: bash
		:linenos:

		$ sudo mv kickstart.php /var/www/joomla-domain
		$ sudo mv backup-file.jpa /var/www/joomla-domain

   Replace the parameter ``backup-file.jpa`` by the actual backup file name.

#. In your browser, type the following address:

   ``http://joomla-domain/kickstart.php``

#. The welcome screen of Akeeba Kickstart appears. Press the button **Click here or press ESC to close this message** on the bottom left.

   .. figure:: pics/kickstart-welcome-screen.png
		:alt: Kickstart Welcome Screen
		:align: center

#. The graphical interface of the **Akeeba archive extraction tool** will appear on your browser screen.

   .. figure:: pics/kickstart-extract-page.png
		:alt: Kickstart Extract Page
		:align: center

   .. raw:: latex

	\newpage

#. Scroll to the bottom of the screen, then click on the **Start** green button under the section **Extract files**.

   .. figure:: pics/kickstart-extract-button-2.png
		:alt: Kickstart Extract Button 2
		:align: center

#. The extraction progress window will appear. Once the files are extracted, click on the green button **Run the Installer** under **Restoration and Cleanup**

   .. figure:: pics/kickstart-extracting-bar.png
		:alt: Kickstart Extracting Bar
		:align: center

#. The site restoration script of Akeeba Backup will perform a pre-installation check. This allows you to take the necessary actions to correct any possible issues. If everything is fine, press the button **→ Next** on the top right side of the screen.

   .. figure:: pics/kickstart-preinstallation-check.png
		:alt: Kickstart Preinstallation Check
		:align: center

   .. raw:: latex

		\newpage

#. In the screen that appears, enter the :ref:`credentials <Credentials>` for the MySQL database that you have created. Once you have entered all the required information, click on the button **→ Next** on the top right side of the screen.

   .. figure:: pics/kickstart-restoration-database.png
		:alt: Kickstart Restoration Database
		:align: center

#. A **Database Restoration Progress Bar** will appear. If the restoration was successful, you wil see the message: **The database restoration was successful**. 

	.. figure:: pics/kickstart-database-progress.png
		:alt: Kickstart Database Progress
		:align: center

	.. raw:: latex

		\newpage

#. In the screen that appears, enter the site parameters such as "Site name" and "Live site URL". Once you have entered all the required information, click on the button **→ Next** on the top right side of the screen.

	.. figure:: pics/kickstart-site-parameters.png
		:alt: Kickstart Site Parameters
		:align: center

#. If the restoration process has completed successfully, you will see the creen below. You can now visit you site's frontend or login to the site's backend.

	.. figure:: pics/restoration-cleanup-akeeba.png
		:alt: Kickstart Restoration and Cleanup
		:align: center

Installing Let's Encrypt certificates with Certbot
==================================================

Now that you have restored your Joomla website, remember that you had to `disable SSL`_ before making the backup with Akeeba.
To protect your website, you can install TLS/SSL certificates from Let's Encrypt. 

Let's Encrypt is a non-profit and open certificate authority managed by the `Internet Security Research Group <https://www.abetterinternet.org/>`_, a public-benefit corporation based in California.

To issue the TLS/SSL certificates and install them automatically on the web server, we are going to use Certbot, an open-source software developed by the `Electronic Frontier Foundation <https://www.eff.org/>`_. 

.. figure:: pics/certbot.jpg
   :alt: Installing Let's Encrypt certificates with Certbot
   :align: center

   Picture by the Electronic Frontier Foundation under `CC BY 2.0 <https://creativecommons.org/licenses/by/2.0/>`_ License

.. Note::

	Before you follow the instructions below, make sure HTTPS traffic is allowed by your firewall. The default port number for HTTPS traffic is 443. 

#. In your terminal, run the following command to install Certbot with the plugin that allows the integration with the Apache web server:

	   .. code-block:: bash

   		$ sudo apt install certbot python3-certbot-apache

#. Press ``Y``, then ``Enter`` to run the installation.

#. To issue a certificate and reconfigure apache automatically, run the command:

	   .. code-block:: bash

   		$ sudo certbot --apache
			
#. Carefully read the questions that will appear on your terminal. Provide a valid email address.

#. Agree to the "Terms of Service" by pressing ``A`` (short for Agree).
   
#. Choose whether you want to share your email address with the Electronic Frontier Foundation by pressing ``Y`` to confirm or ``N`` to refuse.

   .. raw:: latex

	\newpage

#. You will then get the output shown below. Indicate the domains that you want to enable HTTPS for by selecting the appropriate listed numbers: 

	.. code-block:: bash
		
		Plugins selected: Authenticator apache, Installer apache

		Which names would you like to activate HTTPS for?
		- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		1: joomla-domain.com
		2: www.joomla-domain.com
		- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		Select the appropriate numbers separated by commas and/or spaces, or leave input
		blank to select all options shown (Enter 'c' to cancel): c
		Please specify --domains, or --installer that will help in domain names autodiscovery, or --cert-name for an existing certificate name.

#. In the next prompt that appears, choose whether or not you want to force redirecting HTTP to HTTPS traffic.

	.. code-block:: bash

		Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
		- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		1: No redirect - Make no further changes to the webserver configuration.
		2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
		new sites, or if you're confident your site works on HTTPS. You can undo this
		change by editing your web server's configuration.
		- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		Select the appropriate number [1-2] then [enter] (press 'c' to cancel): 

#. Once you have answered all the questions, Certbot will start the installation.

#. If the installation was successful, you will get the following output:

	.. code-block::

		- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		Congratulations! You have successfully enabled https://www.joomla-domain.com

		You should test your configuration at:
		https://www.ssllabs.com/ssltest/analyze.html?d=www.joomla-domain.com
		- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		IMPORTANT NOTES:
		 - Congratulations! Your certificate and chain have been saved at:
		   /etc/letsencrypt/live/www.joomla-domain.com/fullchain.pem
		   Your key file has been saved at:
		   /etc/letsencrypt/live/www.joomla-domain.com/privkey.pem
		   Your cert will expire on 2022-10-25. To obtain a new or tweaked
		   version of this certificate in the future, simply run certbot again
		   with the "certonly" option. To non-interactively renew *all* of
		   your certificates, run "certbot renew"
		 - If you like Certbot, please consider supporting our work by:

		   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
		   Donating to EFF:                    https://eff.org/donate-le

Certbot has now installed your TLS/SSL certificate and configured Apache accordingly.


	




























