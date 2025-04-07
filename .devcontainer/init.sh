cd /workspaces
mkdir app
cp /workspaces/zmk-config/config/west.yml /workspaces/app/
west init -l app/
ln -s /workspaces/zmk-config/.devcontainer/makefile /workspaces/zmk-config/makefile
echo 'build "make build" inside /workspaces/zmk-config.'