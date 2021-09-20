## Overview
When you write a wrangle that you just *love* and want to share it with the
world (or your future self), why go through all the hassle of
*opening* Firefox, *navigating* to your Gists page, *logging in* to GitHub, *copying and
pasting the code* (gasp!), and *pressing* the Create Gist button? Nevermind choosing a
filename, setting the syntax highlighting, and coming up with a description for
it! Did you see all those
words with *-ing* at the end? That's all stuff you have to *do*! What if you
could just have one button that does all that stuff for you? You could
potentially save valuable *seconds* of your life...

That's where **[Wrangle to Gist]({{ site.socials.github }}/{{ page.repo }})**
comes in. It's a simple script that gets added to any parameter in Houdini that
deals with snippets (chunks of code), and allows you to quickly post that
snippet straight to your [Gist Feed]({{ site.socials.gist }}). View the rest of
the features [below](#features).

## Installation

### Houdini Packages

1. Download the latest release [here](https://github.com/jamesrobinsonvfx/wranglegist/releases/latest/download/wranglegist.zip).
   * Optionally, you can clone this repo if you'd like instead.
2. Navigate to your houdini user preferences folder and into the `packages`
   directory (if the `packages` folder does not exist, create it).
   ```
   $HOUDINI_USER_PREF_DIR/packages
   ```
3. Copy the zip archive here and extact its contents.
4. Move (or copy) the `wranglegist.json` file to the parent directory
   `$HOUDINI_USER_PREF_DIR/packages`. Your `packages` folder should now look
   something like this:

   [![Packages Folder](https://www.jamesrobinsonvfx.com/assets/projects/wrangle-to-gist/images/packages-folder.png)](https://www.jamesrobinsonvfx.com/assets/projects/wrangle-to-gist/images/packages-folder.png)

5. Launch Houdini

### Manual Installation
If you prefer not to use Houdini packages for whatever reason, you can manually
copy the files to any Houdini location (`$HSITE`, `$HOUDINI_USER_PREF_DIR`) or
anyhwere on your `$HOUDINI_PATH`.

- `ParmMenu.xml` should live at the root. ie if you're moving these files into your user prefs
  folder, it should live right inside the `houdini18.5` folder.
- Copy the module `wranglegist.py` to `python2.7libs` or `python3.7libs`
  (depending on your Houdini installation version)


## Setup

### 1. Create a Personal Access Token

[![Scopes](https://www.jamesrobinsonvfx.com/assets/projects/wrangle-to-gist/images/personal-access-token.png)](https://www.jamesrobinsonvfx.com/assets/projects/wrangle-to-gist/images/personal-access-token.png)

In order to push gists to your GitHub account, you need to create a personal token to use. It is pretty straightforward,
and well-explained on GitHub's page [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token).

For the **Scopes** section, you can just select **gists**.

[![Scopes](https://www.jamesrobinsonvfx.com/assets/projects/wrangle-to-gist/images/scopes.png)](https://www.jamesrobinsonvfx.com/assets/projects/wrangle-to-gist/images/scopes.png)


### 2. Where to put the token

This tool will look for your personal access token inside your home folder.

Linux / Mac
```
~/gist_personal_access_token
```

```
%UserProfile%\gist_personal_access_token
```

1. Create an empty file in your home folder and call it `gist_personal_access_token`
2. On the first line, put your **GitHub Username**. For me, this would be `jamesrobinsonvfx`
3. On the second line, paste in the token that github created for you in the
   previous step. Your `~/gist_personal_access_token` file should now look like
   the following:
    ```
    jamesrobinsonvfx
    ghp_eeGRRdh7ESHGdfke3GJKEoC46rDmg
    ```
And that's it!

> Don't share your access token with anyone! This one is some gibberish, but
> close to what one would actually look like.

## Features
This menu item does one thing: push the snippet to your Gists feed! There are a couple extra features to note:

- Suggested filename will come from whatever the node is called (`opname(".")`),
  unless the node name is the default one from Houdini (ie. `pointwrangle`).

- Description field is left blank, unless your snippet's first line is a comment
  (`//` or `/*` for C-style languages, `#` or `"""` or `'''` for Python)

- You can choose from a few supported extensions:
```
.h
.vfl
.py
.ocl
```

> Please note that `.vfl` extensions aren't recognized by GitHub/Gist, so the
> format highlighting won't be there. That's why for Vex wrangles I typically
> use `.h` to get some nice color variation. It's close.

### Context
Any parameter named `snippet`, `code` or `python` will have this option in its
**Right Click** menu.

## Usage

<video width="720" height="405" autoplay loop>
	<source src="https://www.jamesrobinsonvfx.com/assets/projects/wrangle-to-gist/images/demo.mp4" type="video/mp4">
</video>