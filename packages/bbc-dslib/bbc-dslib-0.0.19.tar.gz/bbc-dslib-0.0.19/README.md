# Data Scientist's Library (dslib)

This library's purpose is to mutualize classes and functions which can have multiple purposes.


# Install dslib

## Install specific version from public GCS package 

The GCS packages are public and do not require any authentication. 

```bash
pip install bbc-dslib
```

To install it with wrappers' dependencies (e.g. here Google and Prophet):

```bash
pip install bbc-dslib[google]
```

## Upgrade dslib version

To upgrade your dslib version to the latest available, run the following:

```bash
pip install --upgrade bbc-dslib
```


## Install editable version from Git repository

To install it locally in editable mode, go to your projects folder and run:

```bash
git clone ssh://git@git.blbl.cr/lib/dslib.git
pip install -e ./dslib/
```

To use the latest version of the library, simply pull the remote changes. To modify the library, do your changes and 
push them into the repository.

To install it with wrappers' dependencies (e.g. here Google and Prophet):

```bash
pip install -e ./dslib/[google,prophet]
```

---

# Contribute

## Process description

In a nutshell, the contribution process is the following:

- work is made on the `dev` branch, or on feature branches based on `dev`
- every time a developed feature on `dev` is reliable enough and needed in prod, `dev` is to be merged into master, and 
    a new version is to be created and deployed. Do not forget to delete locally and remotely your feature branch once 
    it is merged into `dev`

![](img/git_flow.png)


## Step-by-step process description

#### Develop a new feature

The process to add a new feature is the following:

- if your feature is rather small, you can commit it to `dev` directly
- if your feature is rather big, create a new branch from `dev` (please make its name descriptive of the developped 
feature) and once done, create a pull request to merge into `dev`

#### Make a new version with your new feature

Once your feature is in `dev` and you made sure it is reliable, you are able to release a new version of the lib which
will include your feature:

- make sure your branches (`dev`, `origin/dev`, `master`, and `origin/master`) are up to date
- modify `version.py` with your current version
- commit and push this change with message "version to x.x.x"
- create a pull request (`dev` into `master`)

Once your pull request is merged into `master`, you can deploy the new version lib version. Go to your local dslib 
repository and follow these steps:

- make sure you are up to date: `git checkout master` and `git pull`
- make sure you have all necessary requirements matched: `pip install -r deployment-requirements.txt`
- run `sh deploy.sh`

This will:
- create a new tag on git and push it
- make a package of your application (stored in ./dist)
- send the package to PyPI so anyone can use the latest version
