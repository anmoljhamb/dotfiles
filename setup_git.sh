git config --global user.email "talktoanmol@outlook.com"
git config --global user.name "Anmol Jhamb"
ssh-keygen -t ed25519 -C "talktoanmol@outlook.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub