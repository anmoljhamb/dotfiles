echo "alias cls=clear" >> ~/.bashrc
# change the power mode of the wifi.
sudo sed -i '$d' /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
sudo sh -c "echo 'wifi.powersave = 2' >> /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf"
sudo systemctl restart NetworkManager
curl -sS https://starship.rs/install.sh | sh
