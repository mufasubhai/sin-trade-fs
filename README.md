
- AI related citations and references located in CITATIONS.md

 - Auto generated CLAUDE.md file present as well

For best results to set up the project, I recommend installing 
homebrew (if on mac or linux)
once you've installed homebrew, asdf for versions
asdf plugin add nodejs
asdf plugin add python
asdf install python 3.12.4
asdf set -u python 3.12.4
asdf install nodejs 22.1.0
asdf set -u nodejs 22.1.0
brew install pnpm
cd sin-trade-fe 
pnpm install
cd .. (navigate back to root directory)

create virtual environments. Important for launch.json
python -m venv sin-trade-ds/ds-venv
source sin-trade-ds/ds-venv/bin/activate
pip install -r sin-trade-ds/requirements.txt
deactivate

python -m venv sin-trade-be/be-venv
source sin-trade-be/be-venv/bin/activate
pip install -r sin-trade-be/requirements.txt
deactivate

for running tests while you develop
open a separate terminal for ds and be
in BE
source sin-trade-be/be-venv/bin/activate
cd sin-trade-be
pytest

in DS
source sin-trade-ds/ds-venv/bin/activate
cd sin-trade-ds
pytest

to run tests in frontend
cd sin-trade-fe
pnpm test


