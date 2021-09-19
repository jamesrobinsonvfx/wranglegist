# Wrangle to Gist

## Installation

### Houdini Packages
1. [Get the latest release zip archive]()
   * Optionally, you can clone this repo if you'd like instead.
2. Navigate to your houdini user preferences folder and into the `packages`
   directory (if the `packages` folder does not exist, create it).
   ```
   $HOUDINI_USER_PREFS/packages
   ```
3. Copy the zip archive here and extact its contents.
4. Move (or copy) the `wranglegist.json` file to the parent directory `$HOUDINI_USER_PREFS/packages`
5. Launch Houdini

### Manual Installation
If you prefer not to use Houdini packages for whatever reason, you can manually
copy the files to any Houdini location (`$HSITE`, `$HOUDINI_USER_PREFS`) or
anyhwere on your `$HOUDINI_PATH`.

- `ParmMenu.xml` should live at the root. ie if you're moving these files into your user prefs
  folder, it should live right inside the `houdini18.5` folder.
- Copy the library `wranglegist` to `python2.7libs` or `python3.7libs`
  (depending on your Houdini installation version)


## Setup

### 1. Create a Personal Access Token

In order to push gists to your GitHub account, you need to create a personal token to use. It is pretty straightforward,
and well-explained on GitHub's page [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token).

For the **Scopes** section, you can just select **gists**.

[![Scopes]()]()



### 2. Where to put the token

This tool will look for your personal access token inside your home folder.

Linux / Mac
```
~/gist_personal_access_token
```

```
%UserProfile%\github_personal_access_token
```

1. Create an empty file in your home folder and call it `gist_personal_access_token`
2. On the first line, put your **GitHub Username**. For me, this would be `jamesrobinsonvfx`
3. On the second line, paste in the token that github created for you in the
   previous step. Your `~/gist_personal_access_token` file should now look like
   the following:
    ```
    jamesrobinsonvfx
    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
    ```
And that's it!


## Features
This menu item does one thing: push the snippet to your Gists feed! There are a couple extra features to note:

- Suggested filename will come from whatever the node is called (`opname(".")`). Unless the node name is the default
one from houdini (ie. `pointwrangle`).

- Description field is left blank, unless your snippet's first line is a comment
  (`//` or `/*` for C-style languages, `#` or `"""` or `'''` for Python)

- You can choose from a few supported extensions:
```
.h
.vfl
.py
.ocl
```
Please note that `.vfl` extensions aren't recognized by GitHub/Gist, so the format highlighting won't be there. That's
why for Vex wrangles I typically use `.h` to get some nice color variation. It's close.

- This menu item is available on the following node types:
  SOPs DOPs TOPs

- Any `Null` in any context that has a parameter called `snippet` will also be considered.

## Usage
[![Usage Demo]()]()