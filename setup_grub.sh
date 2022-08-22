sudo add-apt-repository ppa:danielrichter2007/grub-customizer
sudo apt update -y && sudo apt upgrade -y
sudo apt install grub-efi grub2-common grub-customizer
sudo grub-install
sudo cp /boot/grub/x86_64-efi/grub.efi /boot/efi/EFI/pop/grubx64.efi
# /boot/efi/EFI/pop/grub.cfg copy that in the config file of a grub customizer.
git clone https://github.com/ChrisTitusTech/Top-5-Bootloader-Themes
cd Top-5-Bootloader-Themes
sudo ./install.sh
cd ..
rm -rf Top-5-Bootloader-Themes