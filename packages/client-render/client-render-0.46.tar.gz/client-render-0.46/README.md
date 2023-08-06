# How to configure new Image

* Choose AMI windows instance (for example, ...) with GUI
* Boot from image by hand (for example on the t2.medium)
* Execute script (link), why it's needed:
    * disable antivirus (no required)
    * disable firewall (no required)
    * enable download files from internet (no required)
    * set autoload with specific user (needs for the screenshots)
        * add info to the regedit (DEFAULT_USER, DEFAULT_PASS)
        * Disable Ctrl+Alt+Del at Configuration\Windows Settings\Security Settings\Local Policies\Security
    * add bat file in the autoload folder
    * add ability to use user-data for the instance 
    * additional installations:
        * install google chrome (no required)
        * install notepad++ (no required)
        * install python > 3.7
        * create virtualenv in the c:\venv\3dsmax\
* Install necessary environment and enter license:
    * 3DS MAX
    * Corona renderer
* Configure video driver for 3DS MAX 
* Shutdown
* Save the Image