# 7pack
## What is 7pack?
7pack is not a replacement for pip. Instead, it works with pip. 7pack remedies some issues with pip, like the difficulty in installing all packages. In addition, it has a large repository, including nearly all of the most popular pip packages.

## How to install
7pack is a little different from pip. First, you enter the packages. Then, at the end you put flags. To install, put --install. For example, to install urllib3, the most popular pip package, you wold run the command ```7pack urllib3 --install```

## How to uninstall
Uninstalling with 7pack is like installing except the flag must be changed to --uninstall. To uninstall urllib3, you would run the command ```7pack urrlib3 --uninstall```

## List packages
Since 7pack requires packages, you need to enter any random string in 7pack and apply the --list flag. When I list packages I use ```7pack none --list```

## Upgrade Packages
Upgrading is just like installing and uninstalling. Just apply the --upgrade flag. To upgrade urllib3, run the command ```7pack urllib3 --upgrade```.

## Install/Uninstall all
This is the main reason 7pack was created. To uninstall/upgrade all, put one package, called "all". To upgrade all, run the command ```7pack all --upgrade```, and to uninstall all, run the command ```7pack all --uninstall```
