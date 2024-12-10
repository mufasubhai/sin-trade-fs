For best results to set up the project, I recommend installing 
homebrew (if on mac)
once you've installed homebrew, asdf for versions
asdf plugin add nodejs
asdf plugin add python
asdf install python 3.12.4
asdf global python 3.12.4
asdf install nodejs 22.1.0
asdf global nodejs 22.1.0
brew install pnpm
cd sin-trade-fe
pnpm install

create virtual environments. Important for launch.json
python -m venv sin-trade-ds/ds-venv
source sin-trade-ds/ds-venv/bin/activate
pip install -r sin-trade-ds/requirements.txt
deactivate

python -m venv sin-trade-be/be-venv
source sin-trade-be/be-venv/bin/activate
pip install -r sin-trade-be/requirements.txt
deactivate

# for running tests while you develop

- open a separate terminal for ds and be

- in BE
1. source sin-trade-be/be-venv/bin/activate
2. cd sin-trade-be
3. pytest

- in DS
1. source sin-trade-ds/ds-venv/bin/activate
2. cd sin-trade-ds
3. pytest



