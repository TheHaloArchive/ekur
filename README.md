Ekur
===
A multi-purpose blender importer for Halo Infinite.

This project is split into two parts:
- [ekur](./ekur/): Tool to extract files required for the blender addon to function.
- [addon](./addon/): Actual addon to be installed into Blender.

### Requirements
- [Blender 4.3 or Above](https://www.blender.org/download/)
- Windows or Linux/GNU 64-bit machine.
- An installation of Halo Infinite.

### Installation/Setup
Download the zip file included in the [latest release](https://github.com/Surasia/Ekur/releases/latest) and install it by going into Blender preferences (Edit < Preferences), navigating to "Add-ons" and clicking on the "Install from disk" button in the drop-down menu.

Once the addon is installed, open the drop down for the "Ekur" addon and set your paths.
- Data Folder: Location to where files should be extracted. Make sure that the drive containing this folder has at least 30GBs of storage.

- Deploy Folder: This is a folder inside the installation directory for Halo Infinite, called "deploy". You can find your installation folder by clicking "Browse Local Files" in the context menu for the game in Steam.

After you're done setting your paths, click the "Download Required Files" button. This will download the latest build of Ekur for your platform, alongside the strings and visor definition files.


> [!TIP]
> Extracting files can take a long time depending on your system configuration.
> While extraction, Blender will temporarily freeze up.

Once the required files are downloaded, click the "Dump Required Files" button. This will run the main tool that extracts and serializes data from the game into a common format that the addon can use, alongside extracting all required bitmaps that the addon can utilize.

### Credits
- [cylix.guide](https://cylix.guide): Visor data
- [Chunch](https://github.com/Chunch7275) and [ChromaCore](https://bsky.app/profile/chromacore.bsky.social): Developing the Halo Infinite Modular Shader
- [Reclaimer](https://github.com/Gravemind2401/Reclaimer): Lots of the components for mesh importing.
