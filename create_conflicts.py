from os import listdir
from os.path import isfile, join
import shutil
import random

from bs4 import BeautifulSoup
import git


REPRO_URL = "git@github.com:sibalzer/git_workshopxy.git"


DEFAULT_FILES = ["example.html"]

# https://imgur.com/a/kJcWEo9
MEMES_URLS = ["https://i.imgur.com/Fvch9sU.jpg",
              "https://i.imgur.com/IuTjjHx.jpg",
              "https://i.imgur.com/nvju7PD.jpg",
              "https://i.imgur.com/NJ1DW59.jpg",
              "https://i.imgur.com/DmV0wtl.png"]

# path gets deleted
REPRO_PATH = "tmp"
try:
    shutil.rmtree(REPRO_PATH)
except FileNotFoundError:
    pass

repo = git.Repo.clone_from(REPRO_URL,
                           REPRO_PATH, branch='main')
origin = repo.remote(name='origin')
origin.fetch()
origin.pull()

for b in repo.remote().fetch():
    name = b.name.split('/')[1]
    if name not in ["main", "master"]:
        print(f"add meme to branch {name}")

        repo.git.checkout('-B', name, b.name)

        # find new files
        files = [f for f in listdir(REPRO_PATH) if isfile(
            join(REPRO_PATH, f)) and f not in DEFAULT_FILES and f.endswith(".html")]

        for f in files:
            with open(join(REPRO_PATH, f), "r", encoding='utf-8') as file:
                soup = BeautifulSoup(file)

            # edit caption
            body = soup.find('body')
            h1 = soup.find('h1')
            h1.string = ('Alles Kaputt?')

            # add images to body
            meme_tag = soup.new_tag('img', src=random.choice(MEMES_URLS))
            body.append(meme_tag)

            # save and add to index
            with open(join(REPRO_PATH, f), "w", encoding='utf-8') as file:
                file.write(str(soup))
            repo.index.add(f)

        repo.index.commit("feat: add meme")
        origin.push()
repo.close()
