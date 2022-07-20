#Set up the theme.
git clone https://github.com/vinceliuice/Orchis-theme.git
cd Orchis-theme
sudo ./install.sh
cd .. 
rm -rf Orchis-theme
git clone https://github.com/vinceliuice/Tela-icon-theme.git
cd Tela-icon-theme
./install.sh
cd ..
rm -rf Tela-icon-theme/
gsettings set org.gnome.desktop.interface icon-theme 'Tela'
gsettings set org.gnome.shell.extensions.user-theme name 'Orchis-Compact'
gsettings set org.gnome.desktop.interface gtk-theme 'Orchis-Compact'
gsettings set org.gnome.desktop.wm.preferences button-layout 'close,maximize,minimize:appmenu'
mkdir ~/.local/share/gnome-shell/extensions
unzip extensions.zip -d ~/.local/share/gnome-shell/extensions
# Setting up the wallpaper
gsettings set org.gnome.desktop.background picture-uri "file://$(pwd)/wallpaper.jpg"